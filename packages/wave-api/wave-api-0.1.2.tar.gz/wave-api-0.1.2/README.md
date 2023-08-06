# Wave API

Wave (waveapps.com) does not have an API. However, they do have a Google Sheets API. This is a Python API for your Wave Google Sheets document.

Note that you will have to manually use the Wave Google Sheets API to update your Google Sheets document.

# How to install

```pip3 install wave-api```

# Before getting started 

Head over to https://developers.google.com/sheets/api/quickstart/python.

Under "Turn on the Google Sheets API", enable the Google Sheets API and download the credentials.json file.


# Getting started

```
import wave_api as wave
import pandas as pd
from os.path import isfile
from datetime import datetime

# Log in for Google Sheets authentication
if not isfile("token.pickle"):
    wave.google_login("credentials.json")

# Get Google Sheets data
GOOGLE_SHEETS_ID = "Some Long String"  # Change this
GOOGLE_SHEETS_NAME = "Some String"  # Change this
google_sheets_data = wave.get_google_sheets_data(GOOGLE_SHEETS_ID, GOOGLE_SHEETS_NAME, "token.pickle")

# Convert dates into Wave's date format
df = pd.DataFrame(data=google_sheets_data)
dates = [datetime(2021, 1, 31), datetime(2020, 12, 31)]  # Change this
wave_dates = wave.date_settings(df, dates)

# Set options
metrics = ["Seedin Investment", "UOB One (Tuition)"]  # Change this
options = wave.Options('Monthly', metrics, wave_dates)

# Get dictionary of data
dictionary = wave.create_portfolio(df=df, options=options)
print(dictionary)
```
