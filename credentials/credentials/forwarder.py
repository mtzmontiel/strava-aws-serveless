from store_credentials import read_athlete_credentials
import json

def forward_request(event, table, requests_client):
    credentials = read_athlete_credentials(event['athlete_id'], table)
    result = requests_client.get(event['url'], headers={'Authorization': f'Bearer {credentials["access_token"]}'})
    return json.loads(result.text)