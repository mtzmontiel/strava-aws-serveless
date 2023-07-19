import boto3
from dynamodb_encryption_sdk.material_providers import CryptographicMaterialsProvider
from dynamodb_encryption_sdk.encrypted.table import EncryptedTable
from dynamodb_encryption_sdk.structures import AttributeActions
from dynamodb_encryption_sdk.identifiers import CryptoAction
from dynamodb_encryption_sdk.material_providers.aws_kms import AwsKmsCryptographicMaterialsProvider



def create_materials_provider(key_id):
    return AwsKmsCryptographicMaterialsProvider(key_id)

def create_encrypted_table(table_name, materials_provider):
    table = boto3.resource('dynamodb').Table(table_name)
    attribute_actions = AttributeActions(
        default_action=CryptoAction.ENCRYPT_AND_SIGN,
        attribute_actions={
            'expires_at': CryptoAction.DO_NOTHING,
            'credential_type': CryptoAction.DO_NOTHING,
            'updated_at': CryptoAction.DO_NOTHING
        }
    )
    return EncryptedTable(table, materials_provider, attribute_actions=attribute_actions)

def create_table(table_name, key_id):
    materials_provider = create_materials_provider(key_id)
    return create_encrypted_table(table_name, materials_provider)