import argparse
import sys
import time
from typing import List
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError
from googleapiclient import discovery

"""create_gcloud_vm script

Script for trying to start a Google cloud GPU VM in multiple zones with
default settings for the course.

Developed for the deep machine learning course at Chalmers University of
Technolgy, 2025, released under the MIT license, see
https://github.com/dml-cth/deep-machine-learning/blob/master/LICENSE

DISCLAIMER: Note that any VM that you start with this script WILL INCUR COST
TOWARDS YOUR CREDITS until stopped in the cloud console. This scrips has quite
poor error checking etc. After running, always check if a VM is running in the
web console to keep on top of your credits.

Before running, you need to set credentials for your google cloud account.
- Install the gcloud CLI according to https://cloud.google.com/sdk/docs/install-sdk
- Run 'gcloud auth application-default login' from a command window. This
  will open a browser window where you proceed with the authentication.
- Select your google account, check the boxes and click "Continue"   
- You should then be redirected to a page saying that you're authenticated.

Usage example:
  python3 create_gcloud_vm.py yourproject-1234 L4 lab-vm-1

This will attempt to create a VM called lab-vm-1 with an L4 GPU in the project
with ID yourproject-1234.
"""


def list_zones_with_gpu(
        compute: Resource, 
        project: str, 
        gpu_type: str) -> List[str]:
    """List all zones that supports the specified GPU type.

    A bit slow, so for day-to-day use, we recommend using a pre-fetched list 
    (see get_gpu_zones_prefetched).
    
    Args:
        compute: Resource object for interacting with the gcloud compute API.
        project: Project ID (note: NOT project display name, must be full ID).
        gpu_type: Type of GPU to use, e.g. "nvidia-tesla-t4".
    
    Returns:
        List of zones (zone names) that support GPUs of the specified type.
    """

    print("Listing zones with GPU support...")
    zones_request = compute.zones().list(project=project)
    zones = []

    print(f'Zones with support for {gpu_type}: ')
    while zones_request is not None:
        response = zones_request.execute()
        for zone in response.get('items', []):
            zone_name = zone['name']
            try:
                # List available accelerator types in the zone
                accelerator_request = compute.acceleratorTypes().list(project=project, zone=zone_name)
                accelerator_response = accelerator_request.execute()
                accelerator_types = [acc['name'] for acc in accelerator_response.get('items', [])]

                if gpu_type in accelerator_types:
                    zones.append(zone_name)
                    print(f"{zone_name}, ")

            except HttpError as e:
                # Sometimes some zones may be restricted or unavailable, just skip those
                print(f"Skipping zone {zone_name} due to error: {e}")
        zones_request = compute.zones().list_next(previous_request=zones_request, previous_response=response)
    return zones


def get_gpu_zones_prefetched(
        compute: Resource, 
        project: str, 
        gpu_type: str) -> List[str]:
    """Return zones with support for a few selected GPU types.

    Using pre-fetched hard-coded data when available, for speed. Last updated
    Sept 2025. Produced by manually calling list_zones_with_gpu above + manual
    copy-pasting.

    Args:
        compute: Resource object for interacting with the gcloud compute API.
        project: Project ID (note: NOT project display name, must be full ID).
        gpu_type: Type of GPU to use, e.g. "nvidia-tesla-t4"
    """

    # Commented out since we don't currently support P4s (broken drivers on
    # google's imageS)
    # 
    # if gpu_type == 'nvidia-tesla-p4':
    #     return [
    #         'europe-west4-b', 'europe-west4-c', 
    #         'asia-southeast1-b', 'asia-southeast1-c', 'australia-southeast1-b', 
    #         'northamerica-northeast1-a', 'northamerica-northeast1-b', 'northamerica-northeast1-c',
    #         'us-east4-c', 'us-east4-b', 'us-east4-a',
    #         'us-central1-c', 'us-central1-a',
    #         'us-west2-b', 'us-west2-c'
    #         'australia-southeast1-a',
    #      ]

    if gpu_type == 'nvidia-l4': 
        return ['europe-west4-a', 'europe-west4-b', 'europe-west4-c', 'europe-west1-b', 
         'europe-west1-c', 'europe-west3-a', 'europe-west3-b', 'europe-west2-b', 
         'europe-west2-a', 'europe-west6-b', 'europe-west6-c', 
         'us-east1-b', 'us-east1-c', 'us-east1-d', 'us-east4-c', 'us-east4-a', 
         'me-central2-a', 'me-central2-c', 
         'us-central1-c', 'us-central1-a', 'us-central1-b', 
         'us-west1-b', 'us-west1-c', 'us-west1-a', 'us-west4-a', 'us-west4-c', 
         'asia-southeast1-b', 'asia-southeast1-a', 'asia-southeast1-c', 'asia-northeast1-b', 
         'asia-northeast1-c', 'asia-northeast1-a', 
         'asia-east1-b', 'asia-east1-a, asia-east1-c', 
         'asia-south1-c', 'asia-south1-b, asia-south1-a', 
         'asia-northeast3-a', 'asia-northeast3-b', 
         'northamerica-northeast1-b', 'northamerica-northeast2-a', 'northamerica-northeast2-b']

    elif gpu_type == 'nvidia-tesla-t4': 
        return [
            'europe-west4-a', 'europe-west4-b', 'europe-west4-c',
            'europe-west1-b', 'europe-west1-d', 'europe-west1-c',
            'europe-west3-b', 'europe-west3-b', 
            'europe-west2-b', 'europe-west2-a',
            'europe-central2-b', 'europe-central2-c',
            'me-west1-b', 'me-west1-c',
            'us-east1-c', 'us-east1-d', 'us-east4-c', 'us-east4-b', 'us-east4-a',
            'us-central1-c', 'us-central1-a', 'us-central1-f', 'us-central1-b',
            'us-west1-b', 'us-west1-a',
            'us-west2-b', 'us-west2-c', 'us-west3-b', 'us-west4-a', 'us-west4-b',
            'asia-east1-a', 'asia-east1-c',
            'asia-east2-a', 'asia-east2-c',
            'asia-southeast1-b', 'asia-southeast1-a', 'asia-southeast1-c', 'asia-northeast1-c',
            'asia-northeast1-a',
            'asia-south1-b', 'asia-south1-a',
            'australia-southeast1-c', 'australia-southeast1-a',
            'southamerica-east1-c', 'southamerica-east1-a',
            'asia-northeast3-b', 'asia-northeast3-c',
            'asia-southeast2-a', 'asia-southeast2-b',
            'northamerica-northeast1-c']

    else:
        return list_zones_with_gpu(compute, project, gpu_type)


