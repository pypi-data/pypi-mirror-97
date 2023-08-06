import boto3
from boto3.exceptions import Boto3Error as DynamoError

# Create DynamoDB resource.
dynamo_db = boto3.resource('dynamodb')