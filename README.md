# hockey_schedule_scrape Git Repo

This was made by [Jesus R Rosila Mares](https://github.com/jrosilam) to find hockey schedule and plan better.
(aswell as figure out what jersey color we are)

# Table of Contents

- [hockey_schedule_scrape Git Repo](#hockey-schedule-scrape-git-repo)
- [Table of Contents](#table-of-contents)
- [To-Do](#to-do)
- [New User](#new-user)
- [Example](#example)
  - [How to use:](#how-to-use-)
  - [Expected Input:](#expected-input-)
  - [Expected Output:](#expected-output-)
    - [Terminal Output:](#terminal-output-)
    - [Google Calendar Output:](#google-calendar-output-)
      - [With `remove_old_hockey = False`](#with--remove-old-hockey---false-)
      - [With `remove_old_hockey = True`](#with--remove-old-hockey---true-)
      - [With `add_old_flag = True`](#with--add-old-flag---true-)

# To-Do

- [ ] Make job to run every morning.
- [ ] Streamline Calendar generation for new users.
- [ ] finish new user section.

# New User

[python google cal API setup](https://developers.google.com/calendar/api/quickstart/python)

Fill this in later.

# Example

## How to use

Run `pip` with `requirements.txt` to get required packages installed.

Just edit `team_names` in `google_calendar_sync.py` and run!
The following should populate, terminal print statments
And saved `csv/*.csv` files named:

- `all_team_schedule.csv`
- `all_team_schedule_remaining.csv`

## Expected Input

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

## Expected Output

### Terminal Output

```terminal
                                description                date                          id  Upcoming_game
0    Team Beer (2) Vs. Choking Hazards (10) 2022-09-26 22:30:00  7679l9pj2pos14pgrtiajsgtq8          False
1    Team Beer (2) Vs. Seal Team Sticks (0) 2022-10-22 21:30:00  m8a19ngihdsrt5pd2hk18pnihg          False
2        Team Beer (2) Vs. Rebel Scum 1 (6) 2022-10-30 23:15:00  flkg9gc3fmb3pe9f3f1ef0b6ns          False
3   Team America (4) Vs. Cereal Killers (7) 2022-09-19 23:15:00  su4a8qshdmledvfvskeb1e7cn4          False
4         Team Beer (5) @ Flying Pandas (4) 2022-09-03 21:45:00  gl0ia8djrqnjcaqjm0q9bjiafk          False
5   Team America (4) @ Beerbears on Ice (3) 2022-09-10 20:00:00  o3so756qjd429jkdv5355u3at4          False
6   Team America (2) @ Beerbears on Ice (3) 2022-09-25 17:45:00  oje3qu3552e58s39eoeq0memk8          False
7            Team America (8) @ K-Wings (1) 2022-10-09 21:00:00  7oc89o4klgd3ebig6uhib5es4c          False
8       Team Beer (6) @ 3rd Line Scrubs (5) 2022-10-16 19:00:00  h13cd309e7fvhll8269oprqd0o          False
9         Team Beer (3) @ Buffalo Wings (1) 2022-10-02 20:45:00  s7lb0lsh0rrm4h5iegj9m0ep90          False
10          Team America (2) @ Stampede (2) 2022-09-28 21:45:00  ta9r9if2ugnbql2hra4eud5iok          False
11          Team America @ Beerbears on Ice 2022-11-07 22:00:00  ai3mi7b1v8e5tphge52l6gbmjg           True
12        Team Beer Vs. Fighting Icecocks 2 2022-11-15 21:45:00  chgc9mhiukhpjfep67bik980dg           True
13      Team Beer (2) Vs. Schrute Farms (9) 2022-10-09 18:00:00  eeleiusgnt3h9h8ehkao9u1f3g          False
14            Team America @ Cereal Killers 2022-11-12 23:00:00  9t00cr3okrq7mua2ha46v5qdng           True
Index: 0, Team Name: Team America, URL: https://stats.sharksice.timetoscore.com/display-schedule?team=2297&season=55&league=1&stat_class=1
Index: 1, Team Name: Team Beer, URL: https://stats.sharksice.timetoscore.com/display-schedule?team=4637&season=55&league=1&stat_class=1
   index     Game     team_name              vs_team Team_side Goals_Home Goals_Away  ...    League              Level                 Away              Home       Type       Game_datetime Upcoming_game
0      0  328022*  Team America     Beerbears on Ice      Away          3          4  ...  SIAHL@SJ  Adult Division 6A         Team America  Beerbears on Ice  Regular 1 2022-09-10 20:00:00         False        
1      1  354475*  Team America       Cereal Killers      Home          4          7  ...  SIAHL@SJ  Adult Division 6A       Cereal Killers      Team America  Regular 2 2022-09-19 23:15:00         False        
2      2  351696*  Team America     Beerbears on Ice      Away          3          2  ...  SIAHL@SJ  Adult Division 6A         Team America  Beerbears on Ice  Regular 3 2022-09-25 17:45:00         False        
3      3  360402*  Team America             Stampede      Away          2          2  ...  SIAHL@SJ  Adult Division 6A         Team America          Stampede  Regular 4 2022-09-28 21:45:00         False        
4      4  369297*  Team America              K-Wings      Away          1          8  ...  SIAHL@SJ  Adult Division 6A         Team America           K-Wings  Regular 5 2022-10-09 21:00:00         False        
5      5  343483*  Team America    Kraken More Beers      Home          6          5  ...  SIAHL@SJ  Adult Division 6A    Kraken More Beers      Team America  Regular 6 2022-10-18 23:15:00         False        
6      6  352086*  Team America    Peter North Stars      Home          0          2  ...  SIAHL@SJ  Adult Division 6A    Peter North Stars      Team America  Regular 7 2022-10-30 21:00:00         False        
7      7   342031  Team America     Beerbears on Ice      Away        NaN        NaN  ...  SIAHL@SJ  Adult Division 6A         Team America  Beerbears on Ice  Regular 8 2022-11-07 22:00:00          True        
8      8   371926  Team America       Cereal Killers      Away        NaN        NaN  ...  SIAHL@SJ  Adult Division 6A         Team America    Cereal Killers  Regular 9 2022-11-12 23:00:00          True        
0      0  355546*     Team Beer        Flying Pandas      Away          4          5  ...  SIAHL@SJ  Adult Division 7B            Team Beer     Flying Pandas  Preseason 2022-09-03 21:45:00         False        
1      1  341373*     Team Beer      Choking Hazards      Home          2         10  ...  SIAHL@SJ  Adult Division 7B      Choking Hazards         Team Beer  Regular 1 2022-09-26 22:30:00         False        
2      2  351841*     Team Beer        Buffalo Wings      Away          1          3  ...  SIAHL@SJ  Adult Division 7B            Team Beer     Buffalo Wings  Regular 2 2022-10-02 20:45:00         False        
3      3  351908*     Team Beer        Schrute Farms      Home          2          9  ...  SIAHL@SJ  Adult Division 7B        Schrute Farms         Team Beer  Regular 3 2022-10-09 18:00:00         False        
4      4  369302*     Team Beer      3rd Line Scrubs      Away          5          6  ...  SIAHL@SJ  Adult Division 7B            Team Beer   3rd Line Scrubs  Regular 4 2022-10-16 19:00:00         False        
5      5  350303*     Team Beer     Seal Team Sticks      Home          2          0  ...  SIAHL@SJ  Adult Division 7B     Seal Team Sticks         Team Beer  Regular 5 2022-10-22 21:30:00         False        
6      6  355102*     Team Beer         Rebel Scum 1      Home          2          6  ...  SIAHL@SJ  Adult Division 7B         Rebel Scum 1         Team Beer  Regular 6 2022-10-30 23:15:00         False        
7      7   345506     Team Beer          Cobra Kai 1      Away        NaN        NaN  ...  SIAHL@SJ  Adult Division 7B            Team Beer       Cobra Kai 1  Regular 7 2022-11-09 23:15:00          True        
8      8   343918     Team Beer  Fighting Icecocks 2      Home        NaN        NaN  ...  SIAHL@SJ  Adult Division 7B  Fighting Icecocks 2         Team Beer  Regular 8 2022-11-15 21:45:00          True        

[18 rows x 18 columns]

All Team Schedule
    index     team_name              vs_team Team_side  Upcoming_game Goals_Home Goals_Away  Shootout_decider       Game_datetime      Game_datetime_neat        Rink Jersey
0       0     Team Beer        Flying Pandas      Away          False          4          5              True 2022-09-03 21:45:00  Sat, Sep 03 @ 09:45 PM  Orange (N)   Dark
1       0  Team America     Beerbears on Ice      Away          False          3          4              True 2022-09-10 20:00:00  Sat, Sep 10 @ 08:00 PM        Grey   Dark
2       1  Team America       Cereal Killers      Home          False          4          7             False 2022-09-19 23:15:00  Mon, Sep 19 @ 11:15 PM        Grey  Light
3       2  Team America     Beerbears on Ice      Away          False          3          2             False 2022-09-25 17:45:00  Sun, Sep 25 @ 05:45 PM      Sharks   Dark
4       1     Team Beer      Choking Hazards      Home          False          2         10             False 2022-09-26 22:30:00  Mon, Sep 26 @ 10:30 PM      Sharks  Light
5       3  Team America             Stampede      Away          False          2          2             False 2022-09-28 21:45:00  Wed, Sep 28 @ 09:45 PM   White (C)   Dark
6       2     Team Beer        Buffalo Wings      Away          False          1          3             False 2022-10-02 20:45:00  Sun, Oct 02 @ 08:45 PM      Sharks   Dark
7       3     Team Beer        Schrute Farms      Home          False          2          9             False 2022-10-09 18:00:00  Sun, Oct 09 @ 06:00 PM        Grey  Light
8       4  Team America              K-Wings      Away          False          1          8             False 2022-10-09 21:00:00  Sun, Oct 09 @ 09:00 PM  Orange (N)   Dark
9       4     Team Beer      3rd Line Scrubs      Away          False          5          6             False 2022-10-16 19:00:00  Sun, Oct 16 @ 07:00 PM        Grey   Dark
10      5  Team America    Kraken More Beers      Home          False          6          5             False 2022-10-18 23:15:00  Tue, Oct 18 @ 11:15 PM        Grey  Light
11      5     Team Beer     Seal Team Sticks      Home          False          2          0             False 2022-10-22 21:30:00  Sat, Oct 22 @ 09:30 PM      Sharks  Light
12      6  Team America    Peter North Stars      Home          False          0          2             False 2022-10-30 21:00:00  Sun, Oct 30 @ 09:00 PM      Sharks  Light
13      6     Team Beer         Rebel Scum 1      Home          False          2          6             False 2022-10-30 23:15:00  Sun, Oct 30 @ 11:15 PM   Black (E)  Light
14      7  Team America     Beerbears on Ice      Away           True        NaN        NaN             False 2022-11-07 22:00:00  Mon, Nov 07 @ 10:00 PM   Black (E)   Dark
15      7     Team Beer          Cobra Kai 1      Away           True        NaN        NaN             False 2022-11-09 23:15:00  Wed, Nov 09 @ 11:15 PM   Black (E)   Dark
16      8  Team America       Cereal Killers      Away           True        NaN        NaN             False 2022-11-12 23:00:00  Sat, Nov 12 @ 11:00 PM   White (C)   Dark
17      8     Team Beer  Fighting Icecocks 2      Home           True        NaN        NaN             False 2022-11-15 21:45:00  Tue, Nov 15 @ 09:45 PM        Grey  Light

All Team Schedule, games left
   level_0     team_name              vs_team Team_side  Shootout_decider       Game_datetime      Game_datetime_neat       Rink Jersey
0       14  Team America     Beerbears on Ice      Away             False 2022-11-07 22:00:00  Mon, Nov 07 @ 10:00 PM  Black (E)   Dark
1       15     Team Beer          Cobra Kai 1      Away             False 2022-11-09 23:15:00  Wed, Nov 09 @ 11:15 PM  Black (E)   Dark
2       16  Team America       Cereal Killers      Away             False 2022-11-12 23:00:00  Sat, Nov 12 @ 11:00 PM  White (C)   Dark
3       17     Team Beer  Fighting Icecocks 2      Home             False 2022-11-15 21:45:00  Tue, Nov 15 @ 09:45 PM       Grey  Light

Schedule pulled on "Fri Nov 04 2022 04:25 PM"

Schedules printed in "C:\Users\rober\OneDrive\Desktop\code\hockey_schedule_scrape"

Create Hockey Schedule
15 Event Create: https://www.google.com/calendar/event?eid=aDdqMnZjazlrczc3ZXV0MzdqNGdzbGRlOHMgMDQ5ZmZiMmE2OWI3Yzk3Yjk5ZWM1MTgxMWRiMmNiMDllYjdjNTJiMmMyNmQ2YTQ2MWRlMzdkYTZmM2YzNDM4YUBn
Update Hockey Schedule
                                description                date                          id  Upcoming_game
0    Team Beer (2) Vs. Choking Hazards (10) 2022-09-26 22:30:00  7679l9pj2pos14pgrtiajsgtq8          False
1    Team Beer (2) Vs. Seal Team Sticks (0) 2022-10-22 21:30:00  m8a19ngihdsrt5pd2hk18pnihg          False
2        Team Beer (2) Vs. Rebel Scum 1 (6) 2022-10-30 23:15:00  flkg9gc3fmb3pe9f3f1ef0b6ns          False
3   Team America (4) Vs. Cereal Killers (7) 2022-09-19 23:15:00  su4a8qshdmledvfvskeb1e7cn4          False
4         Team Beer (5) @ Flying Pandas (4) 2022-09-03 21:45:00  gl0ia8djrqnjcaqjm0q9bjiafk          False
5   Team America (4) @ Beerbears on Ice (3) 2022-09-10 20:00:00  o3so756qjd429jkdv5355u3at4          False
6   Team America (2) @ Beerbears on Ice (3) 2022-09-25 17:45:00  oje3qu3552e58s39eoeq0memk8          False
7            Team America (8) @ K-Wings (1) 2022-10-09 21:00:00  7oc89o4klgd3ebig6uhib5es4c          False
8       Team Beer (6) @ 3rd Line Scrubs (5) 2022-10-16 19:00:00  h13cd309e7fvhll8269oprqd0o          False
9         Team Beer (3) @ Buffalo Wings (1) 2022-10-02 20:45:00  s7lb0lsh0rrm4h5iegj9m0ep90          False
10          Team America (2) @ Stampede (2) 2022-09-28 21:45:00  ta9r9if2ugnbql2hra4eud5iok          False
11          Team America @ Beerbears on Ice 2022-11-07 22:00:00  ai3mi7b1v8e5tphge52l6gbmjg           True
12        Team Beer Vs. Fighting Icecocks 2 2022-11-15 21:45:00  chgc9mhiukhpjfep67bik980dg           True
13      Team Beer (2) Vs. Schrute Farms (9) 2022-10-09 18:00:00  eeleiusgnt3h9h8ehkao9u1f3g          False
14            Team America @ Cereal Killers 2022-11-12 23:00:00  9t00cr3okrq7mua2ha46v5qdng           True
15                  Team Beer @ Cobra Kai 1 2022-11-09 23:15:00  h7j2vck9ks77eut37j4gslde8s           True
```

### Google Calendar Output

#### With `remove_old_hockey = False`

![Google_Cal](/pics/Google_Cal_False.png)

#### With `remove_old_hockey = True`

![Google_Cal](/pics/Google_Cal_True.png)

#### With `add_old_flag = True`

![Google_Cal](/pics/Google_Cal_update_old_games.png)

----
Created by: [@jrosilam](https://github.com/jrosilam)
