import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()


@app.blob_trigger(arg_name="myblob", 
                  path="blobuploadcontainer/{name}",
                  connection="AzureWebJobsStorage") 
def ProcessBlobFunction(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                f"Name: {myblob.name} \n"
                f"Blob Size: {myblob.length} bytes \n")
