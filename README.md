# s3-transfer

# DISCLAIMER
This sample code is provided for demonstration purposes only and is not intended for production use.  
The code:
- Has not undergone security review or testing
- Is not maintained or supported by AWS
- Should be reviewed and tested thoroughly before any production consideration
- May contain vulnerabilities or implementation issues
- Should not be used with sensitive or production data
- Is provided "AS IS" without warranties of any kind

You are responsible for:
- Testing and securing the code before any production use
- Implementing appropriate security controls
- Reviewing and optimizing the code for your specific needs
- Maintaining and updating the code as needed
- All AWS service costs incurred through the use of this code




Create the Lambda function

Complete the following steps:

    Open the Functions page in the Lambda console.

    Choose Create function, and then, choose Author from scratch.

    For Function name, enter a name for your function.

    From the Runtime dropdown list, choose Python 3.13.

    Expand Change default execution role, and then choose Create a new role with basic permissions.

    Choose Create function.

    Choose the Code tab, and then paste the following Python code

[a relative link](lambda_function.py)
    
    Note: Find the source_bucket name from the event object that the Lambda function receives. You can store the destination_bucket name as an environment variable.

    Choose Deploy.

Lambda creates an execution role that grants the function permission to upload logs to Amazon CloudWatch. For more information, see Create a Lambda function with the console.
Create an Amazon S3 trigger for the Lambda function

Complete the following steps:

    Open the Functions page in the Lambda console.
    In Functions, choose the Lambda function.
    In Function overview, choose Add trigger.
    From the Trigger configuration dropdown list, choose S3.
    In Bucket, enter the name of your source bucket.
    From the Event type dropdown list, choose All object create events.
    Note: Configure this step to use either the POST, PUT, or Multipart Upload event type to upload the object.
    Select the I acknowledge that using the same S3 bucket for both input and output is not recommended agreement, and then choose Add.

For more information, see Tutorial: Using an Amazon S3 trigger to invoke a Lambda function.
Provide IAM permissions for the Lambda function's execution role

To copy files to the destination S3 bucket, add AWS Identity and Access Management (IAM) permissions for the Lambda function's execution role. Use a policy similar to the following resource-based policy:



Note:

    Replace destination-s3-bucket with your S3 destination bucket and source-s3-bucket with your S3 source bucket.
    Replace /* at the end of the resource ARN with the required prefix value for your environment to limit permissions.
    It's a best practice to grant least privilege permissions to perform a task.
    To copy objects that have object tags, the execution role must have s3:GetObjectTagging and s3:PutObjectTagging permissions. You must have s3:GetObjectTagging permission for the source object in the source bucket and s3:PutObjectTagging permission for objects in the destination bucket.

