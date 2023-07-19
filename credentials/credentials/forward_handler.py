import json
import os
import requests
from ddb import create_table
from forwarder import forward_request

table = create_table(table_name=os.environ['TABLE_NAME'],key_id=os.environ['KEY_ID'])
requests_client = requests

def lambda_handler(event, context):
    try:
        result = forward_request(event, table, requests_client)       
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        print('Error forwarding requests: {}'.format(e), e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

