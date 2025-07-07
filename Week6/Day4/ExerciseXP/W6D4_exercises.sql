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


-- Ex.2
-- Task 1
UPDATE olympics.person p
SET height = (
    SELECT AVG(p2.height)
    FROM olympics.person p2
    JOIN olympics.person_region pr2
      ON p2.id = pr2.person_id
    WHERE pr2.region_id = (
        SELECT pr3.region_id
        FROM olympics.person_region pr3
        WHERE pr3.person_id = p.id
    )
)
WHERE height IS NULL;

-- Task 2
CREATE TEMP TABLE multi_event_competitors AS
SELECT
  ce.competitor_id,
  COUNT(DISTINCT ce.event_id) AS total_events
FROM
  olympics.competitor_event ce
GROUP BY
  ce.competitor_id
HAVING
  COUNT(DISTINCT ce.event_id) > 1;

-- Task 3
-- Шаг 1: Считаем медали по каждому спортсмену и региону
WITH medals_per_competitor AS (
  SELECT
    pr.region_id,
    ce.competitor_id,
    COUNT(ce.medal_id) AS medal_count
  FROM
    olympics.competitor_event ce
  JOIN olympics.games_competitor gc
    ON ce.competitor_id = gc.id
  JOIN olympics.person_region pr
    ON gc.person_id = pr.person_id
  GROUP BY
    pr.region_id,
    ce.competitor_id
),

-- -- Шаг 2: Среднее по каждому региону
avg_medals_per_region AS (
  SELECT
    region_id,
    AVG(medal_count) AS avg_medals
  FROM
    medals_per_competitor
  GROUP BY
    region_id
),

-- -- Шаг 3: Общая средняя
overall_avg AS (
  SELECT
    AVG(medal_count) AS overall_avg_medals
  FROM
    medals_per_competitor
)

-- -- Шаг 4: Сравнение и вывод
SELECT
  nr.region_name,
  ar.avg_medals
FROM
  avg_medals_per_region ar
JOIN olympics.noc_region nr
  ON ar.region_id = nr.id,
  overall_avg oa
WHERE
  ar.avg_medals > oa.overall_avg_medals
ORDER BY
  ar.avg_medals DESC;

Task 4
-- Task 4: Create a temporary table to track competitors participation across different seasons
-- and identify those who participated in both Summer and Winter games.

-- Step 1: Create a temp table with competitor IDs and seasons of participation
CREATE TEMP TABLE competitor_seasons AS
SELECT
  ce.competitor_id,
  g.season
FROM
  olympics.competitor_event ce
JOIN olympics.event e
  ON ce.event_id = e.id
JOIN olympics.games g
  ON e.games_id = g.id
GROUP BY
  ce.competitor_id,
  g.season;

-- Step 2: Review the content of the temp table
SELECT *
FROM competitor_seasons
ORDER BY competitor_id, season;

-- Step 3: Find competitors who participated in both Summer and Winter games
SELECT
  competitor_id
FROM
  competitor_seasons
GROUP BY
  competitor_id
HAVING
  COUNT(DISTINCT season) = 2
ORDER BY
  competitor_id;
