import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { QuiddlerAppConstants } from './quiddler-app-constants';
import { QuiddlerBackendServices } from './quiddler-backend-service';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class QuiddlerBackendStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const appConst : QuiddlerAppConstants = {
      s3BucketName : 'quiddler-validator-0bc'
    }

    new QuiddlerBackendServices(this, 'QuiddlerBackendService', appConst)
  }
}
