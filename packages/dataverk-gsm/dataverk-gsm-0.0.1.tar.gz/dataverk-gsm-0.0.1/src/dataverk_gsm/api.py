import os
import google.auth

from google.cloud import secretmanager


def _set_secret(sm_client: secretmanager.SecretManagerServiceClient, secret: str):
    name = secret.split("/")[-1]
    value = sm_client.access_secret_version(name=secret+"/versions/latest").payload.data.decode("utf-8")
    os.environ[name] = value


def set_secrets_as_envs():
    sm_client = secretmanager.SecretManagerServiceClient()
    _, project_id = google.auth.default()
    secrets = [secret.name for secret in list(sm_client.list_secrets(parent=f"projects/{project_id}"))]
    for secret in secrets:
        _set_secret(sm_client, secret)
