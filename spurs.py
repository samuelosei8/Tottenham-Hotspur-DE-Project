# Tottenham Hotspur Junior Data Engineer Assessment
# Author: Samuel Osei
# Date: October 2025
#

import json
import pandas as pd
from datetime import datetime


# PART 1: DATA INGESTION & VALIDATION


# Load lineups file (contains multiple JSON objects)
try:
    with open("data/lineups_4028837.json", "r", encoding="utf-8-sig") as f:
        lineups_data = [json.loads(line) for line in f]
except Exception as e:
    print("Error loading lineups file:", e)
    exit()

# Load events file (each line is a JSON object)
try:
    with open("data/events_4028837.json", "r", encoding="utf-8-sig") as f:
        events_data = [json.loads(line) for line in f]
except Exception as e:
    print("Error loading events file:", e)
    exit()

print("Files loaded successfully!")
print(f"Total events: {len(events_data)}")


# VALIDATION SECTION


print("Validating file structure...")

# Required fields for both datasets
required_lineup_fields = ["match_date", "match_id", "events", "formations", "lineup", "team_id", "team_name"]
required_event_fields = ["match_id", "id", "index", "period", "timestamp", "type"]

# Validate Lineups File
for i, team in enumerate(lineups_data):
    missing_fields = [f for f in required_lineup_fields if f not in team]
    if missing_fields:
        print(f"Team {i} missing fields: {', '.join(missing_fields)}")
    else:
        print(f"Team {i} has all required fields.")

# Validate Events File
missing_event_fields = []
for e in events_data:
    for field in required_event_fields:
        if field not in e:
            missing_event_fields.append(field)

if missing_event_fields:
    print(f"Events file missing some required fields: {set(missing_event_fields)}")
else:
    print("All required event fields found.")

# Check Match ID Consistency
lineup_match_ids = {team.get("match_id") for team in lineups_data if "match_id" in team}
event_match_ids = {e.get("match_id") for e in events_data if "match_id" in e}

if lineup_match_ids and event_match_ids and lineup_match_ids == event_match_ids:
    print("Match ID consistent between lineups and events files.")
else:
    print("Match ID mismatch or missing between files.")

print("Data validation complete!\n")



# PART 2: DATA ANALYSIS


# Convert event data into a DataFrame
events_df = pd.DataFrame(events_data)

# a) Player Time on Pitch
print("\n(a) Player Time on Pitch")
player_times = {}

for team in lineups_data:
    team_name = team.get("team_name", "Unknown Team")
    print(f"\nProcessing team: {team_name}")

    for player in team.get("lineup", []):
        total_time = 0
        positions = player.get("positions", [])

        if not positions:
            # Player never entered the pitch
            total_time = 0
        else:
            for pos in positions:
                start = pos.get("from")
                end = pos.get("to")

                # Convert timestamps if available
                if start:
                    start_time = datetime.strptime(start, "%H:%M:%S.%f")

                if end:
                    end_time = datetime.strptime(end, "%H:%M:%S.%f")
                    duration = (end_time - start_time).total_seconds()
                else:
                    # Player was still on pitch when match ended
                    # Estimate by using last event timestamp as match end
                    if "timestamp" in events_df.columns:
                        final_timestamp = events_df.iloc[-1]["timestamp"]
                        try:
                            end_time = datetime.strptime(final_timestamp, "%H:%M:%S.%f")
                            duration = (end_time - start_time).total_seconds()
                        except Exception:
                            duration = 0
                    else:
                        duration = 0

                total_time += max(duration, 0)

        player_times[player["player_name"]] = round(total_time, 2)

player_time_df = pd.DataFrame(list(player_times.items()), columns=["Player", "Time_on_Pitch_sec"])
print(player_time_df)


# b) Match Duration
print("\n(b) Match Duration")

# Find the end time of each half (period)
period_durations = {}

