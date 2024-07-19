import json
import boto3
s3_client = boto3.client('s3')

 

def lambda_handler(event, context):
    print(str(event))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key =event['Records'][0]['s3']['object']['key']
    str_key = key.split('/')[-1]
    file_key = str_key.split('.')[0]
    # print(bucket_name)
    # print(key)
    json_file_name = event['Records'][0]['s3']['object']['key']
    # print(json_file_name)
    json_object = s3_client.get_object(Bucket = bucket_name , Key = json_file_name)
    jsonFileReader = json_object['Body'].read()
    data = json.loads(jsonFileReader)

    s3 = boto3.resource('s3')

 

    my_bucket = s3.Bucket(bucket_name)

    video_name =file_key+".mp4"
    folder_name =''

 

    print("**********************************************************")
    for file in my_bucket.objects.all():
        folder = file.key
        if video_name in folder:
            folder_name = folder.replace(video_name,'')
            # print(folder_name)

 

    print("**********************************************************")

 

    fileEndPoint = "https://d3ni8ihy6grs9u.cloudfront.net/inputvideo/"+file_key+".mp4"
    # print(fileEndPoint)
    # print(data)

    cs_client = boto3.client('cloudsearchdomain',endpoint_url='http://doc-domain-mtaa3wn4tjw3uzwek7dv6si4cu.us-east-1.cloudsearch.amazonaws.com')

 

 

    data1 = ''
    for i in range(len(data['results']['items'])):
        if((data['results']['items'][i].__contains__('start_time')) and  (data['results']['items'][i].__contains__('end_time')) and (data['results']['items'][i]['alternatives'][0].__contains__('confidence')) and (data['results']['items'][i]['alternatives'][0].__contains__('content')) and (data['results']['items'][i].__contains__('type'))):
            if (i!=0):
                data1 = data1 + ',\n'
            #     print(data['results']['items'][i]['alternatives'][0]['content'])
            # if data['results']['items'][i]['alternatives'][0]['content'] == 'A':
            #     print(data1)
              
            data1 = data1 + '{"type": "add",\n'
            data1 = data1 + '"id":"' +str(i)+ '",\n'
            data1 = data1 + '"fields":{\n'
            data1 = data1 + '"start_time": "' +data['results']['items'][i]['start_time']+'",\n'
            data1 = data1 + '"end_time": "' +data['results']['items'][i]['end_time']+'",\n'
            data1 = data1 + '"confidence": "' +data['results']['items'][i]['alternatives'][0]['confidence']+'",\n'
            data1 = data1 + '"content": "' +data['results']['items'][i]['alternatives'][0]['content']+'",\n'
            data1 = data1 + '"type": "'+data['results']['items'][i]['type']+'",\n'
            data1 = data1 + '"url": "'+fileEndPoint+'"\n'
            data1 = data1 + '  }}\n'
            
            # if data['results']['items'][i]['alternatives'][0]['content'] == 'A':
            #     print("after adding data")
            #     print(data1)

 

    file_data = '[\n'+data1+'\n]'
    
    # print("final data")

    print('response')
    response = cs_client.upload_documents(
    documents=file_data,
    contentType='application/json'
    )
    print(boto3.client('cloudsearch').describe_domains())
    print('response')