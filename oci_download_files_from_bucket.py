import os, oci
from oci.config import validate_config
from dotenv import load_dotenv

load_dotenv()

def print_row(bucket, fileName):
    print " %-30s %-50s %-30s" % (bucket, fileName, "Downloaded")

def create_dir(folder):
	try:
		os.makedirs(folder)
	except Exception as exception:
		raise

def download_file(namespace, bucket_name, file_name):
	folder = '/home/fernando/Documentos/OCI/{}'.format(bucket_name)
	create_dir(folder)
	file_path = '{}/{}'.format(folder, file_name)
	file = objStgClient.get_object(namespace, bucket_name, file_name)
	with open(file_path, 'wb') as f:
		for chunk in file.data.raw.stream(1024 * 1024, decode_content=False):
			f.write(chunk)
	print_row(bucket.name, o.name)

config = {
    "user": os.environ.get('authUserID'),
    "key_file": os.environ.get('ociKeyPath'),
    "fingerprint": os.environ.get('keyFingerPrint'),
    "tenancy": os.environ.get('tenancyID'),
    "region": "us-ashburn-1"
    }

namespace = os.environ.get('namespace')
compartmentID = os.environ.get('compartmentID')

validate_config(config)

objStgClient = oci.object_storage.ObjectStorageClient(config)

buckets = objStgClient.list_buckets(namespace_name=namespace, compartment_id=compartmentID).data

for bucket in buckets:
	object_list = objStgClient.list_objects(bucket.namespace, bucket.name)
	for o in object_list.data.objects:
		download_file(bucket.namespace, bucket.name, o.name)

