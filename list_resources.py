import os
from azure.identity import DefaultAzureCredential, AzureError
from azure.mgmt.resource import SubscriptionClient
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError

def list_subscriptions():
    try:
        # Authenticate using the default Azure credentials
        credential = DefaultAzureCredential()

        # Initialize the SubscriptionClient
        subscription_client = SubscriptionClient(credential)

        # List all subscriptions
        subscriptions = list(subscription_client.subscriptions.list())

        # Check if the subscriptions list is populated
        if subscriptions:
            for subscription in subscriptions:
                print(f"Subscription ID: {subscription.subscription_id}")
                print(f"Subscription Display Name: {subscription.display_name}")
                print(f"Subscription State: {subscription.state}")
                print("-" * 30)
        else:
            print("No subscriptions found.")
    except ClientAuthenticationError as auth_err:
        print(f"Authentication error: {auth_err}")
    except HttpResponseError as http_err:
        print(f"HTTP error: {http_err}")
    except AzureError as azure_err:
        print(f"Azure error: {azure_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Ensure environment variables are set
    required_env_vars = ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID", "AZURE_SUBSCRIPTION_ID"]
    
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Environment variable {var} is not set. Please set it before running the script.")
            exit(1)
    
    list_subscriptions()
