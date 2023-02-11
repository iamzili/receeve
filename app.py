#!/usr/bin/env python3
import os

import aws_cdk as cdk

from receeve.receeve_stack import ReceeveStack


app = cdk.App()
ReceeveStack(app, "ReceeveStack",
    env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])
)

app.synth()
