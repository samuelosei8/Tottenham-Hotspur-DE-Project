Tottenham Hotspur Junior Data Engineer Assessment
Author:Samuel Osei  
Date:October 2025  


## Overview
This project completes the Tottenham Hotspur Junior Data Engineer assessment using Hudl StatsBomb data.  
It includes a Python script (`spurs.py`) and SQL queries (`queries.sql`) that analyse match data and extract useful insights.

I focused on writing simple and clear code to show my understanding of the data and how I approach problem-solving.


## Contents
- `spurs.py` – Python script covering tasks (a) to (e)
- `queries.sql` – SQL queries covering tasks (f) to (h)
- Data folder – Contains JSON files (`lineups_4028837.json` and `events_4028837.json`)


## Python and SQL Tasks Summary

PYTHON
(a) Player time on pitch (in seconds)
(b) Match duration (in milliseconds)
(c) Pass count by player
(d) Goal times (including own goals)
(e) First foul in second half (seconds from match start)

SQL
(f) Find the furthest shot from goal
(g) Count events in the penalty box
(h) Find the longest time gap between consecutive shots

QUERIES.SQL EXPECTED OUTPUT
(f) Furthest Shot from Goal:
    player_name  distance_squared
0  Nicolas Pépé           1480.96

(g) Penalty Box Events:
        event_type  total_events
0         Pressure            23
1    Ball Receipt*            23
2             Pass            18
3            Carry            10
4             Shot             8
5    Ball Recovery             6
6             Duel             4
7       Miscontrol             2
8          Dribble             2
9     Dispossessed             2
10    Own Goal For             1
11         Offside             1
12  Foul Committed             1
13           Block             1

(h) Longest Time Between Shots:
   shot_time_1  shot_time_2  time_diff_seconds
0      992.058      1448.06            456.002




## Challenges & What I Learned

This assessment was a great learning experience and very rewarding, however, also quite challenging in places.  
At first, I found it hard to understand the JSON file structure because the lineups and events files were formatted differently.  
It took some time to figure out how to extract the right values and match them together.

Working out the match duration and foul timings was also tricky because the timestamps reset each half, so I had to think carefully about how to calculate total time from the start of the match.  
I also initially missed the own goal because I didn’t realise StatsBomb stores it as a different event type.

The SQL part was challenging too. I don’t have an expert amount of SQL experience yet, so I had to do the queries as simple as possible using basic comparisons and arithmetic.  
I know some tasks could be done in more advanced ways but I think it showed I understand the basics.

To test the queries, I created a small SQLite in-memory database using Python and loaded the JSON data into it. This allowed me to run each query directly and check the outputs.

Some queries didn’t work at first because of NULL values or because timestamps were stored as strings, so I had to convert them into seconds to calculate time differences.
Once I fixed those issues, I could successfully test and verify each query.

Through a lot trial and error, some help from YouTube videos, websites and testing my code, I managed to complete each part and learned a lot about working with football event data.
 


## If I Had More Time 
- I’d export results (like pass counts and player times) into CSVs for easier analysis.  
- I’d include simple visualisations such as bar charts to present the insights more clearly.  
- I’d learn more functions to improve accuracy and efficiency in future projects.
- Explore automating the process to handle multiple matches efficiently.


## How to Run

1. Place all data files inside a folder named `data/`.  
2. Run the Python script:
   python spurs.py
