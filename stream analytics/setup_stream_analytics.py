import json
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.streamanalytics import StreamAnalyticsManagementClient
from azure.mgmt.streamanalytics.models import (
    StreamingJob,
    Sku,
    SkuName,
    Input,
    Output,
    BlobStreamInputDataSource,
    BlobOutputDataSource,
    JsonSerialization
)
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Load configuration template
with open('stream analytics\config.json') as config_file:
    config_template = config_file.read()

# Replace placeholders with environment variables
config = config_template
for key, value in os.environ.items():
    config = config.replace(f"${{{key}}}", value)

# Convert the updated config to a dictionary
config = json.loads(config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Azure credentials and client
credential = DefaultAzureCredential()
client = StreamAnalyticsManagementClient(credential, config["subscription_id"])

def create_stream_analytics_job():
    try:
        logger.info("Creating Stream Analytics job...")
        poller = client.streaming_jobs.begin_create_or_replace(
            resource_group_name=config["resource_group"],
            job_name=config["job_name"],
            streaming_job=StreamingJob(
                location=config["location"],
                sku=Sku(name=SkuName.standard)
            )
        )
        job = poller.result()
        logger.info(f"Stream Analytics job '{config['job_name']}' created successfully.")
        return job
    except Exception as e:
        logger.error(f"Error creating Stream Analytics job: {e}")
        raise

def add_input_to_job():
    try:
        logger.info("Adding input to Stream Analytics job...")
        input_properties = Input(
            properties={
                "type": "Stream",
                "datasource": BlobStreamInputDataSource(
                    storage_accounts=[{
                        "account_name": config["stream_input_properties"]["datasource"]["properties"]["storageAccounts"][0]["accountName"],
                        "account_key": config["stream_input_properties"]["datasource"]["properties"]["storageAccounts"][0]["accountKey"]
                    }],
                    container=config["stream_input_properties"]["datasource"]["properties"]["container"],
                    path_pattern=config["stream_input_properties"]["datasource"]["properties"]["pathPattern"],
                    date_format=config["stream_input_properties"]["datasource"]["properties"]["dateFormat"],
                    time_format=config["stream_input_properties"]["datasource"]["properties"]["timeFormat"]
                ),
                "serialization": JsonSerialization(
                    encoding=config["stream_input_properties"]["serialization"]["properties"]["encoding"]
                )
            }
        )
        client.inputs.create_or_replace(
            resource_group_name=config["resource_group"],
            job_name=config["job_name"],
            input_name=config["input_name"],
            input=input_properties
        )
        logger.info("Input added successfully.")
    except Exception as e:
        logger.error(f"Error adding input to Stream Analytics job: {e}")
        raise

def add_output_to_job():
    try:
        logger.info("Adding output to Stream Analytics job...")
        output_properties = Output(
            properties={
                "datasource": BlobOutputDataSource(
                    storage_accounts=[{
                        "account_name": config["output_properties"]["datasource"]["storageAccounts"][0]["accountName"],
                        "account_key": config["output_properties"]["datasource"]["storageAccounts"][0]["accountKey"]
                    }],
                    container=config["output_properties"]["datasource"]["container"],
                    path_pattern=config["output_properties"]["datasource"]["pathPattern"]
                ),
                "serialization": JsonSerialization(
                    encoding=config["output_properties"]["serialization"]["encoding"]
                )
            }
        )
        client.outputs.create_or_replace(
            resource_group_name=config["resource_group"],
            job_name=config["job_name"],
            output_name=config["output_name"],
            output=output_properties
        )
        logger.info("Output added successfully.")
    except Exception as e:
        logger.error(f"Error adding output to Stream Analytics job: {e}")
        raise

if __name__ == "__main__":
    try:
        create_stream_analytics_job()
        add_input_to_job()
        add_output_to_job()
    except Exception as e:
        logger.critical(f"Failed to set up Stream Analytics job: {e}")
