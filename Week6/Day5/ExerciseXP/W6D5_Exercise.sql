-- Ex.1

-- Task 1
SELECT
  g.genre_name,
  m.title,
  RANK() OVER (
    PARTITION BY g.genre_name
    ORDER BY m.popularity DESC
  ) AS popularity_rank
FROM
  movies.movie m
JOIN movies.movie_genres mg
  ON m.movie_id = mg.movie_id
JOIN movies.genre g
  ON mg.genre_id = g.genre_id
ORDER BY
  g.genre_name,
  popularity_rank;

-- Task 2
SELECT
  pc.company_name,
  m.title,
  m.revenue,
  NTILE(4) OVER (
    PARTITION BY pc.company_name
    ORDER BY m.revenue DESC
  ) AS revenue_quartile
FROM
  movies.movie m
JOIN movies.movie_company mc
  ON m.movie_id = mc.movie_id
JOIN movies.production_company pc
  ON mc.company_id = pc.company_id
ORDER BY
  pc.company_name,
  revenue_quartile;

WITH ranked_movies AS (
  SELECT
    pc.company_name,
    m.title,
    m.revenue,
    RANK() OVER (
      PARTITION BY pc.company_name
      ORDER BY m.revenue DESC
    ) AS revenue_rank
  FROM
    movies.movie m
  JOIN movies.movie_company mc
    ON m.movie_id = mc.movie_id
  JOIN movies.production_company pc
    ON mc.company_id = pc.company_id
)
SELECT
  company_name,
  title,
  revenue,
  revenue_rank
FROM
  ranked_movies
WHERE
  revenue_rank <= 3
ORDER BY
  company_name,
  revenue_rank;

-- Task 3
SELECT
  g.genre_name,
  m.title,
  m.budget,
  SUM(m.budget) OVER (
    PARTITION BY g.genre_name
    ORDER BY m.budget DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total_budget
FROM
  movies.movie m
JOIN movies.movie_genres mg
  ON m.movie_id = mg.movie_id
JOIN movies.genre g
  ON mg.genre_id = g.genre_id
ORDER BY
  g.genre_name,
  m.budget DESC;

-- Task 4
SELECT
  genre_name,
  title,
  release_date
FROM (
  SELECT
    g.genre_name,
    FIRST_VALUE(m.title) OVER (
      PARTITION BY g.genre_name
      ORDER BY m.release_date DESC
    ) AS title,
    FIRST_VALUE(m.release_date) OVER (
      PARTITION BY g.genre_name
      ORDER BY m.release_date DESC
    ) AS release_date,
    ROW_NUMBER() OVER (
      PARTITION BY g.genre_name
      ORDER BY m.release_date DESC
    ) AS rn
  FROM
    movies.movie m
  JOIN movies.movie_genres mg
    ON m.movie_id = mg.movie_id
  JOIN movies.genre g
    ON mg.genre_id = g.genre_id
) sub
WHERE
  rn = 1
ORDER BY
  genre_name;

-- Ex.2
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
