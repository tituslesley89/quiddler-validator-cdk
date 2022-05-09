import * as s3 from "aws-cdk-lib/aws-s3";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import { QuiddlerAppConstants } from "./quiddler-app-constants";
import { aws_apigateway } from "aws-cdk-lib";
import { Function } from "aws-cdk-lib/aws-lambda";

export class QuiddlerBackendServices extends Construct {
    constructor(scope: Construct, id: string, props: QuiddlerAppConstants) {
        super(scope, id)

        const bucket = new s3.Bucket(this, props.s3BucketName)

        const validate_word_lambda = this.createLambdaFunction('ValidateWordLambda', 'validate_word', props)

        bucket.grantReadWrite(validate_word_lambda);

        const api = new aws_apigateway.RestApi(this, "quiddler-api", {
            restApiName: "Quiddler Validator",
            description: "Service to validate quiddler words"
        })

        const validate = api.root.addResource("validate")
        const validateWithWord = validate.addResource("{word}")
        validateWithWord.addMethod("GET", new aws_apigateway.LambdaIntegration(validate_word_lambda))
    }


    createLambdaFunction(resourceName: string, pythonfileName:string, props: QuiddlerAppConstants) : Function {
        return new lambda.Function(this, resourceName, {
            runtime: lambda.Runtime.PYTHON_3_8,
            code: lambda.Code.fromAsset("resources"),
            handler: `${pythonfileName}.lambda_handler`,
            environment : {
                BUCKET : props.s3BucketName
            }
        })
    }
}