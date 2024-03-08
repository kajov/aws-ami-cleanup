import boto3
import os
import sys
import argparse

def delete_amis_and_snapshots(ec2_client):
    response = ec2_client.describe_images(Owners=['self'])

    for image in response['Images']:
        ami_id = image['ImageId']
        print(f"\nAMI marked for de-registration: {ami_id}")

        try:
            ec2_client.deregister_image(ImageId=ami_id)
            print(f"Deregistered AMI: {ami_id}")
        except Exception as e:
            print(f"Error deregistering AMI {ami_id}: {str(e)}")

    # Now that all AMIs are deregistered, let's delete the associated snapshots
    response = ec2_client.describe_snapshots(OwnerIds=['self'])

    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        print(f"\nSnapshot marked for deletion: {snapshot_id}")

        try:
            ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot: {snapshot_id}")
        except Exception as e:
            print(f"Error deleting snapshot {snapshot_id}: {str(e)}")

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

    ec2_client = session.client('ec2')

    delete_amis_and_snapshots(ec2_client)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to manage AMIs and their associated snapshots.")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    main()
