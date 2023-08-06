from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from typing import List


def get_google_sheets_data(
    google_sheets_id: str,
    google_sheets_name: str,
    token_auth_file: str = 'token.pickle',
) -> List[List[str]]:
    '''
    To get token.pickle file:
    1. Head over to https://developers.google.com/sheets/api/quickstart/python
    2. Download credentials.json file under "Turn on the Google Sheets API"
    3. Run .google_login("credentials.json")
    '''
    # Load .pickle file with Google Sheets authorization
    creds = None
    if os.path.exists(token_auth_file):
        with open(token_auth_file, mode='rb') as token:
            creds = pickle.load(token)

    # Refresh credentials if not valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            msg = "There is an error with get_google_sheets_data() in get_google_sheets_data.py"
            raise Exception(msg)

    # Call Google Sheets API and get dictionary of spreadsheet
    service = build(serviceName='sheets', version='v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=google_sheets_id,
        range=google_sheets_name,
    ).execute()

    # Return empty array if can't findresult['values']
    google_sheets_data = result.get('values', [])
    if not google_sheets_data:
        return [['No data found']]
    return google_sheets_data
