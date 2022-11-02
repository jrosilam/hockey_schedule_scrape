from __future__ import print_function
from calendar import c

import hockey_game_scraper
import os.path
import numpy as np
import pandas as pd

from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

## Given Items & Just Change Team Names!
# delete old hockey games?
remove_old_hockey = False
# find schedules for these teams
team_names = ['Team Beer','Team America']
# main hockey URL page
url_main_league = 'https://stats.sharksice.timetoscore.com/display-stats.php?league=1'
# ice rink hockey SJ
address_hockey = '1500 S 10th St, San Jose, CA 95112'

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
        now = pd.to_datetime('today')
        
        # Call the Calendar API, Get Hockey list
        list_name = []
        list_date = []
        list_id = []
        page_token = None
        
        while True:
            events = service.events().list(calendarId=calendar_id_hockey, pageToken=page_token).execute()
            for event in events['items']:
                start = event['start'].get('dateTime', event['start'].get('date'))
                start = datetime.strptime(start,"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
                list_name.append(event['summary'])
                list_date.append(start)
                list_id.append(event['id'])
                page_token = events.get('nextPageToken')
            if not page_token:
                break
        
        cal_df = pd.DataFrame({'description':list_name,
                               'date':list_date, 
                               'id':list_id})
        print(cal_df)
        
        # call hockey_game_scraper.py, get games
        schedule_data, schedule_data_remaining = hockey_game_scraper.run_scraper(team_names,url_main_league)
        # compare hockey list
        add_index = ~schedule_data['Game_datetime'].isin(cal_df['date'])
        delete_index = cal_df['date'] < now
        # send new events to calendar
        if not any(add_index):
            print("No new hockey games to add")
        else:
            print('Create Hockey Schedule')
            for index, record in schedule_data[add_index].iterrows():
                # TO-DO: separate to dif function and update old games (delete and rewrite)
                # TO-DO: add shootout win/loss, leave empty if they forced to take tie
                if record['Upcoming_game']:
                    summary_str = f"{record['team_name']} Vs. {record['vs_team']}"
                else:
                    goals_for = np.where(record['Team_side'] == 'Home', record['Goals_Home'], record['Goals_Away'])
                    goals_against = np.where(record['Team_side'] != 'Home', record['Goals_Home'], record['Goals_Away'])
                    summary_str = f"{record['team_name']} ({goals_for}) Vs. {record['vs_team']} ({goals_against})"
                event = {
                'summary': summary_str,
                'location': address_hockey,
                'description': f"Rink: {record['Rink']}\nJersey: {record['Jersey']}\nBench: {record['Team_side']}",
                'start': {
                    'dateTime': record['Game_datetime'].strftime("%Y-%m-%dT%H:%M:%S%z"),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': (record['Game_datetime'] + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S%z"),
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
                print(f"{index} Event created: {(event.get('htmlLink'))}")
        
        # Delete Old Hockey games from calendar
        if remove_old_hockey:
            if not any(delete_index):
                print("No new hockey games to add")
            else:
                print('Delete Old Hockey Schedule')
                for index, record in cal_df[delete_index].iterrows():
                    service.events().delete(calendarId=calendar_id_hockey, eventId=record['id']).execute()
                    print(f"{index} Event deleted: {record['description']} @ {record['date']}")
        
    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
        main()