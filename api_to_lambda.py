import json
import boto3
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
cs_client = boto3.client('cloudsearchdomain',endpoint_url='http://doc-domain-mtaa3wn4tjw3uzwek7dv6si4cu.us-east-1.cloudsearch.amazonaws.com')
def lambda_handler(event, context):
    print(event)
    if (event['queryStringParameters'] != None ):
        if ( (event['queryStringParameters']['query']!= None) and (event['queryStringParameters']['query']!= "")):
            q = event['queryStringParameters']['query']
            print(q)
    r=cs_client.search(
        query=q
        )
    print(r)
    response =  {
                "statusCode": 200,
                "body": r['hits']['hit']
                # "headers": { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" }
                }
    return r['hits']['hit']
    print('response and res')