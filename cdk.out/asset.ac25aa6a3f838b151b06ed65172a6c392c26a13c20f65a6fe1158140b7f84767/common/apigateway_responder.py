import json

class ApiGatewayResponder:

    def respond_success(self, content):
        return {
            "statusCode" : 200,
            "body" : json.dumps(content)
        }