# lambda handler that takes code from event and retrieves values 'CLIENT_ID' and 'CLIENT_SECRET' from parameter store
# 
import boto3
import json

application = os.environ['APPLICATION']
table = create_table(table_name=os.environ['TABLE_NAME'],key_id=os.environ['KEY_ID'])

def lambda_handler(event, context):
    authorization_code = event['queryStringParameters']['code']
    client_id = get_parameter_store_value(application+ '/CLIENT_ID')
    client_secret = get_parameter_store_value(application + '/CLIENT_SECRET')
    response = requests.post('https://www.strava.com/oauth/token', data={
        auth_code: authorization_code,
        client_id: client_id,
        client_secret: client_secret
    })
    # if not http 200, return error
    if response.status_code != 200:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    json_response = response.json()
    write_credentials({
            'athlete_id': json_response['athlete']['id'],
            'access_token': json()['access_token'],
            'refresh_token': json_response['refresh_token'],
            'expires_at': json_response['expires_at'],
            'expires_in': json_response['expires_in'],
            'credential_type': 'athlete',
            
        }, table)


def get_parameter_store_value(parameter_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']   