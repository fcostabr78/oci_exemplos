import os, oci
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

def start_instance(ociID):
	compute.instance_action(ociID, "START")

def print_row(id, instance_name, status, shape, region):
    print " %-10s %-40s %30s %20s %20s" % (id, instance_name, shape, status, region)

def request_instance():
	try:
		instance_id = raw_input('\nDigite o ID da instancia/shape que deseja parar:')
		item = float(instance_id)
		print ("A instancia de OCID {} sera iniciada....aguarde".format(instance_dict[item]))
		start_instance(instance_dict[item])
	except KeyboardInterrupt:
		print('\nPrograma abortado\n')
	except ValueError:
		print('\nO valor ingressado esta incorreto\n')
	except Exception as exception:
		print('\nOcorreu um erro: {}'.format(exception))

compartmentId = os.environ.get('compartmentID')
validate_config(config)

compute = oci.core.ComputeClient(config)
instance_list = compute.list_instances(compartmentId, lifecycle_state = "STOPPED")
instances = instance_list.data

print("\ntotal de instancias em seu compartimento que estao parados: {}\n".format(len(instances)))

for idx, instance in enumerate(instances):
	instance_dict[idx] = instance.id
	print_row(idx, instance.display_name, instance.lifecycle_state,	instance.shape,	instance.region)

if (len(instances) > 0):
	request_instance()