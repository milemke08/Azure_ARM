import os
import sys
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server, Database, Sku

# Constants
load_dotenv()
RESOURCE_GROUP_NAME = os.getenv('RESOURCE_GROUP_NAME')
LOCATION = os.getenv('LOCATION')
SQL_SERVER_NAME = os.getenv('SQL_SERVER_NAME')
SQL_DATABASE_NAME = os.getenv('SQL_DATABASE_NAME')
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

def create_resource_group(resource_client):
    try:
        resource_group_params = {"location": LOCATION}
        resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME, resource_group_params)
        print(f"Resource group '{RESOURCE_GROUP_NAME}' created or updated.")
    except Exception as e:
        print(f"Failed to create resource group: {str(e)}")
        sys.exit(1)

def create_sql_server(sql_client):
    try:
        server_params = Server(
            location=LOCATION,
            administrator_login=ADMIN_USER,
            administrator_login_password=ADMIN_PASSWORD
            
        )
        sql_client.servers.begin_create_or_update(RESOURCE_GROUP_NAME, SQL_SERVER_NAME, server_params).result()
        print(f"SQL server '{SQL_SERVER_NAME}' created.")
    except Exception as e:
        print(f"Failed to create SQL server: {str(e)}")
        sys.exit(1)

def create_sql_database(sql_client):
    try:
        database_params = Database(
            location=LOCATION,
            sku=Sku(name="Standard", tier="Standard")
        )
        sql_client.databases.begin_create_or_update(RESOURCE_GROUP_NAME, SQL_SERVER_NAME, SQL_DATABASE_NAME, database_params).result()
        print(f"SQL database '{SQL_DATABASE_NAME}' created.")
    except Exception as e:
        print(f"Failed to create SQL database: {str(e)}")
        sys.exit(1)

def main():
    # Authenticate with Azure
    credential = DefaultAzureCredential()

    # Create clients
    resource_client = ResourceManagementClient(credential, os.environ["AZURE_SUBSCRIPTION_ID"])
    sql_client = SqlManagementClient(credential, os.environ["AZURE_SUBSCRIPTION_ID"])

    # Create resources
    # create_resource_group(resource_client)
    create_sql_server(sql_client)
    create_sql_database(sql_client)

if __name__ == "__main__":
    main()
