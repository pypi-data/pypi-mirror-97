# Copyright 2020 Okera Inc. All Rights Reserved.

import boto3
import botocore
import requests

from botocore.credentials import DeferredRefreshableCredentials, CredentialProvider

class OkeraException(Exception):
    pass

class OkeraCredentialProvider(CredentialProvider):
    CANONICAL_NAME = "okera-aws-creds"

    def __init__(self, rest_api_url, token):
        super().__init__()
        self._okera_rest_api_url = rest_api_url.rstrip('/')
        self._okera_token = token

    def load(self):
        creds = DeferredRefreshableCredentials(refresh_using=self._refresh, method="sts-assume-role")
        return creds

    def _refresh(self):
        response = self._custom_aws_cred_refresh()
        credentials = {
            "access_key": response.get("key"),
            "secret_key": response.get("secret"),
            "expiry_time": response.get("expiry"),
            "token": None,
        }
        return credentials

    def _custom_aws_cred_refresh(self):
        api_url = "%s/%s" % (self._okera_rest_api_url, "api/v2/aws-tokens")
        headers = {"Authorization": "Bearer %s" % self._okera_token}
        res = requests.post(api_url, headers=headers)
        if res.status_code in (401, 403):
            raise OkeraException("Error in authenticating credentials request: %s" % res.text)
        else:
            return res.json()

def okera_session(session, token, rest_uri, proxy_uri):
    bc_session = session._session
    boto3_session = session

    cred_provider = bc_session.get_component('credential_provider')
    cred_provider.insert_before('env', OkeraCredentialProvider(rest_uri, token))
    config = botocore.config.Config(
        proxies={'https': proxy_uri})

    orig_config = bc_session.get_default_client_config()
    if not orig_config:
        orig_config = botocore.config.Config()

    bc_session.set_default_client_config(orig_config.merge(config))

    return boto3_session