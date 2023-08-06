import base64
import json

from botocore.exceptions import ClientError

import boto3
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig

from .base_secret import Secret


class AWSSecret(Secret):
    def retrieve_secret(self, service_name: str, env: str, region_name: str="us-west-2"):
        secret_name = f"{env}/{service_name}"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=region_name
        )

        try:
            # Create a cache
            cache = SecretCache(SecretCacheConfig(), client)

            # Get secret string from the cache
            secret_value_response = cache.get_secret_string(secret_name)

        except ClientError as e:
            raise e
        else:
            return json.loads(secret_value_response)
