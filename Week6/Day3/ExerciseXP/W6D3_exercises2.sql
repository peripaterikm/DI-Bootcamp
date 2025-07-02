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

