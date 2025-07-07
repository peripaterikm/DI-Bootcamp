-- SELECT e.employee_id, e.first_name, e.last_name, e.department_id, s.sales,
--        RANK() OVER (PARTITION BY e.department_id ORDER BY s.sales DESC) AS sales_rank,
--        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY s.sales DESC) AS dense_sales_rank
-- FROM employees e
-- JOIN sales_data s ON e.employee_id = s.employee_id;

-- SELECT employee_id, first_name, last_name, department_id, salary,
--        NTILE(4) OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_quartile
-- FROM employees;

-- SELECT employee_id, first_name, last_name, salary,
--        SUM(salary) OVER (PARTITION BY department_id ORDER BY salary) AS running_total
-- FROM employees;

-- SELECT employee_id, first_name, last_name, salary,
--        SUM(salary) OVER (ORDER BY salary RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_sum
-- FROM employees;

-- SELECT employee_id, first_name, last_name, salary,
-- 	NTILE(2) OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_quartile
-- FROM employees;

-- SELECT e.employee_id, e.first_name, e.last_name, e.department_id, s.sales,
--        SUM(s.sales) OVER (PARTITION BY e.department_id ORDER BY e.employee_id) AS running_total
-- FROM employees e
-- JOIN sales_data s ON e.employee_id = s.employee_id;


SELECT employee_id, first_name, last_name,
       ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num
FROM employees;

SELECT
  e.department_id,
  e.first_name, e.last_name, e.salary,
  SUM(e.salary) OVER (
    PARTITION BY e.department_id
    ORDER BY e.salary DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS cumulative_salary
FROM
  employees e
ORDER BY
  e.department_id,
  e.salary DESC;
