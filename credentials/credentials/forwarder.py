
import json

def forward_request(event, credentials,requests_client):
    validate_request(event)
    url = create_url(event)
    headers= create_headers(credentials)
    result = requests_client.get(url, headers=headers)
    print(str(result))
    print(str(result.text))
    return json.loads(result.text)

def validate_request(event):
    if 'request_type' not in event:
        raise Exception('request_type is missing')
    
def create_url(event):
    return f'https://www.strava.com/api/v3/{event["request_type"]}'

def create_headers(credentials):
    return {
        'Authorization': f'Bearer {credentials["access_token"]}'
    }