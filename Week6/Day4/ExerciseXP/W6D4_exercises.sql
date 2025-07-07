--------------------------------------------------------
-- Task 1: Average age of competitors with at least one medal, grouped by medal type
--------------------------------------------------------

SELECT
  m.medal_name,
  AVG(
    (
      SELECT gc.age
      FROM games_competitor gc
      WHERE gc.id = ce.competitor_id
    )
  ) AS average_age
FROM
  competitor_event ce
INNER JOIN medal m ON ce.medal_id = m.id
GROUP BY
  m.medal_name;


--------------------------------------------------------
-- Task 2: Top 5 regions with the highest number of unique competitors
-- who participated in more than 3 different events
--------------------------------------------------------

SELECT
  nr.region_name,
  COUNT(DISTINCT pr.person_id) AS unique_competitors
FROM
  person_region pr
INNER JOIN noc_region nr ON pr.region_id = nr.id
WHERE
  pr.person_id IN (
    SELECT gc.person_id
    FROM (
      SELECT
        ce.competitor_id,
        COUNT(DISTINCT ce.event_id) AS event_count
      FROM competitor_event ce
      GROUP BY ce.competitor_id
      HAVING COUNT(DISTINCT ce.event_id) > 3
    ) AS sub
    INNER JOIN games_competitor gc
      ON sub.competitor_id = gc.id
  )
GROUP BY
  nr.region_name
ORDER BY
  unique_competitors DESC
LIMIT 5;


--------------------------------------------------------
-- Task 3: Create a temp table with total medals per competitor
-- and filter to show only those with more than 2 medals
--------------------------------------------------------

CREATE TEMP TABLE competitor_medal_count AS
SELECT
  ce.competitor_id,
  COUNT(*) AS medal_count
FROM
  competitor_event ce
WHERE
  ce.medal_id IS NOT NULL
GROUP BY
  ce.competitor_id;


-- Query competitors with more than 2 medals
SELECT *
FROM competitor_medal_count
WHERE medal_count > 2;


--------------------------------------------------------
-- Task 4: Delete records of competitors with no medals from temp table
--------------------------------------------------------

DELETE FROM competitor_medal_count
WHERE competitor_id IN (
  SELECT ce.competitor_id
  FROM competitor_event ce
  GROUP BY ce.competitor_id
  HAVING COUNT(ce.medal_id) = 0
);
