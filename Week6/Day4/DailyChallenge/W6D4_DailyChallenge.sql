-- Ex.1
-- Task 1
-- Temp table for competitors with medals in exactly two sports
CREATE TEMP TABLE competitors_two_sports AS
SELECT
  ce.competitor_id,
  COUNT(DISTINCT e.sport_id) AS num_sports,
  COUNT(*) AS total_medals
FROM
  olympics.competitor_event ce
JOIN olympics.event e
  ON ce.event_id = e.id
WHERE
  ce.medal_id IS NOT NULL
GROUP BY
  ce.competitor_id
HAVING
  COUNT(DISTINCT e.sport_id) = 2;

-- Display top 3 competitors by total medals
SELECT
  cts.competitor_id,
  cts.total_medals
FROM
  competitors_two_sports cts
ORDER BY
  cts.total_medals DESC
LIMIT 3;

-- Display all contents
SELECT *
FROM competitors_two_sports
ORDER BY total_medals DESC;

-- Task 2
-- Temp table for competitors with medals in exactly two sports
CREATE TEMP TABLE competitors_two_sports AS
SELECT
  ce.competitor_id,
  COUNT(DISTINCT e.sport_id) AS num_sports,
  COUNT(*) AS total_medals
FROM
  olympics.competitor_event ce
JOIN olympics.event e
  ON ce.event_id = e.id
WHERE
  ce.medal_id IS NOT NULL
GROUP BY
  ce.competitor_id
HAVING
  COUNT(DISTINCT e.sport_id) = 2;

-- Display top 3 competitors by total medals
SELECT
  cts.competitor_id,
  cts.total_medals
FROM
  competitors_two_sports cts
ORDER BY
  cts.total_medals DESC
LIMIT 3;

-- Display all contents
SELECT *
FROM competitors_two_sports
ORDER BY total_medals DESC;

-- Ex.2
-- Task 1
-- Subquery: for each competitor, find the event with the max medals
WITH competitor_max_event AS (
  SELECT
    ce.competitor_id,
    ce.event_id,
    COUNT(*) AS medals_in_event
  FROM
    olympics.competitor_event ce
WHERE
    ce.medal_id IS NOT NULL
  GROUP BY
    ce.competitor_id,
    ce.event_id
),
-- Total medals per region considering the competitor's best event
region_medals AS (
  SELECT
    pr.region_id,
    SUM(cme.medals_in_event) AS total_medals
  FROM
    competitor_max_event cme
  JOIN olympics.games_competitor gc
    ON cme.competitor_id = gc.id
  JOIN olympics.person_region pr
    ON gc.person_id = pr.person_id
  GROUP BY
    pr.region_id
)
SELECT
  nr.region_name,
  rm.total_medals
FROM
  region_medals rm
JOIN olympics.noc_region nr
  ON rm.region_id = nr.id
ORDER BY
  rm.total_medals DESC
LIMIT 5;

-- Task 2
-- Temp table with competitors with >3 participations and no medals
CREATE TEMP TABLE multi_game_no_medal AS
SELECT
  gc.id AS competitor_id,
  p.person_name,
  COUNT(DISTINCT g.id) AS games_count
FROM
  olympics.games_competitor gc
JOIN olympics.person p
  ON gc.person_id = p.id
JOIN olympics.competitor_event ce
  ON ce.competitor_id = gc.id
JOIN olympics.event e
  ON ce.event_id = e.id
JOIN olympics.games g
  ON e.games_id = g.id
GROUP BY
  gc.id,
  p.person_name
HAVING
  COUNT(DISTINCT g.id) > 3
  AND SUM(CASE WHEN ce.medal_id IS NOT NULL THEN 1 ELSE 0 END) = 0;

-- Display contents
SELECT *
FROM multi_game_no_medal
ORDER BY games_count DESC;
