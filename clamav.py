import os, oci, subprocess
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

def readMessages(streamingID):
    cursor_detail = getCursor()
    cursor = streaming.create_cursor(streamingID, cursor_detail)
    r = streaming.get_messages(streamingID, cursor.data.value)

    if len(r.data):
        for message in r.data:
            file = b64decode(message.value).decode('utf-8')
            execClamAV(file)

def getCursor():
    cursor = oci.streaming.models.CreateCursorDetails()
    cursor.partition = "0"
    cursor.type = "TRIM_HORIZON" #consume all messages in a stream
    return cursor

def decodeByte(data, code='UTF-8'):
    return bytes(data).decode(code)

def execClamAV(file):
    print("Checando arquivo %s" %file)
    command = "curl '{}' | clamdscan -".format(file)
    process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for line in decodeByte(process.communicate()[0]).split("\n"):
        if "Infected files: 1" in line:
            print('Arquivo Contaminado!')
        elif "Infected files: 0" in line:
            print('Arquivo nao contaminado')

readMessages(streamingID)
