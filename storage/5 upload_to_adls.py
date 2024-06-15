from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

def initialize_storage_account(storage_account_name):
    try:
        # Get credentials and create service client
        credential = DefaultAzureCredential()
        service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)
        return service_client
    except Exception as e:
        print(f"An error occurred during service client initialization: {str(e)}")
        return None

def create_file_system(service_client, file_system_name):
    try:
        file_system_client = service_client.create_file_system(file_system_name)
        print(f"File system '{file_system_name}' created successfully.")
        return file_system_client
    except Exception as e:
        print(f"An error occurred during file system creation: {str(e)}")
        return None

def create_directory(service_client, file_system_name, directory_name):
    try:
        file_system_client = service_client.get_file_system_client(file_system_name)
        directory_client = file_system_client.create_directory(directory_name)
        print(f"Directory '{directory_name}' created successfully in file system '{file_system_name}'.")
        return directory_client
    except Exception as e:
        print(f"An error occurred during directory creation: {str(e)}")
        return None

def upload_file_to_directory(directory_client, local_file_path, file_name):
    try:
        file_client = directory_client.create_file(file_name)
        with open(local_file_path, "rb") as data:
            file_client.upload_data(data, overwrite=True)
        print(f"File '{file_name}' uploaded successfully to directory '{directory_client.path_name}'.")
    except Exception as e:
        print(f"An error occurred during file upload: {str(e)}")

if __name__ == "__main__":
    storage_account_name = 'mystrgeactazsdk2adlsv2'
    file_system_name = 'yourfilesystem'
    directory_name = 'yourdirectory'
    local_file_path = 'DALL·E 2024-06-11 19.40.20 - A detailed visualization of neural activation.webp'
    file_name = 'DALL·E 2024-06-11 19.40.20 - A detailed visualization of neural activation.webp'

    service_client = initialize_storage_account(storage_account_name)
    if service_client:
        file_system_client = create_file_system(service_client, file_system_name)
        if file_system_client:
            directory_client = create_directory(service_client, file_system_name, directory_name)
            if directory_client:
                upload_file_to_directory(directory_client, local_file_path, file_name)
