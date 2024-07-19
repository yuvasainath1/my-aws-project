import json
import boto3
import re
import random

s3 = boto3.resource('s3')
s3_client=boto3.client('s3')
client = boto3.client('transcribe')

def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    bucketname = event['Records'][0]['s3']['bucket']['name']
    source_bucket = s3.Bucket('project1-mp3-file')
    dest_bucket = s3.Bucket('project1-json-file')
    
    def obj_last_modified(myobj):
        return myobj.last_modified
        
    sortedObjects = sorted(source_bucket.objects.all(), key=obj_last_modified, reverse=True)
    print(sortedObjects[0].key)
    o = sortedObjects[0].key
    
    # response_contents = s3_client.list_objects_v2(
    #     Bucket='sainath-output-file'
    #     )
    # print(response_contents['Contents'][0]['Key'])
    # var = response_contents['Contents'][0]['Key']
    
    def sanitize_filename(filename):
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        random_number = random.randint(1, 500)
        return f"{sanitized}_{random_number}"

    transcription_job_name = sanitize_filename(o.strip('.mp3'))
    output_key = sanitize_filename(o.strip('.mp3')) + '.json'

    client.start_transcription_job(
        TranscriptionJobName=transcription_job_name,
        LanguageCode='en-US',
        MediaFormat='mp3',
        Media={
            'MediaFileUri': 's3://project1-mp3-file/' + o,
        },
        OutputBucketName='project1-json-file',
        OutputKey=output_key,
    )
    print('response')
    # s3.Object(source_bucket.name, response_contents['Contents'][0]['Key']).delete()    