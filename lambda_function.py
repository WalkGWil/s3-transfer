import boto3
import botocore
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    logger.info("New files uploaded to the source bucket.")
    
    # Enable this line to enable a readout of the event body in the log
    # logger.info(f"Event received: {json.dumps(event)}")

    key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    destination_bucket = os.environ['destination_bucket']
    
    # Generate timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m_%d')
    
    # Extract folder and filename
    if "/" in key:
        folder, filename = key.rsplit("/", 1)  # Extract folder path and filename
    else:
        folder, filename = "", key  # No folder structure
    
    # Construct the new destination key with date subfolder
    if folder:
        destination_key = f"{folder}/{timestamp}/{filename}"
        archive_key = f"archive/{folder}/{timestamp}/{filename}"  # Move to archive with same folder structure
    else:
        destination_key = f"{timestamp}/{filename}"
        archive_key = f"archive/{timestamp}/{filename}"  # Move to archive if no folder exists
    
    source = {'Bucket': source_bucket, 'Key': key}
    
    try:
        # Copy the file to the destination bucket
        s3.meta.client.copy(source, destination_bucket, destination_key)
        logger.info(f"File copied successfully to: {destination_bucket}/{destination_key}")
        
        # Move (Copy + Delete) to Archive within the same source bucket
        archive_source = {'Bucket': source_bucket, 'Key': key}
        s3.meta.client.copy(archive_source, source_bucket, archive_key)  # Copy to archive
        s3.Object(source_bucket, key).delete()  # Delete original file
        logger.info(f"File moved to archive: {source_bucket}/{archive_key}")

    except botocore.exceptions.ClientError as error:
        logger.error("Error during file processing")
        logger.error(f"Error Message: {error}")

    except botocore.exceptions.ParamValidationError as error:
        logger.error("Missing required parameters while calling the API.")
        logger.error(f"Error Message: {error}")