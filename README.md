# hockey_schedule_scrape Git Repo
This was made by [Jesus R Rosila Mares](https://github.com/jrosilam) to find hockey schedule and plan better.   
(aswell as figure out what jersey color we are)

# Table of Contents
- [hockey_schedule_scrape Git Repo](#hockey-schedule-scrape-git-repo)
- [Table of Contents](#table-of-contents)
- [To-Do](#to-do)
- [New User](#new-user)
- [Example](#example)
  * [How to use:](#how-to-use-)
  * [Expected Input:](#expected-input-)
  * [Expected Output:](#expected-output-)
    + [Terminal Output:](#terminal-output-)
    + [Google Calendar Output:](#google-calendar-output-)
      - [With `remove_old_hockey = False`](#with--remove-old-hockey---false-)
      - [With `remove_old_hockey = True`](#with--remove-old-hockey---true-)

# To-Do
- [ ] Make job to run every morning.
- [ ] Update cal for old games showing scores
- [ ] Update cal for Team A vs. Team B and/or Team A @ Team B.
- [ ] Streamline Calendar generation for new users.
- [ ] finish new user section.

# New User
[python google cal API setup](https://developers.google.com/calendar/api/quickstart/python)

Fill this in later.

# Example
## How to use:
Just edit `team_names` in `google_calendar_sync.py` and run!   
The following should populate, terminal print statments   
And saved `csv/*.csv` files named:   
- `all_team_schedule.csv`
- `all_team_schedule_remaining.csv`

## Expected Input:
Adjust teamnames to whatever team you are using.  
If you want to delete old events.
```py 
## Given Items & Just Change Team Names!
# delete old hockey games?
remove_old_hockey = False
# find schedules for these teams
team_names = ['Team Beer','Team America']
# main hockey URL page
url_main_league = 'https://stats.sharksice.timetoscore.com/display-stats.php?league=1'
# ice rink hockey SJ
address_hockey = '1500 S 10th St, San Jose, CA 95112'
```
Edit `calendar_id_hockey` and create a `credentials.json` from [here](https://developers.google.com/calendar/api/quickstart/python)!   
Skip *Configure the sample* and *Run the sample*.
```py
# API access info
# CLINET_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id_hockey = '049ffb2a69b7c97b99ec51811db2cb09eb7c52b2c26d6a461de37da6f3f3438a@group.calendar.google.com'
```

## Expected Output:
### Terminal Output:
```terminal
                           description                date                          id
0       Team Beer Vs. Seal Team Sticks 2022-10-22 21:30:00  cir77fqoo0ailipkannthsbrl4
1    Team America Vs. Beerbears on Ice 2022-09-10 20:00:00  tl58gd6i5991c7bhie1bbclmu4
2      Team America Vs. Cereal Killers 2022-09-19 23:15:00  ie8u3ne90lsdsn1sh589cnkhm8
3    Team America Vs. Beerbears on Ice 2022-09-25 17:45:00  nrassa7m9idi7egdttep80stu8
4        Team Beer Vs. Choking Hazards 2022-09-26 22:30:00  qo29padgdjvq76sm7182co4cgc
5            Team America Vs. Stampede 2022-09-28 21:45:00  843gji2arq3teq1dalddgolts8
6          Team Beer Vs. Buffalo Wings 2022-10-02 20:45:00  4u920hopvhirqg06h4qecj2bg8
7          Team Beer Vs. Schrute Farms 2022-10-09 18:00:00  gjvcg8k4ebpf1925b63hp2m1j4
8             Team America Vs. K-Wings 2022-10-09 21:00:00  brnvm9gtrkqg5fvqi4fnttckak
9        Team Beer Vs. 3rd Line Scrubs 2022-10-16 19:00:00  8se07k2a79jn4528n5ebam96v8
10  Team America Vs. Kraken More Beers 2022-10-18 23:15:00  qmsvo51pemg99usogromfqmsd0
Index: 0, Team Name: Team America, URL: https://stats.sharksice.timetoscore.com/display-schedule?team=2297&season=55&league=1&stat_class=1
Index: 1, Team Name: Team Beer, URL: https://stats.sharksice.timetoscore.com/display-schedule?team=4637&season=55&league=1&stat_class=1
   index     Game     team_name            vs_team      Game_datetime_neat        Rink  ...              Home Goals_Home       Type       Game_datetime Shootout_decider Upcoming_game
0      0  328022*  Team America   Beerbears on Ice  Sat, Sep 10 @ 08:00 PM        Grey  ...  Beerbears on Ice          3  Regular 1 2022-09-10 20:00:00             True         False  
1      1  354475*  Team America     Cereal Killers  Mon, Sep 19 @ 11:15 PM        Grey  ...      Team America          4  Regular 2 2022-09-19 23:15:00            False         False  
2      2  351696*  Team America   Beerbears on Ice  Sun, Sep 25 @ 05:45 PM      Sharks  ...  Beerbears on Ice          3  Regular 3 2022-09-25 17:45:00            False         False  
3      3  360402*  Team America           Stampede  Wed, Sep 28 @ 09:45 PM   White (C)  ...          Stampede          2  Regular 4 2022-09-28 21:45:00            False         False  
4      4  369297*  Team America            K-Wings  Sun, Oct 09 @ 09:00 PM  Orange (N)  ...           K-Wings          1  Regular 5 2022-10-09 21:00:00            False         False  
5      5  343483*  Team America  Kraken More Beers  Tue, Oct 18 @ 11:15 PM        Grey  ...      Team America          6  Regular 6 2022-10-18 23:15:00            False         False  
0      0  355546*     Team Beer      Flying Pandas  Sat, Sep 03 @ 09:45 PM  Orange (N)  ...     Flying Pandas          4  Preseason 2022-09-03 21:45:00             True         False  
1      1  341373*     Team Beer    Choking Hazards  Mon, Sep 26 @ 10:30 PM      Sharks  ...         Team Beer          2  Regular 1 2022-09-26 22:30:00            False         False  
2      2  351841*     Team Beer      Buffalo Wings  Sun, Oct 02 @ 08:45 PM      Sharks  ...     Buffalo Wings          1  Regular 2 2022-10-02 20:45:00            False         False  
3      3  351908*     Team Beer      Schrute Farms  Sun, Oct 09 @ 06:00 PM        Grey  ...         Team Beer          2  Regular 3 2022-10-09 18:00:00            False         False  
4      4  369302*     Team Beer    3rd Line Scrubs  Sun, Oct 16 @ 07:00 PM        Grey  ...   3rd Line Scrubs          5  Regular 4 2022-10-16 19:00:00            False         False  
5      5   350303     Team Beer   Seal Team Sticks  Sat, Oct 22 @ 09:30 PM      Sharks  ...         Team Beer        NaN  Regular 5 2022-10-22 21:30:00            False          True  

[12 rows x 18 columns]

All Team Schedule
      team_name            vs_team  Upcoming_game       Game_datetime      Game_datetime_neat        Rink Jersey Team_side
0     Team Beer      Flying Pandas          False 2022-09-03 21:45:00  Sat, Sep 03 @ 09:45 PM  Orange (N)   Dark      Away
0  Team America   Beerbears on Ice          False 2022-09-10 20:00:00  Sat, Sep 10 @ 08:00 PM        Grey   Dark      Away
1  Team America     Cereal Killers          False 2022-09-19 23:15:00  Mon, Sep 19 @ 11:15 PM        Grey  Light      Home
2  Team America   Beerbears on Ice          False 2022-09-25 17:45:00  Sun, Sep 25 @ 05:45 PM      Sharks   Dark      Away
1     Team Beer    Choking Hazards          False 2022-09-26 22:30:00  Mon, Sep 26 @ 10:30 PM      Sharks  Light      Home
3  Team America           Stampede          False 2022-09-28 21:45:00  Wed, Sep 28 @ 09:45 PM   White (C)   Dark      Away
2     Team Beer      Buffalo Wings          False 2022-10-02 20:45:00  Sun, Oct 02 @ 08:45 PM      Sharks   Dark      Away
3     Team Beer      Schrute Farms          False 2022-10-09 18:00:00  Sun, Oct 09 @ 06:00 PM        Grey  Light      Home
4  Team America            K-Wings          False 2022-10-09 21:00:00  Sun, Oct 09 @ 09:00 PM  Orange (N)   Dark      Away
4     Team Beer    3rd Line Scrubs          False 2022-10-16 19:00:00  Sun, Oct 16 @ 07:00 PM        Grey   Dark      Away
5  Team America  Kraken More Beers          False 2022-10-18 23:15:00  Tue, Oct 18 @ 11:15 PM        Grey  Light      Home
5     Team Beer   Seal Team Sticks           True 2022-10-22 21:30:00  Sat, Oct 22 @ 09:30 PM      Sharks  Light      Home

All Team Schedule, games left
   team_name           vs_team       Game_datetime      Game_datetime_neat    Rink Jersey Team_side
0  Team Beer  Seal Team Sticks 2022-10-22 21:30:00  Sat, Oct 22 @ 09:30 PM  Sharks  Light      Home

Schedule pulled on "Thu Oct 20 2022 01:23 PM"

Schedules printed in "C:\Users\pxrma\Documents\code\jrrm\hockey_schedule_scrape"

Create Hockey Schedule
Event created: https://www.google.com/calendar/event?eid=NTRudGhvdDZsZzYzZ2NrbXQ3dXRzcTNyMDggMDQ5ZmZiMmE2OWI3Yzk3Yjk5ZWM1MTgxMWRiMmNiMDllYjdjNTJiMmMyNmQ2YTQ2MWRlMzdkYTZmM2YzNDM4YUBn   
Delete Old Hockey Schedule
1 Event deleted: Team America Vs. Beerbears on Ice @ 2022-09-10 20:00:00
2 Event deleted: Team America Vs. Cereal Killers @ 2022-09-19 23:15:00
3 Event deleted: Team America Vs. Beerbears on Ice @ 2022-09-25 17:45:00
4 Event deleted: Team Beer Vs. Choking Hazards @ 2022-09-26 22:30:00
5 Event deleted: Team America Vs. Stampede @ 2022-09-28 21:45:00
6 Event deleted: Team Beer Vs. Buffalo Wings @ 2022-10-02 20:45:00
7 Event deleted: Team Beer Vs. Schrute Farms @ 2022-10-09 18:00:00
8 Event deleted: Team America Vs. K-Wings @ 2022-10-09 21:00:00
9 Event deleted: Team Beer Vs. 3rd Line Scrubs @ 2022-10-16 19:00:00
10 Event deleted: Team America Vs. Kraken More Beers @ 2022-10-18 23:15:00
```

### Google Calendar Output:
#### With `remove_old_hockey = False`
![Google_Cal](/pics/Google_Cal_False.png)
#### With `remove_old_hockey = True`
![Google_Cal](/pics/Google_Cal_True.png)

----
Created by: [@jrosilam](https://github.com/jrosilam)