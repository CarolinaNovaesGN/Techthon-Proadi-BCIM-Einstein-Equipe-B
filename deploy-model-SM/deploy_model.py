import time
import sagemaker
import boto3
from sagemaker.estimator import Estimator
from time import gmtime,strftime
import subprocess

#configurando client
region = boto3.Session().region_name

role = "arn:aws:iam::174315626162:role/service-role/SageMaker-MLOpsEngineer"

sm_client = boto3.client('sagemaker', region_name=region)
runtime = boto3.client(service_name="sagemaker-runtime")

boto_session = boto3.session.Session()
s3 = boto_session.resource('s3')

sagemaker_session = sagemaker.Session()


#Monta um tar file com o modelo serializado e o script de inferencia.
bashCommand = "tar -cvpzf model.tar.gz model.joblib inference.py"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


#Bucket para os artefatos do modelo
default_bucket = sagemaker_session.default_bucket()
print(default_bucket)

#Realiza o upload do tar.gz para o bucket
model_artifacts = f"s3://{default_bucket}/model.tar.gz"
response = s3.meta.client.upload_file('model.tar.gz', default_bucket, 'model.tar.gz')

#Seleciona uma imagem do sklearn prebuildada disponível da aws
image_uri = sagemaker.image_uris.retrieve(
    framework="sklearn",
    region=region,
    version="1.0-1",
    py_version="py3",
    instance_type="ml.m5.xlarge",
)

#Step 1: Model Creation
model_name = "sklearn-hepatite-model" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
print("Model name: " + model_name)
create_model_response = sm_client.create_model(
    ModelName=model_name,
    Containers=[
        {
            "Image": image_uri,
            "Mode": "SingleModel",
            "ModelDataUrl": model_artifacts,
            "Environment": {'SAGEMAKER_SUBMIT_DIRECTORY': model_artifacts,
                           'SAGEMAKER_PROGRAM': 'inference.py'} 
        }
    ],
    ExecutionRoleArn=role,
)
print("Model Arn: " + create_model_response["ModelArn"])

#Step 2: EPC Creation
sklearn_epc_name = "sklearn-epc" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
endpoint_config_response = sm_client.create_endpoint_config(
    EndpointConfigName=sklearn_epc_name,
    ProductionVariants=[
        {
            "VariantName": "sklearnvariant",
            "ModelName": model_name,
            "InstanceType": "ml.m5.xlarge",
            "InitialInstanceCount": 1
        },
    ],
)
print("Endpoint Configuration Arn: " + endpoint_config_response["EndpointConfigArn"])

#Step 3: EP Creation
endpoint_name = "sklearn-hepatite-ep" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
create_endpoint_response = sm_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=sklearn_epc_name,
)
print("Endpoint Arn: " + create_endpoint_response["EndpointArn"])


#Monitor creation
describe_endpoint_response = sm_client.describe_endpoint(EndpointName=endpoint_name)
while describe_endpoint_response["EndpointStatus"] == "Creating":
    describe_endpoint_response = sm_client.describe_endpoint(EndpointName=endpoint_name)
    print(describe_endpoint_response["EndpointStatus"])
    time.sleep(15)
print(describe_endpoint_response)
#------------------------------------------------------------------------------------------------------------------
#Criando um model group no sagemaker
#import time
#model_package_group_name = "scikit-hepatite-" + str(round(time.time()))
#model_package_group_input_dict = {
# "ModelPackageGroupName" : model_package_group_name,
# "ModelPackageGroupDescription" : "Hepatite model package group."
#}
#
#create_model_package_group_response = sm_client.create_model_package_group(**model_package_group_input_dict)
#print('ModelPackageGroup Arn : {}'.format(create_model_package_group_response['ModelPackageGroupArn']))
#------------------------------------------------------------------------------------------------------------------

