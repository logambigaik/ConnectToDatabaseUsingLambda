import os
import datetime
import boto3
import base64
import json
import logging

db_client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def handler(event, context):
    TABLE_NAME = os.getenv('DB_TABLE_NAME')
    try:
        response = db_client.put_item(
            TableName=TABLE_NAME,
            Item=get_item(event))  
    except Exception as e:
        logging.error("Exception occured while inserting data : %s", e)

def get_item(event):
    encodedEventBody = event['records']['FAILED_VALIDATION-0'][0]['value']
    notificationType = event['records']['FAILED_VALIDATION-0'][0]['topic']
    decodedEventBody = base64.b64decode(encodedEventBody)
    EventBody = json.loads(decodedEventBody)
    return {
            "uuid": {"S": str(EventBody['objectKey'])},
            "userName": {"S": str(EventBody['dataSetOwners'][0])},
            "notificationType": {"S": str(notificationType)},
            "timeStamp": {"S": str(datetime.datetime.now())},
            "isRead": {"BOOL": False}
    }
