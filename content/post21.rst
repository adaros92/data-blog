****************************
Ranking Windows: A SQL Story
****************************

:date: 2022-06-09 19:04
:modified: 2022-06-09 19:04
:tags: Programming
:category: Programming
:authors: Adams Rosales
:summary: Using SQL window functions and the differences between row_number, rank, and dense rank

Window Functions 101
####################
Window functions or analytical functions, as they are sometimes called, are nothing more than functions that can be
applied at different granularities within your data in the same select statement.

A traditional SQL function is applied for only one granularity per select statement. For example, take the following SUM
over a table of orders.

.. code-block:: sql

    SELECT ORDER_DATE, SUM(UNITS) UNITS_SOLD
    FROM ORDERS
    GROUP BY ORDER_DATE

The granularity here is order date. We are summing all of the units sold for each date. If we were to add another function
like count of records,

.. code-block:: sql

    SELECT ORDER_DATE, SUM(UNITS) UNITS_SOLD, COUNT(1) RECORDS
    FROM ORDERS
    GROUP BY ORDER_DATE

that too would be per order date. So any function we include in this single select scope can only be for one granularity.

But now let's say we want to vary each one of these functions so that they are calculated over different ranges of data
in a single select statement. Say for example, we wanted the total number of units per order date as well as the total
amount in the entire table. We can do something like this with the help of window functions:

.. code-block:: sql

    SELECT
        ORDER_DATE,
        SUM(UNITS) OVER (PARTITION BY ORDER_DATE) UNITS_SOLD,
        SUM(UNITS) OVER () TOTAL_UNITS
    FROM ORDERS

What you actually get here is a bit tricky if you're not used to working with these. For that, it helps to look at some
dummy data.

.. image:: /static/post21/post21_1.png
  :width: 50%
  :alt: A table of orders

And the result of the query above is:

.. image:: /static/post21/post21_2.png
  :width: 50%
  :alt: A table of orders after some window functions

Notice how the granularity here is order_id (one record per order_id). We don't affect this granularity at all
with our query because we're not grouping by any column here. So the result set stays at the same granularity of one
row per order_id. So the number of order_date records remains the same as in the original data. But, if you take
a look at the two measures, you'll see they've been aggregated over other granularities or "windows" of data. The first
measure is the total number of units per order_date. This is the case because we partitioned by order_date in the window
function. The second measure is the total number of units in the entire table, because we didn't partition over anything,
so it ran the sum on the entire data.

The partition keyword essentially determines what window you are running your aggregation over. If it's not specified,
the function will run over the entire data. Let's visualize this!

With ``SUM(UNITS) OVER (PARTITION BY ORDER_DATE) UNITS_SOLD``, we perform the sums over the following windows of data.

.. image:: /static/post21/post21_3.png
  :width: 50%
  :alt: A table split by order_date

But with ``SUM(UNITS) OVER () TOTAL_UNITS``, the window is the entire table.

.. image:: /static/post21/post21_4.png
  :width: 50%
  :alt: A table with no partitioning

Ranking With Window Functions
#############################
So now that you sort of got the hang of window functions, let's look at a specific application used to rank data. By
that I mean assigning numbers to each record in the data based on the order of some column.

Row Number
----------
Let's use the same dummy data. Take the following query as an example.

.. code-block:: sql

    SELECT
        ORDER_ID,
        ORDER_DATE,
        UNITS,
        ROW_NUMBER() OVER (PARTITION BY ORDER_DATE ORDER BY UNITS DESC) RN
    FROM ORDERS

This will add a sequential number (1, 2, 3, etc.) to each row based on how many units were sold. But, since
we're partitioning by order_date, it will only count within each order_date window. This means, that each order date
records will have individual row number series counting up to the total number of records for that order date. Here,
take a look at the result.

.. image:: /static/post21/post21_5.png
  :width: 75%
  :alt: Row number example when partitioning by order date

Notice how we've assigned a row number in descending order by the total number of units in the each order. The order with
the most units gets a 1, followed by 2, then 3, etc. But, when we reach a new order date, this row number restarts so
that units are ranked within individual order dates. If on the other hand, we would have run the following query,

.. code-block:: sql

    SELECT
        ORDER_ID,
        ORDER_DATE,
        UNITS,
        ROW_NUMBER() OVER (ORDER BY UNITS DESC) RN
    FROM ORDERS

