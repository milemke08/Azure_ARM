import azure.functions as func
import datetime
import json
import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeServiceClient

app = func.FunctionApp()


@app.blob_trigger(arg_name="myblob", 
                  path="blobuploadcontainer",
                  connection="AzureWebJobsStorage") 
def ProcessBlobFunction(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                f"Name: {myblob.name} \n"
                f"Blob Size: {myblob.length} bytes \n")
    # Get connection strings from environment variables
    blob_connection_string = os.getenv("AzureWebJobsStorage")
    adls_connection_string = os.getenv("ADLSGen2Storage")
    
    # Initialize BlobServiceClient and DataLakeServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    adls_service_client = DataLakeServiceClient.from_connection_string(adls_connection_string)
    
    # Source container and blob information
    source_container_name = "blobuploadcontainer"
    source_blob_name = myblob.name
    if source_blob_name.startswith(f"{source_container_name}/"):
        source_blob_name = source_blob_name[len(f"{source_container_name}/"):]
    else:
        source_blob_name = source_blob_name
    logging.info(f"source_blob_name: '{source_blob_name}'")
    
    # Target ADLS filesystem and path
    target_filesystem_name = "yourfilesystem"
    target_file_path = f"yourdirectory/{source_blob_name}"
    
    # Download the blob content
    source_blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
    logging.info(f"Request URL: '{source_blob_client.url}'")
    download_stream = source_blob_client.download_blob()
    blob_content = download_stream.readall()
    
    # Upload to ADLS Gen2
    filesystem_client = adls_service_client.get_file_system_client(file_system=target_filesystem_name)
    file_client = filesystem_client.get_file_client(target_file_path)
    
    # Create or overwrite the file in ADLS Gen2
    file_client.create_file()
    file_client.append_data(data=blob_content, offset=0, length=len(blob_content))
    file_client.flush_data(len(blob_content))

    logging.info(f"Blob {source_blob_name} successfully copied to ADLS Gen2 at {target_file_path}")