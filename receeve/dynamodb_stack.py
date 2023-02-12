from aws_cdk import (
    aws_iam as iam,
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_s3 as s3,
    Duration, Stack
)
import aws_cdk as core
from constructs import Construct

class DynamoDBWithBackupStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create dynamo table.
        # DynamoDB point-in-time recovery needs to be enabled
        # if we need to backup DynamoDB to S3.
        demo_table = aws_dynamodb.Table(
            self, "demo_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            point_in_time_recovery = True,
            removal_policy=core.RemovalPolicy.DESTROY,
            read_capacity=1,
            write_capacity=1
        )

        backup_bucket = s3.Bucket(self, "backup_bucket",
                                      versioned=True,
                                      encryption=s3.BucketEncryption.S3_MANAGED,
                                      block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                      enforce_ssl=True,
                                      removal_policy=core.RemovalPolicy.DESTROY)


        # create lambda function
        backup_lambda = aws_lambda.Function(self, "backup_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_9,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.from_asset("./lambda"),
                                              initial_policy=[
                                                iam.PolicyStatement(actions=['dynamodb:ExportTableToPointInTime'],
                                                                    resources=[
                                                                        demo_table.table_arn]
                                                                    ),
                                                iam.PolicyStatement(actions=['s3:AbortMultipartUpload',
                                                                             's3:PutObject',
                                                                             's3:PutObjectAcl'],
                                                                    resources=[
                                                                        backup_bucket.bucket_arn+'/*']
                                                                    ),
                                              ]
                                            )

        backup_lambda.add_environment("TABLE_ARN", demo_table.table_arn)
        backup_lambda.add_environment("BACKUP_BUCKET", backup_bucket.bucket_name)

        # grant permission to lambda to read from demo table
        demo_table.grant_read_data(backup_lambda)

        # create a Cloudwatch Event rule - everyday at 2:00 AM UTC time
        event_rule = aws_events.Rule(
            self, "everyday_at_2_00_AM_UTC",
            schedule=aws_events.Schedule.expression('cron(0 2 * * ? *)'),
        )

        # Add target to Cloudwatch Event
        event_rule.add_target(aws_events_targets.LambdaFunction(backup_lambda))