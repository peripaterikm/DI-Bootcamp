-- =============================================
-- Task 1: Rank Actors by Their Appearance Count
-- =============================================

WITH actor_counts AS (
  SELECT
    p.person_name,
    COUNT(*) AS movies_count
  FROM
    movies.movie_cast mc
  JOIN movies.person p
    ON mc.person_id = p.person_id
  GROUP BY
    p.person_name
)
SELECT
  person_name,
  movies_count,
  DENSE_RANK() OVER (
    ORDER BY movies_count DESC
  ) AS appearance_rank
FROM
  actor_counts
ORDER BY
  appearance_rank;

-- =============================================
-- Task 2: Identify the Top Director by Average Movie Rating
-- =============================================

WITH director_ratings AS (
  SELECT
    p.person_name,
    AVG(m.rating) AS avg_rating
  FROM
    movies.movie m
  JOIN movies.movie_director md
    ON m.movie_id = md.movie_id
  JOIN movies.person p
    ON md.person_id = p.person_id
  GROUP BY
    p.person_name
)
SELECT
  person_name,
  avg_rating,
  RANK() OVER (
    ORDER BY avg_rating DESC
  ) AS rating_rank
FROM
  director_ratings
ORDER BY
  rating_rank
LIMIT 1;

-- =============================================
-- Task 3: Calculate Cumulative Revenue per Actor
-- =============================================

SELECT
  p.person_name,
  SUM(m.revenue) AS total_revenue
FROM
  movies.movie m
JOIN movies.movie_cast mc
  ON m.movie_id = mc.movie_id
JOIN movies.person p
  ON mc.person_id = p.person_id
GROUP BY
  p.person_name
ORDER BY
  total_revenue DESC;

-- =============================================
-- Task 4: Director with the Highest Total Budget
-- =============================================

WITH director_budgets AS (
  SELECT
    p.person_name,
    SUM(m.budget) AS total_budget
  FROM
    movies.movie m
  JOIN movies.movie_director md
    ON m.movie_id = md.movie_id
  JOIN movies.person p
    ON md.person_id = p.person_id
  GROUP BY
    p.person_name
)
SELECT
  person_name,
  total_budget
FROM
  director_budgets
ORDER BY
  total_budget DESC
LIMIT 1;
