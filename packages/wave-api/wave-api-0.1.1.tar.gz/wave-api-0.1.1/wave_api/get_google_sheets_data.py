from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from typing import List
from wave_api.google_sheets_login import google_sheets_login


def get_google_sheets_data(
    google_sheets_id: str,
    google_sheets_name: str,
    google_credentials_filepath: str,
    token_auth_filename: str = 'token.pickle',
) -> List[List[str]]:
    '''
    Your Google authorization .json file can be downloaded:
    https://developers.google.com/sheets/api/quickstart/python

    Default file name is: credentials.json
    google_sheets_login() will then save a token.pickle file to disk
    '''
    creds = None
    # Load .pickle file with Google Sheets authorization
    # (Only need to do this once)
    if os.path.exists(token_auth_filename):
        with open(token_auth_filename, mode='rb') as token_auth_file:
            creds = pickle.load(token_auth_file)
    # Let user log in (if authorization is not valid) and save .pickle file
    if not creds or not creds.valid:
        google_sheets_login(creds, google_credentials_filepath)

    # Call Google Sheets API and get dictionary of spreadsheet
    service = build(serviceName='sheets', version='v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=google_sheets_id,
        range=google_sheets_name,
    ).execute()

    # Return empty array if can't findresult['values']
    values = result.get('values', [])
    if not values:
        return [['No data found']]
    return values