def create_instance(
        compute: Resource,
        project: str,
        zone: str,
        gpu_type: str,
        instance_name: str) -> dict:
    """Try to create an instance in the given zone.

    Args:
        compute: Resource object for interacting with the gcloud compute API.
        project: Project ID (note: NOT project display name, must be full ID)
        zone: zone id, e.g. "europe-west4-a"
        gpu_type: Type of GPU to use, e.g. "nvidia-tesla-t4"
        instance_name: Your name of the new instance, e.g. "lab-vm-1"

    Returns:
        Request response, can be used in subsequent wait_for_operation calls.
    """

    print(f"Trying to create instance in zone: {zone}")

    # Select machine type depending on GPU (different machines are used for different GPUs)
    if gpu_type == 'nvidia-tesla-t4': 
        machine_type = 'n1-standard-4'
    elif gpu_type == 'nvidia-l4':
        machine_type = 'g2-standard-4'
    else:
        print('WARNING: Not a standard GPU type for the course. Defaulting to machine type n1-standard-4. This may or may not work.')
        machine_type = 'n1-standard-4'

    # The T4s and L4s are tested to work with this image. The P4 drivers are broken
    # for this image. This can likely be fixed, but is not trivial. If you want to do
    # this, you're on your own. Other GPU types are untested (by us), so may or may 
    # not work.
    source_image = "projects/ubuntu-os-accelerator-images/global/images/ubuntu-accelerator-2404-amd64-with-nvidia-570-v20250819"

    # Get region from zone
    region = "-".join(zone.split("-")[:2])

    config = {
    "canIpForward": False,
    "confidentialInstanceConfig": {
        "enableConfidentialCompute": False
    },
    "deletionProtection": False,
    "description": "",
    "disks": [{
        "autoDelete": True,
        "boot": True,
        "deviceName": instance_name,
        "initializeParams": {
            "diskSizeGb": "50",
            "diskType": f"projects/{project}/zones/{zone}/diskTypes/pd-balanced",
            "sourceImage": source_image
        },
        "mode": "READ_WRITE",
        "type": "PERSISTENT"
    }],
    "displayDevice": {
        "enableDisplay": False
    },
    "guestAccelerators": [{
        "acceleratorCount": 1,
        "acceleratorType": f"projects/{project}/zones/{zone}/acceleratorTypes/{gpu_type}"
    }],
    "labels": {
        "goog-ops-agent-policy": "v2-x86-template-1-4-0",
        "goog-ec-src": "vm_add-rest"
    },
    "machineType": f"projects/{project}/zones/{zone}/machineTypes/{machine_type}",
    "metadata": {
        "items": [{
            "key": "enable-osconfig",
            "value": "TRUE"
        }]
    },
    "name": instance_name,
    "networkInterfaces": [{
        "accessConfigs": [{
            "name": "External NAT",
            "networkTier": "PREMIUM"
        }],
        "stackType": "IPV4_ONLY",
        "subnetwork": f"projects/{project}/regions/{region}/subnetworks/default"
    }],
    "reservationAffinity": {
        "consumeReservationType": "ANY_RESERVATION"
    },
    "scheduling": {
        "automaticRestart": True,
        "onHostMaintenance": "TERMINATE",
        "provisioningModel": "STANDARD"
    },
    "serviceAccounts": [{
        "email": "default",
        "scopes": [
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring.write",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/trace.append"
        ]
    }],
    "shieldedInstanceConfig": {
        "enableIntegrityMonitoring": True,
        "enableSecureBoot": False,
        "enableVtpm": True
    },
    "zone": zone
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


def wait_for_operation(
        compute: Resource, 
        project: str, 
        zone: str, 
        operation: str) -> None:
    """Wait until 'operation' is finished
    """

    # print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if 'error' in result:
            raise Exception(result['error'])

        if result['status'] == 'DONE':
            # print("Operation complete.")0
            return

        time.sleep(5)


def create_vm_multizone(
    project: str,
    gpu_type: str,
    instance_name: str) -> None:
    """Repeatedly attempt to create a VM in all zones supporting the desired
    GPU type until successful (or until all zones have been exhausted).
    """

    compute = discovery.build('compute', 'v1')

    # Get all zones (pre-fetched if available, for speed)
    zones_with_gpu = get_gpu_zones_prefetched(compute, project, gpu_type)

    # For debugging, try e.g.
    # zones_with_gpu = ['europe-central2-b', 'asia-southeast1-a']

    if not zones_with_gpu:
        print(f"ERROR: No zones found with GPU type {gpu_type}.")
        return

    for zone in zones_with_gpu:
        try:
            operation = create_instance(compute, project, zone, gpu_type, instance_name)
            wait_for_operation(compute, project, zone, operation['name'])
            print(f"Instance successfully created in {zone}")
            break

        except HttpError as e:
            reason = e.error_details[0]['reason']
            if reason == 'alreadyExists':
                print("ERROR: A VM with this name already exists. Please check the web console.")
                break
            elif reason == 'notFound':
                print("ERROR: The specified project was not found")
                break
            elif reason == 'accessNotConfigured':
                print((
                    "ERROR: Project access issue. Make sure that the Compute API is enabled. "
                    "Also make sure that you're referring to the project using the project ID, "
                    "not the project name. Should be something like yourproject-12345"))
                break
            else:
                print(f"ERROR: Unexpected error: {e.reason}.")
                break

        except Exception as e:
            code = e.args[0]['errors'][0]['code']
            if code == 'ZONE_RESOURCE_POOL_EXHAUSTED':
                print('No machine of the specified type available in this zone')
                # Keep going - this is the only error that doesn't break the entore loop
            else:
                msg = e.args[0]['errors'][0]['message']
                print(f"ERROR: Unexpected error: {msg}")
                break

    else:
        print("Failed to create instance in all zones.")

# ----------------------------------------------------------------------------
# Lab code

def lab_multizone_vm():
    """For manual experimentation, e.g. within an IDE
    """

    project_id = 'YOUR PROJECT ID HERE'
    gpu_type = 'nvidia-tesla-t4'
    instance_name = 'lab-vm-1'

    create_vm_multizone(project_id, gpu_type, instance_name)


# ----------------------------------------------------------------------------
# Command-line interface

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = (
        """Simple tool for attempting to start a GPU-equipped google cloud VM in
           multiple zones until successful. Developed for the deep maching learning course
           at Chalmers University of Technology. NOTE THAT ANY VM STARTED WITH THIS
           SCRIPT WILL INCUR COST TOWARDS YOUR CREDITS until stopped in the cloud
           console. Please see the source code and cloud setup instructions for more
           info."""))

    parser.add_argument("project", type=str, help="Your project ID (note: NOT project display name - the ID usually also contains some numbers)")
    parser.add_argument("gpu", type=str, help="GPU type, L4 or T4. These are the options supported by the teaching staff.")
    parser.add_argument("name", type=str, help="VM instance name, free to choose, e.g. lab-vm-1")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Short-hand for common GPU types:
    gpu_lower = args.gpu.lower()
    if  gpu_lower == 'l4':
        expanded_gpu = 'nvidia-l4'
    elif gpu_lower == 't4':
        expanded_gpu = 'nvidia-tesla-t4'
    else:
        print(("ERROR: Unsupported GPU type (by the course). If you want to experiment with other "
               "GPU types, you need to create a VM manually or modify this script. You're welcome "
               "to try, but the teaching staff will only support the L4 and T4 options."))
        sys.exit(1)

    print(f'Selected GPU: {expanded_gpu}')

    try:
        create_vm_multizone(args.project, expanded_gpu, args.name)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        
