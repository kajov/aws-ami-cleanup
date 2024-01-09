![AWS](https://www.google.com/url?sa=i&url=https%3A%2F%2Fmedium.datadriveninvestor.com%2Fintroduction-to-cloud-security-with-aws-13d537ac5d03&psig=AOvVaw04RYslrzYwdV_6PTW1qq4z&ust=1704896468978000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCJjshbfA0IMDFQAAAAAdAAAAABAD)
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
### Running the Script
  1. Set up the required environment variables mentioned above.
  2. Install the necessary Python modules using the provided pip install command.
  3. Populate the map for the known names of the AMIs that you are using
  - ```python3
     known_amis = ['ami-name1, ami-name2, ami-name3, ami-name4...']
    ```
  4. Run the script:
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