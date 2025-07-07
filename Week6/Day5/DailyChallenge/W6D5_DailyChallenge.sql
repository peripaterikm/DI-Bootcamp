-- ============================================
-- Task 1: Average Budget Growth Rate per Company
-- ============================================

WITH company_budget_growth AS (
  SELECT
    pc.company_name,
    m.movie_id,
    m.title,
    m.release_date,
    m.budget,
    LAG(m.budget) OVER (
      PARTITION BY pc.company_name
      ORDER BY m.release_date
    ) AS prev_budget
  FROM
    movies.movie m
  JOIN movies.movie_company mc
    ON m.movie_id = mc.movie_id
  JOIN movies.production_company pc
    ON mc.company_id = pc.company_id
)
SELECT
  company_name,
  AVG(
    CASE
      WHEN prev_budget IS NOT NULL AND prev_budget > 0 THEN
        (budget - prev_budget) * 1.0 / prev_budget
      ELSE NULL
    END
  ) AS avg_budget_growth_rate
FROM
  company_budget_growth
GROUP BY
  company_name
ORDER BY
  avg_budget_growth_rate DESC;

------------------------------------------------------------

-- ============================================
-- Task 2: Most Consistently High-Rated Actor
-- ============================================

WITH avg_rating AS (
  SELECT AVG(rating) AS overall_avg_rating
  FROM movies.movie
),
high_rated_movies AS (
  SELECT
    m.movie_id
  FROM
    movies.movie m,
    avg_rating a
  WHERE
    m.rating > a.overall_avg_rating
),
actor_high_rated_counts AS (
  SELECT
    p.person_name,
    COUNT(*) AS high_rated_movie_count
  FROM
    movies.movie_cast mc
  JOIN movies.person p
    ON mc.person_id = p.person_id
  WHERE
    mc.movie_id IN (SELECT movie_id FROM high_rated_movies)
  GROUP BY
    p.person_name
)
SELECT
  person_name,
  high_rated_movie_count
FROM
  actor_high_rated_counts
ORDER BY
  high_rated_movie_count DESC
LIMIT 1;

------------------------------------------------------------

-- ============================================
-- Task 3: Rolling Average Revenue per Genre
-- ============================================

SELECT
  g.genre_name,
  m.title,
  m.release_date,
  m.revenue,
  ROUND(AVG(m.revenue) OVER (
    PARTITION BY g.genre_name
    ORDER BY m.release_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ), 2) AS rolling_avg_revenue
FROM
  movies.movie m
JOIN movies.movie_genres mg
  ON m.movie_id = mg.movie_id
JOIN movies.genre g
  ON mg.genre_id = g.genre_id
ORDER BY
  g.genre_name,
  m.release_date;

------------------------------------------------------------

-- ============================================
-- Task 4: Highest-Grossing Movie Series (by Keyword)
-- ============================================

WITH keyword_revenue AS (
  SELECT
    k.keyword_name,
    SUM(m.revenue) AS total_revenue
  FROM
    movies.movie m
  JOIN movies.movie_keyword mk
    ON m.movie_id = mk.movie_id
  JOIN movies.keyword k
    ON mk.keyword_id = k.keyword_id
  GROUP BY
    k.keyword_name
)
SELECT
  keyword_name,
  total_revenue
FROM
  keyword_revenue
ORDER BY
  total_revenue DESC
LIMIT 1;
