import json
import boto3

def lambda_handler(event, context):
    # Initialize the S3 and Rekognition clients
    s3 = boto3.client('s3')
    rekognition = boto3.client('rekognition')

    # Specify the output bucket where the results will be stored
    output_bucket = 'imagelabelerpro-results-bucket'

    # Iterate through the S3 events triggered by the image uploads
    for record in event['Records']:
        # Extract information about the S3 object from the event record
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Use Rekognition to detect labels in the uploaded image
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )

        # Extract label names from the Rekognition response
        labels = [label['Name'] for label in response['Labels']]

        # Define the key for storing the result JSON file in the output bucket
        result_key = f"results/{key.split('/')[-1].split('.')[0]}-labels.json"

        # Store the detected labels in the specified output bucket
        s3.put_object(
            Bucket=output_bucket,
            Key=result_key,
            Body=json.dumps(labels),
            ContentType='application/json'
        )

    # Return a response indicating successful execution
    return {
        'statusCode': 200,
        'body': json.dumps('Labels detected and stored successfully!')
    }
