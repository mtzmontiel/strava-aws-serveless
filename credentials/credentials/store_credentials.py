

def write_credentials(credentials, table):
    """
    Write credentials to storage
    """
    check_keys_in_dict(credentials, ['id', 'access_token', 'refresh_token','credential_type', 'expires_at'])

    item = create_item(credentials)
    table.put_item(Item=item)
    return {
        'status':'success',
        'id': credentials['id']
    }

def create_item(credentials):
    item = {}
    item['pk']= credentials['id']
    for key in credentials: 
        if key == 'id':
            continue
        item[key] = credentials[key]
    return item

def check_keys_in_dict(dict, keys):
    """
    Check if all keys in keys are in dict
    """
    for key in keys:
        if not key in dict:
            raise ValueError('Missing key: ' + key)
    pass
