import os, oci
from oci.config import validate_config
from dotenv import load_dotenv
from base64 import b64decode, b64encode

load_dotenv()

instance_dict = {}

config = { "user": os.environ.get('authUserID'), 
"key_file": os.environ.get('ociKeyPath'), 
"fingerprint": os.environ.get('keyFingerPrint'), 
"tenancy": os.environ.get('tenancyID'), 
"region": "us-ashburn-1"}

streamingID = os.environ.get('streamingID')
endpoint = "https://cell-1.streaming.us-ashburn-1.oci.oraclecloud.com"

validate_config(config)

streaming = oci.streaming.StreamClient(config, endpoint)

def getMessages(streamingID):
    cursor_detail = getCursor()
    cursor = streaming.create_cursor(streamingID, cursor_detail)
    r = streaming.get_messages(streamingID, cursor.data.value)

    messages = []
    if len(r.data):
        for message in r.data:
            messages.append(b64decode(message.value).decode('utf-8'))
    return messages

def getCursor():
    cursor = oci.streaming.models.CreateCursorDetails()
    cursor.partition = "0"
    cursor.type = "TRIM_HORIZON"
    return cursor
    
print(getMessages(streamingID))
