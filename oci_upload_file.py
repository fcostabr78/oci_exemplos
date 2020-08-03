import psutil, oci, os, time
from oci.config import validate_config
from dotenv import load_dotenv
from multiprocessing import Process
from glob import glob

load_dotenv()

config = {
    "user": os.environ.get('authUserID'),
    "key_file": os.environ.get('ociKeyPath'),
    "fingerprint": os.environ.get('keyFingerPrint'),
    "tenancy": os.environ.get('tenancyID'),
    "region": "us-ashburn-1"
    }

namespace = os.environ.get('namespace')
compartmentID = os.environ.get('compartmentID')
local_path = '/home/fernando/Documentos/uploads/*.*'
bucket = 'bucketLunes'

def upload_item(path):
    with open(path, "rb") as in_file:
        name = os.path.basename(path)
        objStgClient = oci.object_storage.ObjectStorageClient(config)
        objStgClient.put_object(namespace, bucket, name, in_file)
        print("Upload de {} concluido com sucesso".format(name))

validate_config(config)
files = []

for file_path in glob(local_path):
    print("Starting upload for {}".format(file_path))
    p = Process(target=upload_item, args=(file_path,))
    p.start()
    files.append(p)
    
for file in files:
    file.join()