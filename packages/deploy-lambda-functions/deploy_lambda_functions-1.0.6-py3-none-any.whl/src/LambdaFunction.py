import boto3

class LambdaFunction:

    def __init__(self, name, region='us-east-2'):
        self.name = name
        self.client = boto3.client('lambda',region_name=region)

    def deploy(self, S3bucket,S3key):
        print("Deploying function: {}".format(self.name))
        self.client.update_function_code(
            FunctionName=self.name,
            S3Bucket=S3bucket,
            S3Key=S3key
        ) 

    def update_alias(self,alias,description, version):
        print("Updating alias: {}".format(alias))
        try:
            return self.client.update_alias(
                FunctionName=self.name,
                Name=alias,
                Description=description,
                FunctionVersion=version
            )
        except self.client.exceptions.ResourceNotFoundException:
            print("Alias not exist")
            return self.create_alias(alias,description,version)

    def create_alias(self,alias,description,version):
        print("Creating alias: {}".format(alias))
        return self.client.create_alias(
            FunctionName=self.name,
            Name=alias,
            Description=description,
            FunctionVersion=version
        )

    def publish_version(self,description):
        print("Creating version: {}".format(description))
        return self.client.publish_version(
            FunctionName=self.name,
            Description=description
        )
    
    def update_env_variables(self,variables):
        print("Updating environment variables")
        return self.client.update_function_configuration(
            FunctionName=self.name,
            Environment = {
                "Variables": variables
            }
        )