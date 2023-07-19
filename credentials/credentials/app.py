import json
import os

from ddb import create_table
from store_credentials import write_credentials

def lambda_handler(event, context):
    table = create_table(table_name=os.environ['TABLE_NAME'],key_id=os.environ['KEY_ID'])
    try:
        result = write_credentials(event, table)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
