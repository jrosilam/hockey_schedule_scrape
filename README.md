# hockey_schedule_scrape
This was made by Jesus R Rosila Mares to schedule and plan better. 
(aswell as figure out what jersey color we are)

## How to use:
Just edit `team_names` in `hockey_game_scraper.py` and run!   
The following should populate, terminal print statments   
And saved `.csv` files named:   
- `all_team_schedule.csv`
- `all_team_schedule_remaining.csv`

## expected output:
```sh
Index: 0, Team Name: Team America, URL: https://stats.sharksice.timetoscore.com/display-schedule?team=2297&season=55&league=1&stat_class=1
Index: 1, Team Name: Team Beer, URL: https://stats.sharksice.timetoscore.com/display-schedule?team=4637&season=55&league=1&stat_class=1
All Team Schedule
      team_name            vs_team  Upcoming_game      Game_datetime_neat        Rink Jersey Team_side
0     Team Beer      Flying Pandas          False  Sat, Sep 03 @ 09:45 PM  Orange (N)   Dark      Away
0  Team America   Beerbears on Ice          False  Sat, Sep 10 @ 08:00 PM        Grey   Dark      Away
1  Team America     Cereal Killers          False  Mon, Sep 19 @ 11:15 PM        Grey  Light      Home
2  Team America   Beerbears on Ice          False  Sun, Sep 25 @ 05:45 PM      Sharks   Dark      Away
1     Team Beer    Choking Hazards          False  Mon, Sep 26 @ 10:30 PM      Sharks  Light      Home
3  Team America           Stampede          False  Wed, Sep 28 @ 09:45 PM   White (C)   Dark      Away
2     Team Beer      Buffalo Wings          False  Sun, Oct 02 @ 08:45 PM      Sharks   Dark      Away
3     Team Beer      Schrute Farms           True  Sun, Oct 09 @ 06:00 PM        Grey  Light      Home
4  Team America            K-Wings           True  Sun, Oct 09 @ 09:00 PM  Orange (N)   Dark      Away
4     Team Beer    3rd Line Scrubs           True  Sun, Oct 16 @ 07:00 PM        Grey   Dark      Away
5  Team America  Kraken More Beers           True  Tue, Oct 18 @ 11:15 PM        Grey  Light      Home
5     Team Beer   Seal Team Sticks           True  Sat, Oct 22 @ 09:30 PM      Sharks  Light      Home

All Team Schedule, games left
      team_name            vs_team      Game_datetime_neat        Rink Jersey Team_side
0     Team Beer      Schrute Farms  Sun, Oct 09 @ 06:00 PM        Grey  Light      Home
1  Team America            K-Wings  Sun, Oct 09 @ 09:00 PM  Orange (N)   Dark      Away
2     Team Beer    3rd Line Scrubs  Sun, Oct 16 @ 07:00 PM        Grey   Dark      Away
3  Team America  Kraken More Beers  Tue, Oct 18 @ 11:15 PM        Grey  Light      Home
4     Team Beer   Seal Team Sticks  Sat, Oct 22 @ 09:30 PM      Sharks  Light      Home

Schedules printed in "D:\Documents\code"
```