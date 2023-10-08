import boto3
import json

region = boto3.Session().region_name

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
)

runtime_client = session.client('sagemaker-runtime')
content_type = "application/json"
request_body = {"Input": [[0, 3.0, 3.0, 2.0, 2.0, 0.0, 4.0, 7.0]]}
data = json.loads(json.dumps(request_body))
payload = json.dumps(data)
endpoint_name = "sklearn-hepatite-ep2023-10-07-15-49-36"

response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=payload)
result = json.loads(response['Body'].read().decode())['Output']
print(result)
