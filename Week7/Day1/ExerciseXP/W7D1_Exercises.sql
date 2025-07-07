-- Exercise 1: Building a Comprehensive Dataset for Employee Analysis
CREATE TABLE df_employee AS
SELECT
    s.employee_id || '_' || DATE(s.date) AS id,
    DATE(s.date) AS month_year,
    s.employee_id,
    s.employee_name,
    e.employee_name_emp,
    e."GEN(M_F)" AS gender,
    e.age,
    s.comp_name,
    c.company_city,
    c.company_state,
    c.company_type,
    s.func,
    f.function_group,
    REPLACE(s.salary, ',', '.') * 1 AS salary_numeric
FROM salaries s
LEFT JOIN employees e
    ON CAST(e.employee_code_emp AS TEXT) = CAST(s.employee_id AS TEXT)
LEFT JOIN companies c
    ON CAST(c.rowid AS TEXT) = CAST(s.comp_code AS TEXT)
LEFT JOIN functions f
    ON CAST(f.function_code AS TEXT) = CAST(s.func_code AS TEXT);
    
-- Ex.2
-- run the following SQLite request and observe your new table.
SELECT * FROM df_employee;

-- Remove all unwanted spaces from all text columns using TRIM
UPDATE df_employee
SET
    id = TRIM(id),
    employee_name = TRIM(employee_name),
    employee_name_emp = TRIM(employee_name_emp),
    gender = TRIM(gender),
    comp_name = TRIM(comp_name),
    company_city = TRIM(company_city),
    company_state = TRIM(company_state),
    company_type = TRIM(company_type),
    func = TRIM(func),
    function_group = TRIM(function_group);

-- Check for NULL values and empty values.
SELECT *
FROM df_employee
WHERE
    id IS NULL OR id = ''
    OR month_year IS NULL OR month_year = ''
    OR employee_id IS NULL OR employee_id = ''
    OR employee_name IS NULL OR employee_name = ''
    OR salary_numeric IS NULL;

-- Delete rows of the detected missing values.
DELETE FROM df_employee
WHERE salary_numeric IS NULL
OR salary_numeric = '';

SELECT *
FROM df_employee
LIMIT 10;

--Ex.3
SELECT
    comp_name,
    COUNT(DISTINCT employee_id) AS employee_count
FROM
    df_employee
GROUP BY
    comp_name
ORDER BY
    employee_count DESC;

--Ex.4
-- Считаем сотрудников по городу и процент от общего числа
SELECT
    COALESCE(company_city, 'Unknown') AS company_city,
    COUNT(DISTINCT employee_id) AS employee_count,
    ROUND(
        COUNT(DISTINCT employee_id) * 100.0 /
        (SELECT COUNT(DISTINCT employee_id) FROM df_employee),
        2
    ) AS percentage_of_total
FROM
    df_employee
GROUP BY
    COALESCE(company_city, 'Unknown')
ORDER BY
    employee_count DESC;

-- Ex.5
-- 🎯 Задача 1: Минимум и максимум сотрудников по месяцам
WITH monthly_counts AS (
    SELECT
        month_year,
        COUNT(DISTINCT employee_id) AS employee_count
    FROM
        df_employee
    GROUP BY
        month_year
)
SELECT
    *
FROM
    monthly_counts
WHERE
    employee_count = (SELECT MIN(employee_count) FROM monthly_counts)
    OR
    employee_count = (SELECT MAX(employee_count) FROM monthly_counts)
ORDER BY
    employee_count;

--------------------------------------------------------

-- 🎯 Задача 2: Среднее количество сотрудников по месяцам по функциям
WITH monthly_function_counts AS (
    SELECT
        month_year,
        function_group,
        COUNT(DISTINCT employee_id) AS employee_count
    FROM
        df_employee
    GROUP BY
        month_year,
        function_group
)
SELECT
    function_group,
    ROUND(AVG(employee_count), 2) AS avg_employees_per_month
FROM
    monthly_function_counts
GROUP BY
    function_group
ORDER BY
    avg_employees_per_month DESC;

--------------------------------------------------------

-- 🎯 Задача 3: Средняя зарплата за год
SELECT
    SUBSTR(month_year, 1, 4) AS year,
    ROUND(AVG(salary_numeric), 2) AS avg_salary
FROM
    df_employee
GROUP BY
    year
ORDER BY
    year;
