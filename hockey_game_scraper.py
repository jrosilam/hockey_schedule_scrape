import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime as dt
from urllib.parse import urlparse
import os

## functions
def get_sublinks(dict_links,url_main_league,team_names):
    page_hockey_main = requests.get(url_main_league)
    soup_main = BeautifulSoup(page_hockey_main.content,"html.parser")
    link_names = soup_main.find_all('a',href=True)
    ## parse data for table finder
    parsed = urlparse(url_main_league)
    for link in link_names:           
        for name in team_names:                
            if link.text.strip()==name:
                hockey_url = parsed.scheme + '://' + parsed.netloc + '/' + link['href']
                dict_links['team_name'].append(name)
                dict_links['href_link'].append(hockey_url)
    return dict_links

def get_schedule(dict_links,df_all_teams):
    # get tables and clean
    for index_, trash_man in enumerate(dict_links):
        team_name  = dict_links['team_name'][index_]
        hockey_url = dict_links['href_link'][index_]
        print(f"Index: {index_}, Team Name: {team_name}, URL: {hockey_url}")
        hockey_url_check = requests.get(hockey_url)
        soup = BeautifulSoup(hockey_url_check.content,"html.parser")
        tables = soup.find_all('table')

        ## read table and fix data
        df_hockey_games = pd.read_html(str(tables[0]), flavor='bs4')[0]
        df_hockey_games = df_hockey_games.droplevel(0,axis=1)
        df_hockey_games.reset_index(inplace=True)
        df_hockey_games.rename(columns={'Goals':'Goals_Away','Goals.1':'Goals_Home'},inplace=True)
        df_hockey_games.head()
        df_hockey_games.replace("NaN", np.nan, inplace = True)
        df_hockey_games.drop(columns=['Box Score','Scoresheet'],inplace=True)

        ## get datetime
        current_year = pd.to_datetime('today').strftime('%Y')
        current_datetime = pd.DataFrame([df_hockey_games['Date'] + ' ' + current_year + ' ' + df_hockey_games['Time']]).T
        current_datetime.columns = ['Date_Time']
        current_datetime_fix = pd.to_datetime(current_datetime['Date_Time'], format = '%a %b %d %Y %I:%M %p')
        df_hockey_games['Game_datetime'] = current_datetime_fix

        ## get bench and jersey color
        idx_team_side = df_hockey_games['Home'] == team_name
        df_hockey_games['Team_side'] = pd.DataFrame(np.where(idx_team_side,'Home','Away'))
        df_hockey_games['Jersey']    = pd.DataFrame(np.where(idx_team_side,'Light','Dark'))

        ## playing against
        df_hockey_games['vs_team'] = pd.concat([df_hockey_games['Home'][~idx_team_side],df_hockey_games['Away'][idx_team_side]]).sort_index()

        ## see if there is games left
        df_hockey_games['Upcoming_game'] = pd.to_datetime('today') < df_hockey_games['Game_datetime']
        
        ## fix goals and determine shootout
        shootout_decider = pd.DataFrame([df_hockey_games['Goals_Home'].astype(str).str[-1] == 'S'] or [df_hockey_games['Goals_Away'].astype(str).str[-1] == 'S']).T

        # add category for Shoot_out_win_home/away or False
        df_hockey_games['Shootout_decider'] = shootout_decider
        df_hockey_games['Goals_Home'] = df_hockey_games['Goals_Home'].astype(str).str.extract('(\d+)')
        df_hockey_games['Goals_Away'] = df_hockey_games['Goals_Away'].astype(str).str.extract('(\d+)')

        ## game time pretty format
        df_hockey_games['Game_datetime_neat'] = df_hockey_games['Game_datetime'].dt.strftime('%a, %b %d @ %I:%M %p')
        df_hockey_games.drop(['Date','Time'], axis = 1, inplace=True)

        ## Clean Rink Names, add team_name
        df_hockey_games['Rink'] = df_hockey_games['Rink'].str.replace('San Jose ','')
        df_hockey_games['team_name'] = team_name
        df_all_teams = pd.concat([df_all_teams,df_hockey_games])

    ## clean data        
    ## reorder
    cols_to_order = ['index', 'Game', 'team_name', 'vs_team', 'Team_side', 'Goals_Home', 'Goals_Away', 'Shootout_decider', 'Game_datetime_neat', 'Rink', 'Jersey']
    new_columns = cols_to_order + (df_all_teams.columns.drop(cols_to_order).tolist())
    df_all_teams = df_all_teams[new_columns]
    df_all_teams

    ## subq-date
    schedule_data = df_all_teams.loc[:,['team_name', 'vs_team', 'Team_side', 'Upcoming_game', 'Goals_Home', 'Goals_Away', 'Shootout_decider', 'Game_datetime', 'Game_datetime_neat', 'Rink', 'Jersey']]
    schedule_data.sort_values(by='Game_datetime', ascending=True, inplace=True)
    schedule_data.reset_index(inplace=True)
    # schedule_data.drop(columns='Game_datetime',inplace=True)

    ## remaining games
    schedule_data_remaining = schedule_data.loc[schedule_data['Upcoming_game']].reset_index().drop(columns = ['Upcoming_game','index', 'Goals_Home', 'Goals_Away'])
    
    ## return data_frames
    return df_all_teams, schedule_data, schedule_data_remaining

def print_save(df_all_teams,schedule_data,schedule_data_remaining):

    ## print to terminal stuff
    print(df_all_teams)
    
    print('\nAll Team Schedule')
    print(schedule_data)

    print('\nAll Team Schedule, games left')
    print(schedule_data_remaining)

    print(f"\nSchedule pulled on \"{pd.to_datetime('today').strftime('%a %b %d %Y %I:%M %p')}\"")
    
    ## print to csv
    outdir = './csv'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    print(f"\nSchedules printed in \"{os.getcwd()}\"\n")
    schedule_data.to_csv('csv/all_team_schedule.csv',index=False)
    schedule_data_remaining.to_csv('csv/all_team_schedule_remaining.csv',index=False)

def run_scraper(team_names,url_main_league):
    # make empty dicts or dfs
    dict_links = {'team_name':[],'href_link':[]} # empty dict
    df_all_teams = pd.DataFrame() # empty df

    # get sublinks
    dict_links = get_sublinks(dict_links,url_main_league,team_names)

    # get all schedules
    df_all_teams, schedule_data, schedule_data_remaining = get_schedule(dict_links,df_all_teams)

    # print schedules
    print_save(df_all_teams,schedule_data,schedule_data_remaining)
    return schedule_data, schedule_data_remaining

if __name__ == '__main__':
    ## Given Items & Just Change Team Names!
    # find schedules for these teams
    team_names = ['Team Beer','Team America']
    # main hockey URL page
    url_main_league = 'https://stats.sharksice.timetoscore.com/display-stats.php?league=1'
    run_scraper(team_names,url_main_league)