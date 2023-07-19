

def write_credentials(credentials, table):
    """
    Write credentials to storage
    """
    check_keys_in_dict(credentials, ['id', 'access_token', 'refresh_token','credential_type', 'expires_at'])
    table.put_item(Item=credentials)
    return {
        'status':'success',
        'id': credentials['id']
    }

def check_keys_in_dict(dict, keys):
    """
    Check if all keys in keys are in dict
    """
    for key in keys:
        if not key in dict:
            raise ValueError('Missing key: ' + key)
    pass
