from common.dictionary_client import DictionaryClient
from common.apigateway_responder import ApiGatewayResponder
import os

def lambda_handler(event, context):
    print(event)
    subject = event['subject']
    access_key = event['access_key']
    bucket_name = os.environ['BUCKET']
    print("S3 Bucket name [{}]".format(bucket_name))
    client = DictionaryClient(bucket_name=bucket_name)
    responder = ApiGatewayResponder()
    client.toggle_exception_subject(access_key, subject)
    return responder.respond_success({})
