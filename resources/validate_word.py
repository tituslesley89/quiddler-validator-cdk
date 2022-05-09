from common.dictionary_client import DictionaryClient
from common.apigateway_responder import ApiGatewayResponder

def lambda_handler(event, context):
    print(event)
    word = event['word']
    client = DictionaryClient()
    responder = ApiGatewayResponder()
    response = client.query_word(word)
    return responder.respond_success(response)

if __name__ == "__main__":
    event = {}
    event['word'] = 'apple'
    resp = lambda_handler(event, None)
    print(resp)