from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build


def get_service(creds: Credentials) -> Resource:
    """
    Gets sheets service.

    Parameters
    ----------
    creds: Credentials
        Google authentication credentials.

    Returns
    -------
    service : Resource
        A v4 sheets, authenticates service.
    """
    return build("sheets", "v4", credentials=creds)


def get_sheet_data(service: Resource, id: str, range: str, roles: bool) -> list[list[str]]:
    """
    Gets data from a google sheet.

    Parameters
    ----------
    service : Resource
        The sheets authenticated service to use.
    id : str
        The id of the google sheet.
    range : str
        The range to use. Can just be the name of the tab for the sheet being considered.
    roles : bool
        Removes the first row - so that column names are not in the data.

    Returns
    -------
    result : list[list[str]]
        The google sheet data requested.
    """
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=id, range=range).execute()

    if roles:
        return result["values"][1:]
    else:
        return result["values"]
