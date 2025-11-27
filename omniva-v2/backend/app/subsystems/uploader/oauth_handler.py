"""
OAuth utilities for authenticating with the YouTube Data API.
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


class OAuthHandler:
    """Manage OAuth credentials stored in storage/oauth/."""

    def __init__(self) -> None:
        self.cred_dir = os.path.join("storage", "oauth")
        os.makedirs(self.cred_dir, exist_ok=True)

        self.client_secret = os.path.join(self.cred_dir, "client_secret.json")
        self.token_path = os.path.join(self.cred_dir, "token.json")

    def get_credentials(self) -> Credentials:
        """Return valid credentials, kicking off browser flow if needed."""
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secret, SCOPES)
                creds = flow.run_local_server(port=8085)

            with open(self.token_path, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())

        return creds
