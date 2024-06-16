import os
import sys
import pyodbc

# Constants - Fetching from environment variables
SERVER = f"{os.getenv('SQL_SERVER_NAME')}.database.windows.net"
DATABASE = os.getenv('SQL_DATABASE_NAME')
DRIVER = '{ODBC Driver 18 for SQL Server}'
ADMIN = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

def get_connection():
    try:
        connection_string = f'DRIVER={DRIVER};SERVER=tcp:{SERVER},1433;DATABASE={DATABASE};Uid={ADMIN};Pwd={ADMIN_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        connection = pyodbc.connect(connection_string)
        
        print("Connection successful")
        return connection
    except pyodbc.Error as e:
        print(f"Error connecting to database: {str(e)}")
        sys.exit(1)

def create_table(cursor):
    try:
        cursor.execute("""
        CREATE TABLE Persons (
            PersonID int,
            LastName varchar(255),
            FirstName varchar(255),
            Address varchar(255),
            City varchar(255)
        )
        """)
        print("Table created successfully")
    except pyodbc.Error as e:
        print(f"Error creating table: {str(e)}")

def insert_data(cursor):
    try:
        cursor.execute("""
        INSERT INTO Persons (PersonID, LastName, FirstName, Address, City)
        VALUES (1, 'Doe', 'John', '123 Main St', 'Anytown')
        """)
        print("Data inserted successfully")
    except pyodbc.Error as e:
        print(f"Error inserting data: {str(e)}")

def read_data(cursor):
    try:
        cursor.execute("SELECT * FROM Persons")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("Data read successfully")
    except pyodbc.Error as e:
        print(f"Error reading data: {str(e)}")

def update_data(cursor):
    try:
        cursor.execute("""
        UPDATE Persons
        SET City = 'Newtown'
        WHERE PersonID = 1
        """)
        print("Data updated successfully")
    except pyodbc.Error as e:
        print(f"Error updating data: {str(e)}")

def delete_data(cursor):
    try:
        cursor.execute("""
        DELETE FROM Persons
        WHERE PersonID = 1
        """)
        print("Data deleted successfully")
    except pyodbc.Error as e:
        print(f"Error deleting data: {str(e)}")

def main():
    # Get database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Perform CRUD operations
    create_table(cursor)
    insert_data(cursor)
    read_data(cursor)
    update_data(cursor)
    read_data(cursor)
    delete_data(cursor)
    read_data(cursor)

    # Commit transactions
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    #edit firewall access for SQL server first, then run main function
    main()
