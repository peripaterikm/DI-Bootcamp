-- ========================================
-- CREATE TABLE AND INSERT SAMPLE DATA
-- ========================================

-- Create the employees table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date VARCHAR(20),
    department VARCHAR(50)
);

-- Insert 20 sample records
INSERT INTO employees (employee_id, employee_name, salary, hire_date, department) VALUES
(1, 'Amy West', 60000.00, '2021-01-15', 'HR'),
(2, 'Ivy Lee', 75000.50, '2020-05-22', 'Sales'),
(3, 'joe smith', 80000.75, '2019-08-10', 'Marketing'),
(4, 'John White', 90000.00, '2020-11-05', 'Finance'),
(5, 'Jane Hill', 55000.25, '2022-02-28', 'IT'),
(6, 'Dave West', 72000.00, '2020-03-12', 'Marketing'),
(7, 'Fanny Lee', 85000.50, '2018-06-25', 'Sales'),
(8, 'Amy Smith', 95000.25, '2019-11-30', 'Finance'),
(9, 'Ivy Hill', 62000.75, '2021-07-18', 'IT'),
(10, 'Joe White', 78000.00, '2022-04-05', 'Marketing'),
(11, 'John Lee', 68000.50, '2018-12-10', 'HR'),
(12, 'Jane West', 89000.25, '2017-09-15', 'Sales'),
(13, 'Dave Smith', 60000.75, '2022-01-08', NULL),
(14, 'Fanny White', 72000.00, '2019-04-22', 'IT'),
(15, 'Amy Hill', 84000.50, '2020-08-17', 'Marketing'),
(16, 'Ivy West', 92000.25, '2021-02-03', 'Finance'),
(17, 'Joe Lee', 58000.75, '2018-05-28', 'IT'),
(18, 'John Smith', 77000.00, '2019-10-10', 'HR'),
(19, 'Jane Hill', 81000.50, '2022-03-15', 'Sales'),
(20, 'Dave White', 70000.25, '2017-12-20', 'Marketing');

-- ========================================
-- 1. HANDLE MISSING VALUES
-- ========================================

-- Identify records with NULL in any field
SELECT *
FROM employees
WHERE department IS NULL
   OR employee_name IS NULL
   OR salary IS NULL
   OR hire_date IS NULL;

-- Replace NULL department with 'Unknown'
UPDATE employees
SET department = 'Unknown'
WHERE department IS NULL;

-- ========================================
-- 2. CHECK FOR DUPLICATE ROWS
-- ========================================

-- Find duplicate records (if any)
SELECT employee_name, hire_date, department, COUNT(*)
FROM employees
GROUP BY employee_name, hire_date, department
HAVING COUNT(*) > 1;

-- ========================================
-- 3. FIX INCONSISTENT NAMING (CAPITALIZATION)
-- ========================================

-- Update inconsistent lowercase name to proper case
UPDATE employees
SET employee_name = 'Joe Smith'
WHERE employee_id = 3;

-- ========================================
-- 4. VERIFY DATE FORMAT
-- ========================================

-- Check for invalid date formats
SELECT *
FROM employees
WHERE hire_date NOT LIKE '____-__-__';

-- ========================================
-- 5. IDENTIFY OUTLIERS IN SALARY
-- ========================================

-- Get salary min, max, and average
SELECT
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    AVG(salary) AS avg_salary
FROM employees;

-- Show top 3 highest salaries
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 3;

-- ========================================
-- 6. STANDARDIZE DEPARTMENT NAMES
-- ========================================

-- List unique department names
SELECT DISTINCT department FROM employees;

-- Example: Standardize 'sales' to 'Sales' (if needed)
-- (No lowercase 'sales' in this dataset, but here is the example)
-- UPDATE employees
-- SET department = 'Sales'
-- WHERE LOWER(department) = 'sales';

-- ========================================
-- 7. FINAL CHECK AND OUTPUT
-- ========================================

-- Show cleaned data
SELECT *
FROM employees
ORDER BY employee_id;

-- Get average salary per department
SELECT
    department,
    ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;
