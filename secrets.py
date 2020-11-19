import argparse, os, oci 
from base64 import b64decode, b64encode
from dotenv import load_dotenv
from oci.config import validate_config
from oci.vault.models import Base64SecretContentDetails, CreateSecretDetails, Secret, SecretContentDetails
from oci.vault import VaultsClient, VaultsClientCompositeOperations
load_dotenv()

config = { "user": os.environ.get('authUserID'), 
"key_file": os.environ.get('ociKeyPath'), 
"fingerprint": os.environ.get('keyFingerPrint'), 
"tenancy": os.environ.get('tenancyID'), 
"region": "us-ashburn-1"}

validate_config(config)
client = oci.secrets.SecretsClient(config)
CONTENT_TYPE_BASE64 = SecretContentDetails.CONTENT_TYPE_BASE64

def get_secret_data(secret_client, secret_id):
    response = secret_client.get_secret_bundle(secret_id)
    return response.data.secret_bundle_content.content

def get_content(data):
    message = b64decode(data.encode('ascii'))
    return message.decode('ascii')

def create_content_detail(content):
    data = b64encode(content.encode('ascii'))
    base64_data = data.decode('ascii')
    return Base64SecretContentDetails(content_type = CONTENT_TYPE_BASE64, content = base64_data, stage = "CURRENT")

def create_secret(name, content, description):
    details = CreateSecretDetails(compartment_id = os.environ.get('compartmentID'), 
    description = description, 
    secret_content = (create_content_detail(content)), 
    secret_name = name, 
    vault_id = os.environ.get('vaultID'), 
    key_id = os.environ.get('keyID'))
    client_composite = VaultsClientCompositeOperations(VaultsClient(config))
    return client_composite.create_secret_and_wait_for_state(create_secret_details = details,  wait_for_states=[Secret.LIFECYCLE_STATE_ACTIVE])


data = argparse.ArgumentParser()
data.add_argument('--secretID')
data.add_argument('--secretName')
data.add_argument('--secretContent')
args = data.parse_args()

secretID = args.secretID
secretName = args.secretName
secretContent = args.secretContent


if (args.secretID is not None):
    resp = get_secret_data(client, secretID)
    print(get_content(resp))
elif (args.secretName is not None and args.secretContent is not None):
    create_secret(secretName, secretContent, 'criado em demo')
else:
    print('Nao foi informado parametros nem para consulta nem para criacao de secret')







