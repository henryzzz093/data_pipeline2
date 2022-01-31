import boto3


if __name__ == "__main__":
    client = boto3.client("ssm", region_name="us-west-2")
    response = client.get_parameter(Name="/airflow/test", WithDecryption=True)
    print(response)
