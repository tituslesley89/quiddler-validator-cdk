import boto3
import json

class S3Reader:
    def __init__(self, bucket_name, file_key):
        self.bucket_name = bucket_name
        self.file_key = file_key
        self.s3_client = boto3.resource("s3")
        self.bucket_client = self.s3_client.Bucket(bucket_name)
    
    def file_exist(self):
        try:
            self.s3_client.Object(self.bucket_name, self.file_key).load()
        except:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise Exception('Could not confirm if file exists.')
        else:
            return True

    def read_set(self):
        if(not self.file_exist()):
            self.write_set([])
            return set([])
        else:
            content_object = self.s3_client.Object(self.bucket_name, self.file_key)
            file_content = content_object.get()['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)
            return set(json_content)

    def write_set(self, set_content):
        client = self.s3_client.Object(self.bucket_name, self.file_key).load()
        client.put(
            Body=(bytes(json.dumps(list(set_content)).endcode('UTF-8')))
        )
