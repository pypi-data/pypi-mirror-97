from .base_secret import Secret


class AzureSecret(Secret):
    def retrieve_secret(self, service_name: str, env: str, region_name: str="us-west-2"):
        raise NotImplementedError
