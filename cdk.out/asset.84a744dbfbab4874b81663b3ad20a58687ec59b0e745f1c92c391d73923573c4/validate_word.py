from common.dictionary_client import DictionaryClient

def lambda_handler(event, context):
    print(event)
    word = event['word']
    client = DictionaryClient()
    return client.query_word(word)

if __name__ == "__main__":
    event = {}
    event['word'] = 'apple'
    resp = lambda_handler(event, None)
    print(resp.content)