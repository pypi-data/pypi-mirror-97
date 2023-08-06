import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import TypeVar

GOOGLE_AUTH_CRED = TypeVar('google.oauth2.credentials.Credentials')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
GOOGLE_CREDENTIALS_FILENAME = 'credentials.json'


def google_sheets_login(
    creds: GOOGLE_AUTH_CRED,
    google_credentials_filepath: str,
) -> None:
    '''
    The default filename of google_credentials_filepath is credentials.json
    '''
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Enable Google Sheets API and download client configuration
        flow = InstalledAppFlow.from_client_secrets_file(
            google_credentials_filepath,
            SCOPES,
        )
        creds = flow.run_local_server(port=0)

    # Save Google Sheets API authorization as .pickle file
    with open('token.pickle', 'wb') as token_auth_file:
        pickle.dump(creds, token_auth_file)
