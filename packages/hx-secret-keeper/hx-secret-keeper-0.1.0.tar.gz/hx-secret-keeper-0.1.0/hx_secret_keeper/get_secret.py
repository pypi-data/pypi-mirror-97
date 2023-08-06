from .secret_factory import SecretFactory

def get_secret(cloud, region, env, service_name):
    """
    Function to retrieve secrets.

    Parameters:
    cloud (str): Cloud Provider. Currently supports "aws" and "azure"
    region (str): Cloud Provider Region.
    env (str): Can take one of "dev", "staging", "greenprod" or "blueprod" values
    service_name (str): Resource for which the secret is required

    Returns:
    secret_value (json)
    """

    # Input validation
    if cloud not in ["aws", "azure"]:
        raise ValueError("Cloud Provider Not Supported. Use either 'aws' or 'azure'")
    if env not in ["dev", "staging", "greenprod", "blueprod"]:
        raise ValueError("Use one of 'dev', 'staging', 'greenprod' or 'blueprod'")

    secret_client = SecretFactory().get_secret_client(cloud=cloud)
    return secret_client.retrieve_secret(service_name, env, region)
