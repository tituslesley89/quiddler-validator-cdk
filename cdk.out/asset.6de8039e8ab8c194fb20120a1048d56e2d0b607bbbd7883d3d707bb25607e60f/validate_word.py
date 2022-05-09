import requests
from common.dictionary_client import DictionaryClient

def lambda_handler(event, context):
    print(event)
    word = event['word']
    client = DictionaryClient()
    return client.query_word(word)