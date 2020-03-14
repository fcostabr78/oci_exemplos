import os, oci, shapes, requests, random, string
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
network = oci.core.VirtualNetworkClient(config)

instance_list = compute.list_instances(compartmentId)
instances = instance_list.data

def randomString(len=6):
    rand_data = string.ascii_lowercase
    return ''.join(random.choice(rand_data) for i in range(len))

def get_operation_system(instance):
    response = compute.get_image(instance.source_details.image_id)
    imagedetails = response.data
    return imagedetails.display_name

def get_public_ips(instance):
    public_ips = ""
    response = compute.list_vnic_attachments(compartment_id = instance.compartment_id, instance_id = instance.id)
    vnics = response.data
    for vnic in vnics:
        responsenic = network.get_vnic(vnic.vnic_id)
        nicinfo = responsenic.data
        public_ips = public_ips + nicinfo.public_ip + " "
    return public_ips

def send_data(instance):
    data = {
        "name": instance.display_name, 
        "shape": instance.shape, 
        "region": instance.region, 
        "life_cycle": instance.lifecycle_state,
        "snapshot": randomString(),
        "ociID": instance.id,
        "ip": get_public_ips(instance),
        "so": get_operation_system(instance)
    }
    requests.post(url = os.environ.get('url_post_instance'), data = data) 

for idx, instance in enumerate(instances):
	send_data(instance)
