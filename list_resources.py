from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient

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