without specifying any partition argument in the ROW_NUMBER function, the result would have been as follows.

.. image:: /static/post21/post21_6.png
  :width: 75%
  :alt: Row number example without a partition

In this case, the row numbers don't reset all all. We simply rank all of the order records by the number of units sold.
The order with the largest number of units in the entire table comes first, without any regard to the order date like
before.

Rank
----
With the row number function, we assign a number to each row sequentially no matter what. If there are duplicate values,
such as unit values 3, 2, and 1 in the example above, we still increment the row number by 1. With the rank function,
though, any repeated values we're ranking by get the same rank number. Take the following query:

.. code-block:: sql

    SELECT
        ORDER_ID,
        ORDER_DATE,
        UNITS,
        RANK() OVER (ORDER BY UNITS DESC) RANK
    FROM ORDERS

This again doesn't partition by anything so there will be no resets of the ranking by order date. However, take a look
at the rank column. You'll notice that duplicate unit values get the same rank. When the unit value changes, the rank
continues as if we had ranked consecutively. For example, there are 2 repeating unit values of 3. When we reach unit value
2, the rank continues to 5, since there were 2 repeating 3s.

.. image:: /static/post21/post21_7.png
  :width: 75%
  :alt: Rank without partition

There are 3 repeating values of 2, so when we continue on to unit value 1, the rank goes from 5 to 8 (5 + 3).

Dense Rank
----------
Dense rank also assigns the same rank to repeating values, but doesn't do the same gap as rank does after repeating
values. It will just continue counting up without any breaks. Take for example, the following query:

.. code-block:: sql

    SELECT
        ORDER_ID,
        ORDER_DATE,
        UNITS,
        DENSE_RANK() OVER (ORDER BY UNITS DESC) RANK
    FROM ORDERS

which yields the following,

.. image:: /static/post21/post21_8.png
  :width: 75%
  :alt: Dense rank without partition

If there are any repeating values, we repeat the rank, but then continue on to the next consecutive rank number after
that. So when there 2 unit values of 3, we assign them both the rank of 3 and continue on to rank 4 for unit value
2 without skipping any ranks.

Practical Use Cases
###################
So why should you care? Well, window functions make it easy to perform complex calculations while reducing the
amount of logic written. Here are some applications I come across often at work.

Top N values by some segment
----------------------------
Calculate the top 2 salaries by department given a table of employees.

.. image:: /static/post21/post21_9.png
  :width: 50%
  :alt: Top 2 salaries by department data

Answer:

.. code-block:: sql

    SELECT
        DEPARTMENT
        , EMPLOYEE_ID
    FROM (
        SELECT
            EMPLOYEE_ID
            , DEPARTMENT
            , RANK() OVER (PARTITION BY DEPARTMENT ORDER BY SALARY DESC) RNK
        FROM EMPLOYEE
    ) WHERE RNK <= 2

We partition by department so the ranking happens individually for each department by salary descending. Remember that
the grain of the data remains at the employee_id level because we are just restricting the grain within the scope
of the function. So the result is that we get a rank for each employee in their individual departments. We can then filter
on that rank to get the top 2. See how the result of the subquery would look for more clarity.

.. image:: /static/post21/post21_10.png
  :width: 50%
  :alt: Top 2 salaries by department inner query data

The red squares are the windows created by the partition on department and the highlighted values are what we filter on
to retrieve the final result. See how it gets the employees with the top 2 salaries by department?

% of total by segment
---------------------
Get the percentage of total employees working in each department from the same data above.

Answer:

.. code-block:: sql

    SELECT DISTINCT
        DEPARTMENT
        , COUNT(1) OVER (PARTITION BY DEPARTMENT) * 1.00
            / COUNT(1) OVER () * 100 PERCENT_OF_TOTAL
    FROM EMPLOYEE

This calculates the count of records in this table or employees since it's one record per employee by department and
divides by the total count of records in the table. We add a distinct here because the granularity of the table is
employee_id.

Before distinct:

.. image:: /static/post21/post21_11.png
  :width: 50%
  :alt: Department count of total before distinct

After distinct:

.. image:: /static/post21/post21_12.png
  :width: 50%
  :alt: Department count of total after distinct

Now try to answer the same questions without using window functions. Hint: it's a lot more code :).