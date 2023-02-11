import aws_cdk as core
import aws_cdk.assertions as assertions

from receeve.receeve_stack import ReceeveStack

# example tests. To run these tests, uncomment this file along with the example
# resource in receeve/receeve_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ReceeveStack(app, "receeve")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
