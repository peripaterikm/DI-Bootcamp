-- 1. Get a list of all the languages, from the language table.
SELECT * FROM language;

-- 2. Get a list of all films joined with their languages – select the following details : film title, description, and language name.
SELECT f.title, f.description, l.name FROM film f 
INNER JOIN
  language l
ON
  f.language_id = l.language_id;

-- 3. Get all languages, even if there are no films in those languages – select the following details : film title, description, and language name.
SELECT f.title, f.description, l.name FROM film f 
RIGHT JOIN
  language l
ON
  f.language_id = l.language_id;

-- 4. Create a new table called new_film with the following columns : id, name. Add some new films to the table.
CREATE TABLE new_film(
 	id SERIAL primary key, 
	name VARCHAR(100) 
);

INSERT INTO new_film (name)
VALUES
  ('The Grand Adventure'),
  ('Midnight Secrets'),
  ('Echoes of Tomorrow'),
  ('Silent Horizon');

-- 5. Create a new table called customer_review, which will contain film reviews that customers will make.
-- Think about the DELETE constraint: if a film is deleted, its review should be automatically deleted.
-- It should have the following columns:
-- review_id – a primary key, non null, auto-increment.
-- film_id – references the new_film table. The film that is being reviewed.
-- language_id – references the language table. What language the review is in.
-- title – the title of the review.
-- score – the rating of the review (1-10).
-- review_text – the text of the review. No limit on the length.
-- last_update – when the review was last updated. 
CREATE TABLE customer_review(
 	review_id SERIAL primary key, 
	film_id INTEGER NOT NULL REFERENCES new_film(id) ON DELETE CASCADE,
    language_id INTEGER NOT NULL REFERENCES language(language_id),
    title VARCHAR(255),
    score INTEGER CHECK (score BETWEEN 1 AND 10),
    review_text TEXT,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP	
);

-- 6. Add 2 movie reviews. Make sure you link them to valid objects in the other tables.
INSERT INTO customer_review (
    film_id,
    language_id,
    title,
    score,
    review_text
) VALUES
(
    1,             -- film_id (например, "The Grand Adventure")
    1,             -- language_id (например, English)
    'Epic Journey',
    8,
    'An inspiring and exciting adventure from start to finish.'
),
(
    2,             -- film_id (например, "Midnight Secrets")
    2,             -- language_id (например, Spanish)
    'Noches Misteriosas',
    7,
    'Una película interesante con un toque de misterio.'
);

-- 7. Delete a film that has a review from the new_film table, what happens to the customer_review table?
DELETE FROM new_film WHERE id = 1;

SELECT * FROM customer_review;

-- Ex.2
-- 1) Update the language of some films
UPDATE film
SET language_id = 2
WHERE language_id = 1;

-- Check the list of available languages
SELECT * FROM language;

-- 2) Foreign keys in the customer table:
-- address_id:
-- FOREIGN KEY (address_id) REFERENCES address(address_id)
-- store_id:
-- FOREIGN KEY (store_id) REFERENCES store(store_id)

-- 3) Drop the customer_review table
DROP TABLE customer_review;

-- (or force drop if there are dependencies)
-- DROP TABLE customer_review CASCADE;

-- 4) Count how many rentals have not been returned yet
SELECT COUNT(*)
FROM rental
WHERE return_date IS NULL;

-- 5) Find the 30 most expensive movies that have not been returned yet
SELECT
  f.film_id,
  f.title,
  f.replacement_cost
FROM
  rental r
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
WHERE
  r.return_date IS NULL
ORDER BY
  f.replacement_cost DESC
LIMIT 30;

-- 6) Find the films based on the descriptions

-- 6.1 The first film: about a sumo wrestler, with actress Penelope Monroe
SELECT
  f.film_id,
  f.title
FROM
  film f
INNER JOIN film_actor fa ON f.film_id = fa.film_id
INNER JOIN actor a ON fa.actor_id = a.actor_id
WHERE
  a.first_name = 'Penelope'
  AND a.last_name = 'Monroe'
  AND f.description ILIKE '%sumo%';

-- 6.2 The second film: a short documentary (<1 hour), rated "R"
SELECT
  film_id,
  title
FROM
  film
WHERE
  length < 60
  AND rating = 'R'
  AND description ILIKE '%documentary%';

-- 6.3 Find the customer_id of Matthew Mahan
SELECT customer_id
FROM customer
WHERE first_name = 'Matthew' AND last_name = 'Mahan';

-- Suppose the result: customer_id = 5

-- 6.4 The third film: rented by Matthew Mahan, paid over $4, returned between July 28 and August 1, 2005
SELECT DISTINCT
  f.film_id,
  f.title
FROM
  rental r
INNER JOIN payment p ON r.rental_id = p.rental_id
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
WHERE
  r.customer_id = 5
  AND p.amount > 4.00
  AND r.return_date BETWEEN '2005-07-28' AND '2005-08-01';

-- 6.5 The fourth film: watched by Matthew Mahan, contains "boat" in the title or description, expensive to replace
SELECT DISTINCT
  f.film_id,
  f.title,
  f.replacement_cost
FROM
  rental r
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
WHERE
  r.customer_id = 5
  AND (
    f.title ILIKE '%boat%'
    OR f.description ILIKE '%boat%'
  )
ORDER BY
  f.replacement_cost DESC;