for e in events_data:
    period = e.get("period")
    timestamp = e.get("timestamp")

    if period and timestamp:
        # Track the latest timestamp for each period
        if period not in period_durations:
            period_durations[period] = timestamp
        else:
            # Compare to keep the latest time
            current_latest = datetime.strptime(period_durations[period], "%H:%M:%S.%f")
            new_time = datetime.strptime(timestamp, "%H:%M:%S.%f")
            if new_time > current_latest:
                period_durations[period] = timestamp

# Sum durations across all periods
total_seconds = 0
for period, time_str in period_durations.items():
    t = datetime.strptime(time_str, "%H:%M:%S.%f")
    seconds = (t - datetime.strptime("00:00:00.000", "%H:%M:%S.%f")).total_seconds()
    total_seconds += seconds

match_duration_ms = int(total_seconds * 1000)

print(f"Match duration: {round(total_seconds / 60, 2)} minutes ({match_duration_ms} milliseconds)")


# c) Pass Count by Player
print("\n(c) Pass Count by Player")
if "type" in events_df.columns:
    pass_events = [e for e in events_data if e.get("type", {}).get("name") == "Pass"]
    pass_df = pd.DataFrame(pass_events)
    pass_df["player_name"] = pass_df["player"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
    pass_counts = pass_df["player_name"].value_counts().reset_index()
    pass_counts.columns = ["Player", "Pass_Count"]
    print(pass_counts)

else:
    print("No 'type' data found in events file.")

# d) Goal Times
print("\n(d) Goal Times")

goal_events = []

for event in events_data:
    event_type = event.get("type", {}).get("name")

    # Check for normal goals
    if event_type == "Shot":
        if "shot" in event:
            outcome = event["shot"].get("outcome", {}).get("name")
            if outcome == "Goal":
                player_name = event.get("player", {}).get("name")
                team_name = event.get("team", {}).get("name")
                minute = event.get("minute")
                goal_events.append((player_name, team_name, minute, "Goal"))

    # Check for own goals
    if event_type == "Own Goal For":
        player_name = event.get("player", {}).get("name")
        team_name = event.get("team", {}).get("name")
        minute = event.get("minute")
        goal_events.append((player_name, team_name, minute, "Own Goal"))

# Print results
if goal_events:
    print("Goals scored in match:")
    for g in goal_events:
        player, team, minute, goal_type = g
        if goal_type == "Own Goal":
            print(f"{player} scored an OWN GOAL for {team} at minute {minute}")
        else:
            print(f"{player} scored for {team} at minute {minute}")
else:
    print("No goals found in match data.")



# e) First Foul in Second Half
#
print("\n(e) First Foul in Second Half")

# Find the first half duration (so we can offset the second half)
first_half_end = None
for event in events_data:
    if event.get("period") == 1:
        first_half_end = event.get("timestamp")  # keep updating, ends with last timestamp

# Now find fouls in the second half
fouls_second_half = [
    e for e in events_data
    if e.get("type", {}).get("name") == "Foul Committed" and e.get("period") == 2
]

if fouls_second_half:
    # Take the first foul event in 2nd half
    first_foul = fouls_second_half[0]
    foul_time_str = first_foul.get("timestamp")

    # Convert both timestamps to seconds
    try:
        if first_half_end and foul_time_str:
            fh_end = datetime.strptime(first_half_end, "%H:%M:%S.%f")
            foul_time = datetime.strptime(foul_time_str, "%H:%M:%S.%f")

            # Add first half total seconds to foul time in 2nd half
            total_seconds = (
                (fh_end - datetime.strptime("00:00:00.000", "%H:%M:%S.%f")).total_seconds()
                + (foul_time - datetime.strptime("00:00:00.000", "%H:%M:%S.%f")).total_seconds()
            )
            print(f"First foul in 2nd half occurred at {round(total_seconds, 2)} seconds from match start.")
        else:
            print("Could not determine foul time accurately (missing timestamps).")
    except Exception as e:
        print("Error calculating foul time:", e)
else:
    print("No fouls found in second half.")



# END OF SCRIPT

print("\nAnalysis complete.")
