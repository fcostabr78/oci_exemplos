import psutil, oci, os, time
from oci.config import validate_config
from dotenv import load_dotenv

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
local_path = '/home/fernando/Documentos/OCI/'

def convert_ratio(ratio):
	prefix = {}
	unit_prefix = ('K', 'M', 'G', 'T', 'P')
	for i, s in enumerate(unit_prefix):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(unit_prefix):
		if ratio >= prefix[s]:
			return ('%.2f %s' % ((float(ratio) / prefix[s]), s))
	return ('%.2f B' % ratio)

def print_row(bucket, fileName, download_ratio):
    print ("%-30s %-50s %-20s %-10s" % (bucket, fileName, "downloaded", download_ratio))

def create_dir(bucket_name):
	folder = '{}{}'.format(local_path, bucket_name)
	try:
		os.makedirs(folder, exist_ok=True)
	except (Exception, OSError) as exception:
		raise
	return folder

def download_file(namespace, bucket_name, file_name):
	folder = create_dir(bucket_name)
	file_path = '{}/{}'.format(folder, file_name)
	download_before = psutil.net_io_counters().bytes_recv
	file = objStgClient.get_object(namespace, bucket_name, file_name)
	with open(file_path, 'wb') as f:
		for content in file.data.raw.stream(1024 * 1024, decode_content=False):
			f.write(content)
		f.flush()
	time.sleep(1)
	download_after = psutil.net_io_counters().bytes_recv
	download_ratio = download_after - download_before
	print_row(bucket.name, o.name, convert_ratio(download_ratio))
	
validate_config(config)

objStgClient = oci.object_storage.ObjectStorageClient(config)
buckets = objStgClient.list_buckets(namespace_name=namespace, compartment_id=compartmentID).data

for bucket in buckets:
	object_list = objStgClient.list_objects(bucket.namespace, bucket.name)
	for o in object_list.data.objects:
		download_file(bucket.namespace, bucket.name, o.name)

