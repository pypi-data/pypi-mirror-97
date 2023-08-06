#!/usr/bin/env python3

import boto3

def get_secret(secret_name, region_name):

    secret_name = secret_name
    region_name = region_name

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    return secret