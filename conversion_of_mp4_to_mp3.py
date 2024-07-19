import json
import boto3

s3 = boto3.resource('s3')
s3_client=boto3.client('s3')
client = boto3.client('elastictranscoder')
def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    bucketname = event['Records'][0]['s3']['bucket']['name']
    source_bucket = s3.Bucket('project1-mp4-file')
    dest_bucket = s3.Bucket('project1-mp3-file')
    def obj_last_modified(myobj):
        return myobj.last_modified
        
    sortedObjects = sorted(source_bucket.objects.all(), key=obj_last_modified, reverse=True)
    print(sortedObjects[0].key)
    o = sortedObjects[0].key
    # response_contents = s3_client.list_objects_v2(
    #     Bucket='sainath-input-file'
    #     )
    # print(response_contents['Contents'][0]['Key'])
    client.create_job(
        PipelineId='1721380723127-bmrp64',
        Input= 
            {
              'Key': o,
              'FrameRate': 'auto',
              'Resolution': 'auto',
              'AspectRatio': 'auto',
              'Interlaced': 'auto',
              'Container': 'auto'
            },
        Outputs=
        [
            {
                 'Key': o.strip('.mp4') +'.mp3',
                'PresetId': '1351620000001-300010' # mp3 320
            }
        ]
    )
    # # s3.Object(source_bucket.name, response_contents['Contents'][count]['Key']).delete()