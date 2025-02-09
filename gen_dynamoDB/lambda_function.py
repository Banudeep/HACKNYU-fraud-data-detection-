import json
import boto3
import os
from datetime import datetime
from decimal import Decimal
import numpy as np
import pandas as pd

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
table_name = os.environ.get("DYNAMODB_TABLE", "gen_data")
print("Table Name:", table_name)
table = dynamodb.Table(table_name)

# Define config table name (which has only ONE column: last_TransactionID)
config_table_name = "ConfigTable"  # Ensure this is the correct table name
config_table = dynamodb.Table(config_table_name)

def get_last_transaction_id():
    """Fetches last transaction ID from ConfigTable (Only ONE column exists)."""
    try:
        response = config_table.scan()  # Scan because there's only one row
        print("Response from DynamoDB:", response)
        
        if 'Items' in response and len(response['Items']) > 0:
            return int(response['Items'][0]['last_TransactionID'])  # Convert string to int
        else:
            print("No last_TransactionID found. Initializing to 0.")
            store_last_transaction_id(0)  # Initialize if not present
            return 0
    except Exception as e:
        print(f"Error retrieving last_TransactionID: {str(e)}")
        return 0

def generate_data(num_samples=10):
    """Generates synthetic transaction data"""
    last_ID = get_last_transaction_id()  # Fetch last transaction ID

    # Generate synthetic data
    transaction_ids = np.arange(last_ID + 1, num_samples + last_ID + 1)
    transaction_amounts = np.abs(np.random.normal(loc=100, scale=50, size=num_samples))
    card1 = np.random.randint(1000, 9999, size=num_samples)
    addr1 = np.random.randint(1, 500, size=num_samples)
    d1n = np.random.randint(-500, 500, size=num_samples)
    d3n = np.random.randint(-500, 500, size=num_samples)
    dist1 = np.random.randint(0, 1000, size=num_samples)
    email_encoded = np.random.randint(1, 100, size=num_samples)

    df = pd.DataFrame({
        'TransactionID': transaction_ids,
        'TransactionAmt': transaction_amounts,
        'card1': card1,
        'addr1': addr1,
        'D1n': d1n,
        'D3n': d3n,
        'dist1': dist1,
        'email_encoded': email_encoded
    })

    return df

def lambda_handler(event, context):
    num_samples = 10
    stratified_sample = generate_data(num_samples)

    # Write to DynamoDB
    batch_write_dynamodb(stratified_sample)

    # Update last transaction ID in ConfigTable
    new_last_id = stratified_sample["TransactionID"].max()
    store_last_transaction_id(new_last_id)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully added {len(stratified_sample)} transactions! Last ID: {new_last_id}')
    }

def batch_write_dynamodb(df):
    """Writes multiple records to DynamoDB in batches"""
    try:
        with table.batch_writer() as batch:
            for _, row in df.iterrows():
                batch.put_item(
                    Item={
                        'TransactionID': int(row['TransactionID']),
                        'TransactionAmt': Decimal(str(row['TransactionAmt'])),
                        'card1': int(row['card1']),
                        'addr1': int(row['addr1']),
                        'D1n': int(row['D1n']),
                        'D3n': int(row['D3n']),
                        'dist1': int(row['dist1']),
                        'email_encoded': int(row['email_encoded']),
                        'CreatedAt': datetime.utcnow().isoformat()
                    }
                )
        print("Batch write successful!")
    except Exception as e:
        print(f"Batch write error: {str(e)}")

def store_last_transaction_id(new_last_id):
    try:
        response = config_table.scan()  # Fetch all records

        if 'Items' in response and len(response['Items']) > 0:
            for item in response['Items']:
                config_table.delete_item(Key={'last_TransactionID': item['last_TransactionID']})
                print(f"Deleted last_TransactionID: {item['last_TransactionID']}")
            print("All last_TransactionID records deleted successfully.")
        else:
            print("No last_TransactionID records found to delete.")
    except Exception as e:
        print(f"Error deleting last_TransactionID records: {str(e)}")
    """Replaces the existing row in ConfigTable with the new last_TransactionID."""
    try:
        config_table.put_item(
            Item={
                'last_TransactionID': str(new_last_id)  # Overwriting the existing row
            }
        )
        print(f"Updated last_TransactionID to {new_last_id}")
    except Exception as e:
        print(f"Error storing last_TransactionID: {str(e)}")
