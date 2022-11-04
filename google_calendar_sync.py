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
# add old hockey games?
add_old_flag = True
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

now_dt = pd.to_datetime('today').to_pydatetime()

def get_cal_event(service):
    # Call the Calendar API, Get Hockey list
    list_name = []
    list_date = []
    list_id = []
    list_upcoming = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id_hockey, pageToken=page_token).execute()
        for event in events['items']:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = datetime.strptime(start,"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
            list_name.append(event['summary'])
            list_date.append(start)
            list_id.append(event['id'])
            list_upcoming.append(now_dt < start)
            page_token = events.get('nextPageToken')
        if not page_token:
            break
    
    cal_df = pd.DataFrame({'description':list_name,
                            'date':list_date, 
                            'id':list_id,
                            'Upcoming_game':list_upcoming})
    print(cal_df)
    return cal_df
    
def get_hockey_event(cal_df):
    # call hockey_game_scraper.py, get games
    schedule_data, schedule_data_remaining = hockey_game_scraper.run_scraper(team_names,url_main_league)
    # compare hockey list
    add_index = ~schedule_data['Game_datetime'].isin(cal_df['date'])
    delete_index = cal_df['date'] < now_dt
    return schedule_data, add_index, delete_index

def create_event(service,schedule_data,add_index,add_old_flag):
    create_update_str = 'Create'
    if add_old_flag:
        create_update_str = 'Update'
    print(f"{create_update_str} Hockey Schedule")
    for index, record in schedule_data[add_index].iterrows():
        # skip old games from populating 
        add_index[index] = False
        # add flag to add old games
        # think this thru lol.
        if add_old_flag:
            pass
        elif not record['Upcoming_game']:
            continue
        
        if record['Team_side'] == 'Home':
            str_split_bench = 'Vs.'
        else:
            str_split_bench = '@'
            
        summary_str = f"{record['team_name']} {str_split_bench} {record['vs_team']}"
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
        print(f"{index} Event {create_update_str}: {(event.get('htmlLink'))}")

def update_event(service,cal_df,schedule_data):
    cal_joined_df = cal_df.merge(schedule_data, left_on = 'date', right_on = 'Game_datetime')
    for index, record in cal_joined_df.iterrows():
        if record['Upcoming_game_x']:
            continue
        
        # get existing cal event
        event = service.events().get(calendarId=calendar_id_hockey, eventId=record['id']).execute()

        #Update old schedule
        goals_for = np.where(record['Team_side'] == 'Home', record['Goals_Home'], record['Goals_Away'])
        goals_against = np.where(record['Team_side'] != 'Home', record['Goals_Home'], record['Goals_Away'])
        
        if record['Team_side'] == 'Home':
            str_split_bench = 'Vs.'
        else:
            str_split_bench = '@'
            
        summary_str = f"{record['team_name']} ({goals_for}) {str_split_bench} {record['vs_team']} ({goals_against})"
        
        # check if event has been updated
        if (event['summary'] == summary_str):
            continue
        
        # change summary label
        event['summary'] = summary_str
        
        # update event
        updated_event = service.events().update(calendarId=calendar_id_hockey, eventId=event['id'], body=event).execute()

        print(f"{index} Event updated: {(updated_event.get('htmlLink'))}")
    
def remove_event(service,cal_df,delete_index):
    # Delete Old Hockey games from calendar
    print('Delete Old Hockey Schedule')
    for index, record in cal_df[delete_index].iterrows():
        # remove old events to calendar
        service.events().delete(calendarId=calendar_id_hockey, eventId=record['id']).execute()
        print(f"{index} Event deleted: {record['description']} @ {record['date']}")

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

        # get calendar event info 
        cal_df = get_cal_event(service)
        
        # get hockey game info
        schedule_data, add_index, delete_index = get_hockey_event(cal_df)
        
        # add only new games
        create_event(service,schedule_data,add_index,False)
        
        # delete all old games
        if remove_old_hockey:
            remove_event(service,cal_df,delete_index)
        else:
            # update/add old games with scores
            create_event(service,schedule_data,add_index,add_old_flag)
            cal_df = get_cal_event(service)
            update_event(service,cal_df,schedule_data)
        
    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
        main()