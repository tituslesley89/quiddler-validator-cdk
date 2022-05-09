import urllib3
import json

class DictionaryClient:
    def __init__(self):
        self.base_url='https://dictionaryapi.com/api/v3/references/sd3/json/'
        self.api_key='bc5c2d51-6a62-43b2-87cc-eeabd258ea7a'
        self.http = urllib3.PoolManager()
    
    def query_word(self, word):
        query_url = '{}{}?key={}'.format(self.base_url, word, self.api_key)
        print(query_url)
        response = self.http.request("GET", query_url)
        return json.loads(response.data.decode('utf-8'))

if __name__ == "__main__":
    client = DictionaryClient()
    resp = client.query_word("apple")
    print(resp)