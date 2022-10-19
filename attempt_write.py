from __future__ import print_function
from calendar import c

import os.path
import numpy as np
import pandas as pd

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# API access info
# CLINET_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id_hockey = '049ffb2a69b7c97b99ec51811db2cb09eb7c52b2c26d6a461de37da6f3f3438a@group.calendar.google.com'

def main():
    """SJ Adult hockey schedule
    Read and Write Scheduled Games for hockey adult league.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # build gCal API service
        service = build(API_NAME, API_VERSION, credentials=creds)
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        
        # Call the Calendar API, Get Hockey list
        list_name = []
        list_date = []
        page_token = None
        
        while True:
            events = service.events().list(calendarId=calendar_id_hockey, pageToken=page_token).execute()
            for event in events['items']:
                start = event['start'].get('dateTime', event['start'].get('date'))
                start = datetime.strptime(start,"%Y-%m-%dT%H:%M:%S%z")
                list_name.append(event['summary'])
                list_date.append(start)
                page_token = events.get('nextPageToken')
            if not page_token:
                break
        
        cal_df = pd.DataFrame({'description':list_name,
                               'date':list_date}) 
        print(cal_df)
        
        # TODO: call hockey_game_scraper.py, get upcoming games
        
        # TODO: Upload filtered Hockey list to calendar
        print('Create Hockey Schedule')
        event = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2022-10-22T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2022-10-22T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 60},
            ],
        },
        }
        event = service.events().insert(calendarId=calendar_id_hockey, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        
        # TODO: Delete Old Hockey games from calendar
        
        
        
    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()
    
