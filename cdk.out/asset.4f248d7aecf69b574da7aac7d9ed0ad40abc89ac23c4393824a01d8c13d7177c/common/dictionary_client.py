import urllib3
import json
from common.s3_reader import S3Reader

class DictionaryClient:
    def __init__(self, bucket_name):
        self.base_url='https://dictionaryapi.com/api/v3/references/sd3/json/'
        self.api_key='bc5c2d51-6a62-43b2-87cc-eeabd258ea7a'
        self.http = urllib3.PoolManager()
        self.access_keys = S3Reader(bucket_name, '/access_keys.json')
        self.house_words = S3Reader(bucket_name, '/house_words.json')
        self.invalid_subjects = S3Reader(bucket_name, '/invalid_subjects.json')
        self.access_keys_set = self.access_keys.read_set()
        self.house_words_set = self.house_words.read_set()
        self.invalid_subjects_set = self.invalid_subjects.read_set()
    
    def query_word(self, word):
        query_url = '{}"{}"?key={}'.format(self.base_url, word, self.api_key)
        response = self.http.request("GET", query_url)
        payload = json.loads(response.data.decode('utf-8'))
        word_definition = self.transformMerriamToLocal(payload, word)
        if word in self.house_words_set:
            return {
                "isValid" : False,
                "reason" : 'Exception Word',
                "meta" : {
                    "foundDefinition" : word_definition
                }
            }
        if not word_definition["isFound"]:
            return {
                "isValid" : False,
                "reason" : "Word Not Found",
            }
        definition_search = self.has_valid_definition(word_definition["definitions"])
        if(definition_search["result"]):
            return {
                "isValid" : True,
                "foundDefinition" : definition_search["foundValidDefinition"]
            }
        else:
            return {
                "isValid" : False,
                "reason" : "Exception subjects",
                "meta" : {
                    "exceptionSubjects" : definition_search["allSubjects"]
                }
            }
    
    def mark_exception_word(self, access_key, word):
        if(word in self.access_keys_set):
            self.house_words_set.add(word)
            self.house_words.write_set(self.house_words_set)
        else:
            raise Exception('Permission Denied')
    
    def mark_exception_subject(self, access_key, subject):
        if(word in self.access_keys_set):
            self.invalid_subjects_set.add(subject)
            self.invalid_subjects.write_set(self.invalid_subjects_set)
        else:
            raise Exception('Permission Denied')

    def has_valid_definition(self, definitions):
        set_of_subjects = set()
        for definition in definitions:
            if definition["subject"] not in self.invalid_subjects_set:
                return {
                    "result" : True,
                    "foundValidDefinition" : definition
                }
            else:
                set_of_subjects.add(definition["subject"])
        return {
            "result" : False,
            "allSubjects" : list(set_of_subjects)
        }


    def transformMerriamToLocal(self, apiResponse, word):
        if len(apiResponse) > 0:
            definitions = []
            for merriamWord in apiResponse:
                subject = merriamWord["fl"]
                definition = merriamWord["shortdef"][0]
                definitions.append({
                    "subject" : subject,
                    "definition" : definition
                })
            return {
                "isFound" : True,
                "word" : word,
                "definitions" : definitions
            }
        else:
            return {
                "isFound" : False,
                "word" : word
            }


if __name__ == "__main__":
    client = DictionaryClient()
    resp = client.query_word("pizza")
    print(resp)