<img src="https://media.licdn.com/dms/image/D5612AQERySmtAVp7kQ/article-cover_image-shrink_600_2000/0/1680275682788?e=2147483647&v=beta&t=E7UEu2xOneY6O7S5Ud09E2YglQa_d9ZZGhIoZOmp9aI" alt="AWS Cloud" width="250" height="200" />

[![Quality gate](https://q0pag5bxw8.loclx.io/api/project_badges/quality_gate?project=ka.jov_aws-ami-cleanup_f885e82f-ed7d-4fe6-b3a2-ff7bd4353142&token=sqb_0958f75c44691d25ac48a59d8ab71b7420854f67)](https://q0pag5bxw8.loclx.io/dashboard?id=ka.jov_aws-ami-cleanup_f885e82f-ed7d-4fe6-b3a2-ff7bd4353142)

# AMI and Snapshot Management Script 

This Python script allows you to manage Amazon Machine Images (AMIs) and their associated snapshots on AWS.

## Description

The script uses the AWS SDK for Python (Boto3) to perform the following tasks:
- Fetch information about AMIs owned by the specified AWS account.
- Filter and display details about AMIs, such as Name, Image ID, Architecture, and more.
- Identify older versions of known AMIs and their associated Image IDs.
- Identify associated snapshots for older versions of AMIs and their Snapshot IDs.
- Provide options to deregister AMIs and delete associated snapshots based on user confirmation.

## Usage

### Expected Environment Variables

- `AWS_PROFILE`: The AWS profile name with appropriate permissions.
- `AWS_REGION`: The AWS region where the AMIs and snapshots are located.

[//]: # (- `CLUSTER_NAME`: &#40;Optional&#41; Cluster name, if applicable.)

### Expected Pip Modules

- `boto3`: AWS SDK for Python. Install it via pip:
  ```bash
  pip install boto3
  ```
- install with requirements.txt
  ```bash
  pip install -r requirements.txt
  ```
  
### Running the Script
  1. Set up the required environment variables mentioned above.
  2. Install the necessary Python modules using the provided pip install command.
  3. Run the script:
- ```bash
  python remove-amis.py [--debug]
  ```
- Use `--debug` flag to enable debug mode (optional). This retrieves all AMIs available to the AWS Profile
- Follow on-screen prompts for deletion confirmation when necessary.
- Debug mode currently is not functioning properly

# Important Note
  Ensure that the AWS credentials associated with the provided profile have appropriate permissions to deregister AMIs and delete associated snapshots.

# Disclaimer
Be cautious when performing deletion operations, as they can't be reversed. Always verify the items to be deleted before confirming deletion.
