import json
import os

from ddb import create_table
from store_credentials import write_credentials

table = create_table(table_name=os.environ['TABLE_NAME'],key_id=os.environ['KEY_ID'])

def lambda_handler(event, context):
    try:
        result = write_credentials(event, table)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        print('Error writing credentials to DDB: {}'.format(e), e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
