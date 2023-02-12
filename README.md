# Instructions

1. set `~/.aws/credentials`
2. bootstrap AWS envs, where XXXXXXX is the AWS account ID, YYYYYYYY is the AWS profile
```
cd ..
npx cdk bootstrap aws://XXXXXXX/eu-central-1 --profile YYYYYYYY \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
```
3. cd receeve
4. create python virtual environment (Python 3.10.10 used)
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
5. execute `cdk deploy`
6. Change code, commit push, everything should be deployed automatically. We don't need `cdk deploy` anymore.
