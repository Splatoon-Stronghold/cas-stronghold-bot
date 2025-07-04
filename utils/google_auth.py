import os.path
from pathlib import Path
from typing import Tuple

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

base_path = (Path(os.path.abspath(__file__)) / ".." / "..").resolve()
app_creds_path = base_path / "cas-bot-api-gsheet.json"
auth_path = base_path / "token.json"


def get_authentication() -> Credentials | None:
    """
    Gets the authentication if present, otherwise none.

    Parameters
    ----------
    None - reads from file

    Returns
    -------
    creds : Credentials or None
        Authenticated credentials if present, otherwise returns None
    """
    # needs to be refactored to accept scope as function input
    if os.path.exists(auth_path):
        try:
            creds = Credentials.from_authorized_user_file(auth_path, SCOPES)
        except Exception as e:
            print(f"Exception: {e}")
            return None

    else:
        print("No auth path")
        return None

    if not creds or not creds.valid:
        print("Invalid")
        return None
    else:
        return creds


def get_authentication_link(scopes: list[str]) -> Tuple[str, Flow]:
    """
    Gets the necessary authentication link along with its flow.

    Parameters
    ----------
    SCOPES : list[str]
        A list of the required scopes

    Returns
    -------
    auth_url : str
        The url for the user to get their token
    flow : Flow
        The google authentication flow after generating the link.
    """
    # returns the authentication link from a given flow
    flow = Flow.from_client_secrets_file(app_creds_path, scopes, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
    auth_url, _ = flow.authorization_url()
    return auth_url, flow


def get_new_auth(flow: Flow, code: str) -> Credentials:
    """
    Authenticates the bot and saves the token.

    Parameters
    ----------
    flow : Flow
        The google authentication flow after generating the link.
    code : str
        The authentication token recieved by the user.

    Returns
    -------
    creds : Credentials
        The authenticated credentials.
    """
    # stores the auth to the json file
    flow.fetch_token(code=code)
    creds = flow.credentials

    with open(auth_path, "w") as token:
        token.write(creds.to_json())

    return creds
