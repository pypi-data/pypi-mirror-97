"""

"""
"""
    AWS Auth utilities
"""
import base64
import boto3

def get_aws_ecr(region: str):
    # this loads AWS access token and secret from env and returns an ECR client
    ecr_client = boto3.client('ecr', region_name=region)
    # get login token
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    password = base64.b64decode(token["authorizationData"][0]["authorizationToken"]).decode().split(":")[1]
    registry = token['authorizationData'][0]['proxyEndpoint']
    # return docker credentials
    return username, password, registry
