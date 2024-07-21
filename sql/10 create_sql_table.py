import pyodbc
from azure.identity import DefaultAzureCredential
import urllib
from dotenv import load_dotenv
import os
import sys
load_dotenv()

server = os.getenv('SQL_SERVER_NAME')
database = os.getenv('SQL_DATABASE_NAME')
username = os.getenv('ADMIN_USER')
password = os.getenv('ADMIN_PASSWORD')




# Define the SQL script
sql_script = """
CREATE TABLE YellowTaxiData (
    doLocationId NVARCHAR(255),
    endLat FLOAT,
    endLon FLOAT,
    extra FLOAT,
    fareAmount FLOAT,
    improvementSurcharge NVARCHAR(255),
    mtaTax FLOAT,
    passengerCount INT,
    paymentType NVARCHAR(255),
    puLocationId NVARCHAR(255),
    puMonth INT,
    puYear INT,
    rateCodeId INT,
    startLat FLOAT,
    startLon FLOAT,
    storeAndFwdFlag NVARCHAR(255),
    tipAmount FLOAT,
    tollsAmount FLOAT,
    totalAmount FLOAT,
    tpepDropoffDateTime DATETIME,
    tpepPickupDateTime DATETIME,
    tripDistance FLOAT,
    vendorID NVARCHAR(255),
    vendorID_LPEP INT
);
"""

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish the connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Execute the SQL script
    cursor.execute(sql_script)
    connection.commit()

    print("Table created successfully.")

except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    print(f"An error occurred while executing the SQL script: {sqlstate}")
    sys.exit(1)

except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
    sys.exit(1)

finally:
    # Close the connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()