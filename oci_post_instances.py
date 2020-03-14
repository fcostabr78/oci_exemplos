import os, oci, requests 
from oci.config import validate_config
from dotenv import load_dotenv
load_dotenv()

instance_dict = {}

config = { 
    "user": os.environ.get('authUserID'), 
    "key_file": os.environ.get('ociKeyPath'), 
    "fingerprint": os.environ.get('keyFingerPrint'), 
    "tenancy": os.environ.get('tenancyID'), 
    "region": "us-ashburn-1"
}

compartmentId = os.environ.get('compartmentID')
validate_config(config)

compute = oci.core.ComputeClient(config)
instance_list = compute.list_instances(compartmentId)
instances = instance_list.data

def send_data(instance):
    data = {
        "name": instance.display_name, 
        "shape": instance.shape, 
        "region": instance.region, 
        "life_cycle": instance.lifecycle_state,
        "ociID": instance.id
    } 
    requests.post(url = os.environ.get('url_post_instance'), data = data) 

for idx, instance in enumerate(instances):
	send_data(instance)
