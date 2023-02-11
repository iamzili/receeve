import aws_cdk as cdk
from constructs import Construct
from receeve.dynamodb_stack import DynamoDBWithBackupStack

class MyDynamoDBStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dynamoStack = DynamoDBWithBackupStack(self, "DynamoDBstack")