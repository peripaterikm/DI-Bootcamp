-- How to create a table

-- CREATE TABLE actors(
-- actor_id SERIAL PRIMARY KEY,
-- first_name VARCHAR(50) NOT NULL,
-- last_name VARCHAR(150) NOT NULL,
-- date_of_birth DATE NOT NULL,
-- number_oscars SMALLINT NOT NULL
-- )

-- How to inset data into the table

-- INSERT INTO actors(first_name, last_name, date_of_birth, number_oscars)
-- VALUES  ('Matt', 'Damon', '06/05/1961', 2)


-- INSERT INTO actors (first_name, last_name, date_of_birth, number_oscars)
-- VALUES ('Emma', 'Stone', '06/11/1988', 2);

-- INSERT INTO actors (first_name, last_name, date_of_birth, number_oscars)
-- VALUES ('Scarlett', 'Johansson', '22/11/1984', 0);


-- INSERT INTO actors (first_name, last_name, date_of_birth, number_oscars)
-- VALUES 
--   ('Leonardo', 'DiCaprio', '11/11/1974', 1),
--   ('Meryl', 'Streep', '22/06/1949', 3),
--   ('Robert', 'De Niro', '17/08/1943', 2);

-- SELECT last_name, number_oscars FROM actors WHERE date_of_birth < '1970-01-01' ORDER BY last_name DESC

-- SELECT * FROM actors LIMIT 4;
-- SELECT * FROM actors ORDER BY last_name DESC LIMIT 4;
-- SELECT * FROM actors WHERE first_name ILIKE '%e%';
-- SELECT * FROM actors WHERE number_oscars > 2;

-- DELETE FROM actors WHERE first_name = 'Emma';

-- SELECT * FROM actors;

SELECT COUNT(*) FROM actors;

INSERT INTO actors (first_name, last_name, date_of_birth, number_oscars)
VALUES ('Emma', 'Watson', '15/04/1990', Null);

-- All columns are declared NOT NULL, so the query will fail with an error.
