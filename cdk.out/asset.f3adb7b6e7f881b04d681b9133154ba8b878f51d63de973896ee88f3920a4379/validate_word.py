from common.dictionary_client import DictionaryClient
from common.apigateway_responder import ApiGatewayResponder

def lambda_handler(event, context):
    print(event)
    word = event['word']
    bucket_name = process.env.BUCKET
    print("S3 Bucket name [{}]".format(bucket_name))
    client = DictionaryClient(bucket_name=bucket_name)
    responder = ApiGatewayResponder()
    response = client.query_word(word)


if __name__ == "__main__":
    event = {}
    event['word'] = 'apple'
    resp = lambda_handler(event, None)
    print(resp)