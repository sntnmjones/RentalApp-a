import boto3
from logging import getLogger
from main.utils.common_utils import is_prod

class Ddb:
    def __init__(self):
        self.logger = getLogger()
        self._client = boto3.client('dynamodb') if is_prod() else boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000', region_name='us-west-2')

