import json
import os
import requests
from ddb import create_table
from credentials import forward_request
from store_credentials import read_athlete_credentials

table = create_table(table_name=os.environ['TABLE_NAME'],key_id=os.environ['KEY_ID'])
requests_client = requests

def lambda_handler(event, context):
    try:
        credentials = read_athlete_credentials(event['athlete_id'], table)
        result = forward_request(event, credentials, requests_client)       
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

