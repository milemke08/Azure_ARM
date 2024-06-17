import os
import sys
import pyodbc
import pandas as pd
from azure.identity import DefaultAzureCredential

# Constants - Fetching from environment variables
SERVER = f"{os.getenv('SQL_SERVER_NAME')}.database.windows.net"
DATABASE = os.getenv('SQL_DATABASE_NAME')
USERNAME = os.getenv('ADMIN_USER')
PASSWORD = os.getenv('ADMIN_PASSWORD')
DRIVER = '{ODBC Driver 18 for SQL Server}'

def get_connection():
    try:
        # Establish a connection to Azure SQL Database
        connection_string = f'DRIVER={DRIVER};SERVER={SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        conn = pyodbc.connect(connection_string)
        print("Connection successful")
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {str(e)}")
        sys.exit(1)

def sanitize_column_names(df):
    """Sanitize column names to handle unnamed columns."""
    sanitized_columns = []
    for col in df.columns:
        if "Unnamed" in col:
            sanitized_columns.append(f"col_{df.columns.get_loc(col)}")
        else:
            sanitized_columns.append(col)
    df.columns = sanitized_columns
    return df

def convert_data_types(df):
    """Convert data types to ensure compatibility with SQL Server."""
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            df[col] = df[col].astype(str)
    return df

def ingest_csv_to_sql(file_path, table_name):
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Sanitize column names
        df = sanitize_column_names(df)

        # Convert data types
        df = convert_data_types(df)

        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute(f"""
        IF OBJECT_ID(N'{table_name}', N'U') IS NULL
        CREATE TABLE {table_name} (
            {', '.join([f"[{col}] NVARCHAR(MAX)" for col in df.columns])}
        )
        """)

        # Insert data into table
        for index, row in df.iterrows():
            cursor.execute(f"INSERT INTO {table_name} ({', '.join([f'[{col}]' for col in df.columns])}) VALUES ({', '.join(['?' for _ in df.columns])})", tuple(row))
        
        # Commit transaction
        conn.commit()
        print("Data ingestion completed successfully")
    except pyodbc.Error as e:
        print(f"Database error: {str(e)}")
    except Exception as ex:
        print(f"An error occurred: {str(ex)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python ingest_csv_to_sql.py <csv_file_path> <table_name>")
    #     sys.exit(1)
    
    csv_file_path = r'support\Azure_SDK_Learning.csv'
    table_name = 'AzureSDKLearning'

    ingest_csv_to_sql(csv_file_path, table_name)
