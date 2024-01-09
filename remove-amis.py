import boto3, os, sys, argparse

def get_ami_info(response):
    output_file = 'amis_info.txt'

    with open(output_file, 'w') as file:
        for image in response['Images']:
            file.write(f"Name: {image['Name']}\n")
            file.write(f"ImageId: {image['ImageId']}\n")
            file.write(f"Architecture: {image['Architecture']}\n")
            file.write(f"Public: {image['Public']}\n")
            file.write(f"OwnerId: {image['OwnerId']}\n")
            file.write("Block Device Mappings:\n")
            for device in image.get('BlockDeviceMappings', []):
                file.write(f"  Device Name: {device['DeviceName']}\n")
                file.write(f"    Snapshot ID: {device['Ebs']['SnapshotId']}\n")
            state_tag = next((tag for tag in image.get('Tags', []) if tag['Key'] == 'State'), None)
            if state_tag:
                file.write("Tags:\n")
                file.write(f"  State: {state_tag['Value']}\n")
            file.write(f"CreationDate: {image['CreationDate']}\n")
            file.write("-----------\n")

        if not response['Images']:
            print("No AMIs found. Exiting.")
            sys.exit(0)

    print(f"AMI information written to {output_file}")
    return output_file

def find_older_amis(output_file):
    known_amis = ['ami-name1, ami-name2, ami-name3, ami-name4...']
    latest_amis = {}

    with open(output_file, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('Name:'):
                name = lines[i].split(': ')[1].split('-')[0]
                if name in known_amis:
                    creation_date = lines[i + 9].split(': ')[1].strip()
                    if name not in latest_amis or creation_date > latest_amis[name]:
                        latest_amis[name] = creation_date
            i += 1

    older_amis = {}
    for name, date in latest_amis.items():
        older_amis[name] = []

    with open(output_file, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('Name:'):
                name = lines[i].split(': ')[1].split('-')[0]
                if name in known_amis:
                    creation_date = lines[i + 9].split(': ')[1].strip()
                    if creation_date != latest_amis[name] and creation_date < latest_amis[name]:
                        image_id = lines[i + 1].split(': ')[1].strip()
                        older_amis[name].append(image_id)
            i += 1

    for name, older_versions in older_amis.items():
        print(f"\nOlder versions for {name} with Image IDs:")
        if older_versions:
            print("\t" + "\n\t".join(older_versions))
        else:
            print("\tNone")

    return older_amis

def find_older_amis_snapshots(output_file, older_amis):
    older_amis_snapshots = {}

    with open(output_file, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('ImageId:'):
                image_id = lines[i].split(': ')[1].strip()
                for name, older_versions in older_amis.items():
                    if image_id in older_versions:
                        snapshot_index = -1
                        for j in range(i, len(lines)):
                            if 'Snapshot ID:' in lines[j]:
                                snapshot_index = j
                                break
                        if snapshot_index != -1:
                            snapshot_id = lines[snapshot_index].split(': ')[1].strip()
                            older_amis_snapshots.setdefault(name, []).append(snapshot_id)
            i += 1

    for name, snapshot_ids in older_amis_snapshots.items():
        print(f"\nSnapshot IDs for older versions of {name}:")
        if snapshot_ids:
            print("\t" + "\n\t".join(snapshot_ids))
        else:
            print("\tNone")

    return older_amis_snapshots

def delete_amis_and_snapshots(older_amis, older_amis_snapshots, ec2_client):
    for name, ami_ids in older_amis.items():
        print(f"\nOld {name} AMI marked for de-registration:")
        if ami_ids:
            print("\t" + "\n\t".join(ami_ids))
        else:
            print("\tNone")

        if name in older_amis_snapshots:
            print(f"\n{name} Snapshots marked for removal:")
            if older_amis_snapshots[name]:
                print("\t" + "\n\t".join(older_amis_snapshots[name]))
            else:
                print("\tNone")
        else:
            print(f"\nNo snapshots found for older versions of {name}")

    print("\n")

    if not older_amis_snapshots or not older_amis:
        print("No AMIs or snapshots to delete. Exiting.")
        sys.exit(0)

    confirmation = input("Proceed with deletion? (yes/no): ").lower()

    while confirmation not in ['yes', 'no']:
        print("Invalid input. Please enter 'yes' or 'no'.")
        confirmation = input("Proceed with deletion? (yes/no): ").lower()

    if confirmation == "yes":
        for name, snapshot_ids in older_amis_snapshots.items():
            for snapshot_id in snapshot_ids:
                ec2_client.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted snapshot: {snapshot_id}")

        for name, ami_ids in older_amis.items():
            for ami_id in ami_ids:
                ec2_client.deregister_image(ImageId=ami_id)
                print(f"Deregistered AMI: {ami_id}")
    else:
        print("Deletion aborted. Nothing was removed.")
        sys.exit(0)

def main():
    aws_profile_name = os.environ.get('AWS_PROFILE')
    aws_region = os.environ.get('AWS_REGION')

    if not (aws_profile_name and aws_region):
        print("Missing required environment variables.")
        sys.exit(1)

    session = boto3.session.Session(
        region_name=aws_region,
        profile_name=aws_profile_name
    )

    sts_client = session.client('sts')
    response = sts_client.get_caller_identity()
    owner_id = response['Account']
    ec2 = session.resource('ec2')
    ec2_client = session.client('ec2')

    response = ec2_client.describe_images(Owners=[owner_id])
    ami_info_file = get_ami_info(response)

    older_amis = find_older_amis(ami_info_file)
    older_amis_snapshots = find_older_amis_snapshots(ami_info_file, older_amis)

    delete_amis_and_snapshots(older_amis, older_amis_snapshots, ec2_client)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to manage AMIs and their associated snapshots.")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    main()
