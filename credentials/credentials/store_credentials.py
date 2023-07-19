import datetime

def write_credentials(credentials, table):
    """
    Write credentials to storage
    """
    check_keys_in_dict(credentials, ['id','credential_type'])
    check_value_in_set(credentials['credential_type'], ['athlete','application'])
    if credentials['credential_type'] == 'athlete':        
        check_keys_in_dict(credentials, ['access_token', 'refresh_token', 'expires_at'])
    elif credentials['credential_type'] == 'application':
        check_keys_in_dict(credentials, ['application_id', 'application_secret'])
    item = create_item(credentials)
    table.put_item(Item=item)
    return {
        'status':'success',
        'id': credentials['id']
    }

def create_item(credentials):
    item = {}
    item['pk']= f'{credentials["credential_type"]}#{credentials["id"]}'
    item['updated_at'] = datetime.datetime.now().isoformat()'
    for key in credentials: 
        if key == 'id':
            continue
        item[key] = credentials[key]
    return item


def check_value_in_set(value, set):
    for valid_value in set:
        if value == valid_value:
            return
    raise ValueError(f'Value not valid: {value}')

    

def check_keys_in_dict(dict, keys):
    """
    Check if all keys in keys are in dict
    """
    for key in keys:
        if not key in dict:
            raise ValueError(f'Missing key: {key}')
    pass
