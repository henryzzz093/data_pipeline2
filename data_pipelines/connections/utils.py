import boto3
import logging
import json


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Parameters:
    """
    Used to access paramters stored in AWS Systems Manager Parameter Store.
    """

    def __init__(self, region="us-west-2"):
        self.client = boto3.client("ssm", region_name=region)
        self.log = logger

    def get(self, parameter_id):
        if parameter_id:
            self.log.info(f"Requesting parameters: {parameter_id}")
            name = f"/airflow/{parameter_id}"
            response = self.client.get_parameter(
                Name=name,
                WithDecryption=True,
            )
            value = response.get("Parameter").get("Value")
            return json.loads(value)
        return {}


if __name__ == "__main__":
    A = Parameters()
    print(A.get("mysql_local"))
