import boto3
import csv

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Step 1: Get file info from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f"File mili: {key} from bucket: {bucket}")

    # Step 2: Read file from S3
    obj = s3.get_object(Bucket=bucket, Key=key)
    rows = obj['Body'].read().decode('utf-8').splitlines()

    # Step 3: Parse and write to DynamoDB (case-sensitive table name!)
    table = dynamodb.Table('Processedrecords')
    for row in csv.DictReader(rows):
        if row.get('id'):
            table.put_item(Item=row)
            print(f"Inserted: {row}")

    print("Done")
    return {"statusCode": 200, "body": "Success"}
