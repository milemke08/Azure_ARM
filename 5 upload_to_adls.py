from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient, DataLakeFileClient

def initialize_storage_account(storage_account_name):
    try:
        # Get credentials and create service client
        credential = DefaultAzureCredential()
        service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)
        return service_client
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_directory(service_client, file_system_name, directory_name):
    try:
        file_system_client = service_client.get_file_system_client(file_system_name)
        directory_client = file_system_client.create_directory(directory_name)
        print(f"Directory '{directory_name}' created successfully in file system '{file_system_name}'.")
        return directory_client
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def upload_file_to_directory(directory_client, local_file_path, file_name):
    try:
        file_client = directory_client.create_file(file_name)
        with open(local_file_path, "rb") as data:
            file_client.upload_data(data, overwrite=True)
        print(f"File '{file_name}' uploaded successfully to directory '{directory_client.path_name}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    storage_account_name = 'yourstorageaccount'
    file_system_name = 'yourfilesystem'
    directory_name = 'yourdirectory'
    local_file_path = 'path/to/your/file.txt'
    file_name = 'file.txt'

    service_client = initialize_storage_account(storage_account_name)
    directory_client = create_directory(service_client, file_system_name, directory_name)
    upload_file_to_directory(directory_client, local_file_path, file_name)
