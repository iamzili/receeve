import os
import boto3
import json

dynamodb = boto3.client("dynamodb")

# set environment variable
table_arn = os.environ["TABLE_ARN"]
bucket_name = os.environ["BACKUP_BUCKET"]


def lambda_handler(event, context):
    try:
        response = dynamodb.export_table_to_point_in_time(
            TableArn=table_arn,
            S3Bucket=bucket_name,
            S3SseAlgorithm='AES256',
            ExportFormat='DYNAMODB_JSON'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(response['ExportDescription']['ExportArn'])
        }

    except Exception as e:
        print('Error')
        print(str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }