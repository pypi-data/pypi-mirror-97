import pickle
from os.path import isfile
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def google_login(google_credentials_filepath: str = "credentials.json"):
    '''
    Default filename of google_credentials_filepath:
    credentials.json

    Download credentials.json from "Turn on the Google Sheets API":
    https://developers.google.com/sheets/api/quickstart/python
    '''
    if not isfile(google_credentials_filepath):
        msg = "There is an error with google_login() in google_login.py. The file does not exist in path."
        raise Exception(msg)

    # Enable Google Sheets API and download client configuration
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=google_credentials_filepath,
        scopes=SCOPES,
    )

    # creds is google.oauth2.credentials.Credentials type
    creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
