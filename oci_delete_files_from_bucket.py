import os
import oci
import subprocess
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

prefix = [
    'apps.v1',
    'com.oraclecloud', 
    'core.v1',
    'oci-logs', 
    'io.k8s',
    'batch.v1beta1',
    'batch.v1',
    'autoscaling.v1',
    ]

def delete_bucket(namespace, bucket_name):
    objStgClient.delete_bucket(namespace, bucket_name)

def delete_all_files(bucket_name):
    print("\nExcluir Arquivos do Bucket: {}".format(bucket_name))
    subprocess.run(["oci", "os", "object", "bulk-delete", "-bn", bucket_name])

namespace = os.environ.get('namespace')
compartmentID = os.environ.get('compartmentID')

validate_config(config)

objStgClient = oci.object_storage.ObjectStorageClient(config)

buckets = objStgClient.list_buckets(
    namespace_name=namespace, compartment_id=compartmentID).data

for bucket in buckets:
    object_list = objStgClient.list_objects(bucket.namespace, bucket.name)
    if any(ext in bucket.name for ext in prefix):
        if (len(object_list.data.objects) == 0):
            print("\nExcluir Bucket: {}".format(bucket.name))
            delete_bucket(bucket.namespace, bucket.name)
        else:
            delete_all_files(bucket.name)