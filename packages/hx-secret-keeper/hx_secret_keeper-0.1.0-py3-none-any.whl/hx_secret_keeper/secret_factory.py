from .aws_secret import AWSSecret
from .azure_secret import AzureSecret


class SecretFactory(object):
    def get_secret_client(self, cloud: str="aws"):
        if cloud == "aws":
            return AWSSecret()
        else:
            return AzureSecret()
