import json
import urllib.request

# 🔹 Databricks API Configuration
DATABRICKS_URL = "https://dbc-aafcd4c0-2b0c.cloud.databricks.com/api/2.0/jobs/run-now"  # Replace with your instance
DATABRICKS_TOKEN = "dapif48cbf085d9a20f18aa24b6c291a1872"  # Replace with your token
DATABRICKS_JOB_ID = "799339525905177"  # Replace with your Job ID

def lambda_handler(event, context):
    """Triggered when new data is inserted into DynamoDB. Sends transaction data to Databricks."""

    transactions = []

    for record in event['Records']:
        if record['eventName'] == 'INSERT':  # Only process new records
            new_image = record['dynamodb']['NewImage']
            #print("New Image:", json.dumps(new_image, indent=2))

            # Extract transaction fields and convert to correct data types
            transaction = {
                "TransactionID": int(new_image['TransactionID']['S']),  # int32
                "isFraud": int(new_image['isFraud']['N']),  # int64
                "TransactionAmt": float(new_image['TransactionAmt']['N']),  # float64
                "card1": int(new_image.get('card1', {}).get('N', 0)),  # int32, default to 0 if missing
                "addr1": float(new_image.get('addr1', {}).get('N', 'nan')),  # float64, default to NaN
                "D1n": float(new_image.get('D1n', {}).get('N', 'nan')),  # float64, default to NaN
                "D3n": float(new_image.get('D3n', {}).get('N', 'nan')),  # float64, default to NaN
                "dist1": float(new_image.get('dist1', {}).get('N', 'nan')),  # float64, default to NaN
                "email_encoded": float(new_image.get('email_encoded', {}).get('N', 'nan')),  # float64
            }
            transactions.append(transaction) 

            #print(type(transactions.append(transaction["TransactionID"])))
            #print(type())

    # If no transactions, exit
    if not transactions:
        return {"message": "No new transactions to process"}

    # 🔹 Prepare Data for Databricks API
    payload = json.dumps({
        "job_id": DATABRICKS_JOB_ID,
        "notebook_params": {"json_data": json.dumps(transactions)}
    }).encode('utf-8')  # Convert JSON to bytes

    # 🔹 Set Headers
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    # 🔹 Create HTTP Request
    request = urllib.request.Request(DATABRICKS_URL, data=payload, headers=headers, method="POST")

    # 🔹 Send Request & Get Response
    try:
        with urllib.request.urlopen(request) as response:
            response_data = response.read().decode("utf-8")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Data sent to Databricks", "response": json.loads(response_data)})
            }
    except urllib.error.HTTPError as e:
        return {
            "statusCode": e.code,
            "body": json.dumps({"error": e.reason, "response": e.read().decode("utf-8")})
        }
    except urllib.error.URLError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to connect to Databricks", "reason": str(e)})
        }