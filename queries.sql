
-- Tottenham Hotspur – SQL Analysis
-- Table: events(event_id, match_id, team_id, player_id, player_name, event_type, timestamp, location_x, location_y)


 -- f) Furthest Shot from Goal
 -- Find the player who took a shot from the furthest distance from the goal centre (x=120, y=40).

SELECT
  player_name,
  ((location_x - 120) * (location_x - 120) +
   (location_y - 40)  * (location_y - 40)) AS distance_squared
FROM events
WHERE event_type = 'Shot'
  AND location_x IS NOT NULL
  AND location_y IS NOT NULL
ORDER BY distance_squared DESC
LIMIT 1;


-- g) Penalty Box Events
-- Count events that occurred in the penalty box (x > 102 AND y BETWEEN 18 AND 62), grouped by type.

  event_type,
  COUNT(*) AS total_events
FROM events
WHERE location_x > 102
  AND location_y BETWEEN 18 AND 62
GROUP BY event_type
ORDER BY total_events DESC;



-- h) Longest Time Between Shots (consecutive shots)
-- Find the longest gap (in seconds) between any two CONSECUTIVE shots in the match (regardless of team),
-- and show both shot timestamps and the time difference.

WITH shots AS (
  SELECT timestamp
  FROM events
  WHERE event_type = 'Shot'
    AND timestamp IS NOT NULL
),
next_shot_for_each AS (
  SELECT
    s1.timestamp AS shot_time_1,
    (
      SELECT MIN(s2.timestamp)
      FROM shots s2
      WHERE s2.timestamp > s1.timestamp
    ) AS shot_time_2
  FROM shots s1
)
SELECT
  shot_time_1,
  shot_time_2,
  (shot_time_2 - shot_time_1) AS time_diff_seconds
FROM next_shot_for_each
WHERE shot_time_2 IS NOT NULL
ORDER BY time_diff_seconds DESC
LIMIT 1;
