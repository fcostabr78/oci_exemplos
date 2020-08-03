import psutil, oci, os, time
from dotenv import load_dotenv
from datetime import date, datetime
from glob import glob
from multiprocessing import Process
from oci.config import validate_config

# https://docs.python.org/3/library/multiprocessing.html
# gerar os arquivos de teste local: truncate -s 4k exemplo{1..1000}.oracle
# configurar o limite de arq aberto pelo SO: ulimit -n 6000

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
bucket = 'aLunesFiesta'

def upload_item(path):
    with open(path, "rb") as in_file:
        name = os.path.basename(path)
        objStgClient = oci.object_storage.ObjectStorageClient(config)
        objStgClient.put_object(namespace, bucket, name, in_file)

validate_config(config)
files = []

print('Inicio do Upload: {}'.format(datetime.now()))
for file_path in glob(local_path):
    p = Process(target=upload_item, args=(file_path,))
    p.start()
    files.append(p)
    
for file in files:
    file.join()

print('Total de Arquivos: {}'.format(len(files)))
print('Fim do Upload: {}'.format(datetime.now()))