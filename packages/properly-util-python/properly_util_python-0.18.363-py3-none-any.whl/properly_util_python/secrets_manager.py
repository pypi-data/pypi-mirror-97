import base64
import json
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def get_secret(
        secret_name: str,
        stage: str = None,
) -> dict:
    """
    Gets a secret from the AWS Secrets Manager
    It will look for the secret with the name in the following pattern: `{stage}-{secret name}`

    :param secret_name: The name of the secret in AWS Secrets Manager.
    :param stage: (Optional) The stage name of the system environment.
                  Defaults to the environment variable "PROPERLY_STAGE".
    :return: The dictionary of secrets.
    """

    if not stage:
        stage = os.environ["PROPERLY_STAGE"]

    secret_name = f"{stage}-{secret_name}"
    secret = get_from_secrets_manager(secret_name)

    return json.loads(secret)


def get_from_secrets_manager(secret_name: str) -> Optional[str]:
    """
    Gets the secret from AWS Secrets Manager.
    This code is mostly supplied by AWS.

    :param secret_name: The name of the secret.
    :return: The string representation of the secret value.
    """
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the "GetSecretValue" API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can"t decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
            return secret

        secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        return secret
