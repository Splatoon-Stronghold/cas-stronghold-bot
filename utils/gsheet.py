from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_service(creds : Credentials):
    return build('sheets', 'v4', credentials=creds)

def get_sheet_data(service, id, range, roles):
    sheets = service.spreadsheets()
    result = (
        sheets.values()
        .get(spreadsheetId=id, range=range)
        .execute()
    )

    if roles:
        return result['values'][1:]
    else:
        return result['values']
