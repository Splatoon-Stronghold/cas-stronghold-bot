import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

base_path = (Path(os.path.abspath(__file__)) / ".." / "..").resolve()
app_creds_path = base_path / "cas-bot-api-gsheet.json"
auth_path = base_path / "token.json"




def get_authentication():
   # returns creds if auth
   # returns None if not
    if os.path.exists(auth_path):
        try:
            creds = Credentials.from_authorized_user_file(auth_path, SCOPES)
        except Exception as e:
           print(f'Exception: {e}')
           return None

    else:
       print('No auth path')
       return None

    if not creds or not creds.valid:
       print('Invalid')
       return None
    else:
       return creds



def get_authentication_link(SCOPES):
   # returns the authentication link from a given flow
   flow = Flow.from_client_secrets_file(
        app_creds_path, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob'
   )
   auth_url, _ = flow.authorization_url()
   return auth_url, flow


def get_new_auth(flow: Flow, code : str):
   # stores the auth to the json file
   flow.fetch_token(code=code)
   creds = flow.credentials

   with open(auth_path, "w") as token:
      token.write(creds.to_json())

   return creds
