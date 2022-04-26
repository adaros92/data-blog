********************
Stars and Snowflakes
********************

:date: 2020-12-13 00:00
:modified: 2020-12-13 00:00
:tags: Data Modeling
:category: Data Modeling
:authors: Adams Rosales
:summary: Structuring data in OLAP systems
:header_cover: /static/post5/header.jpg

Requirements in an OLAP System
##############################
In my previous `Be Normal <https://decipheringbigdata.com/be-normal.html>`_ post I mentioned that normalization is good
for OLTP but not so much for OLAP systems. The way you adapt data models for OLAP purposes is by de-normalizing tables in
a normalized data model. At a high level this process involves precomputing certain features and joining tables together
for our analyst customers.

Analysts typically need to answer complex business questions dealing with certain "facts" about a business. For example,
what do revenues look like over time? What category of product sells the best during sale periods? Which apps are the
top performing as measured by daily active users? With a highly normalized database, the analysts would have to write
complex queries to join many different tables together and aggregate up individual records to produce the summarized
figures they need in order to answer these questions.

Here I discuss how we may go about making this process easier by designing an OLAP data model with the help of two buzz
phrases in the data modeling community: star and snowflake schemas.

Star Schemas
############
The basic premise of a star schema is to organize your data such that you store your key business measures that analysts
care about in one or many fact tables. How granular you go with these measures is really up to the needs of the business
and what types of questions we want to answer with the data.

These fact tables will then have `foreign keys <https://www.techopedia.com/definition/7272/foreign-keyl>`_ to other
tables in the database that describe the numerical facts stored in the fact tables. These types of tables are called
dimensions and commonly deal with locations, time, products, organizations, and people.

This gives us a central denormalized location where the crucial measures are stored so that we don't have to join a
bunch of system tables together to derive those measures and some lookup tables that we can easily join to segment the
data depending on the task at hand.

Take the following normalized set of tables from the `previous post <https://decipheringbigdata.com/be-normal.html>`_.

.. image:: /static/post4/post4_complexdiagram.jpg
  :width: 90%
  :alt: Complex OLTP diagram

Some of the business questions we may want to ask about these data are:

- How much sales revenue was brought in over some time period by product category?
- How many orders were processed by store?
- How many units were shipped by location?

The facts here are most likely to be units, orders, and dollar revenue and we should be able to segment these by the
different groups of attributes shown - sales staff, stores, customer locations, and product categories. Here is
one option for a star schema to capture these requirements.

.. image:: /static/post5/post5_star.jpg
  :width: 100%
  :alt: Sample star schema

We have pre-aggregated the measures we care about and stored them with references to all of the descriptive attributes
to segment by in one fact_orders table. The dimensions are other denormalized tables that combine all characteristics
of the specific subjects in one table per subject. This simplifies the OLTP model substantially and makes it a lot
easier to answer the business questions above.

For example, here is the SQL to answer how much sales revenue was brought in over some time period by product category.
${PERIOD_START} and ${PERIOD_END} are user inputs for the time period in question.

.. code-block:: sql

    SELECT
            FO.ORDER_DATE
            , DP.PRODUCT_CATEGORY
            , SUM(FO.ORDER_AMOUNT) TOTAL_ORDER_AMOUNT

    FROM    FACT_ORDERS FO

    JOIN    DIM_PRODUCT DP ON FO.PRODUCT_ID = DP.PRODUCT_ID

    WHERE   FO.ORDER_DATE BETWEEN ${PERIOD_START} AND ${PERIOD_END}

    GROUP BY
            FO.ORDER_DATE
            , DP.PRODUCT_CATEGORY

Compare that to the logic required to get the same answer but from the normalized OLTP data model.

.. code-block:: sql

    SELECT
            SOH.OrderDate ORDER_DATE
            , PC.Name PRODUCT_CATEGORY
            , SUM(SOD.OrderQty * SOD.UnitPrice) TOTAL_ORDER_AMOUNT

    FROM    SalesOrderDetail SOD

    JOIN    SalesOrderHeader SOH  ON SOD.SalesOrderID = SOH.SalesOrderID
    JOIN    Product P ON SOD.ProductID = P.ProductID
    JOIN    ProductSubcategory PSC ON P.ProductSubcategoryID = PSC.ProductSubcategoryID
    JOIN    ProductCategory PC ON PSC.ProductCategoryID = PC.ProductCategoryID

    WHERE   SOH.OrderDate BETWEEN ${PERIOD_START} AND ${PERIOD_END}

    GROUP BY
            SOH.OrderDate
            , PC.Name

That's a lot of joins!

Snowflake Schemas
#################
The premise of snowflake schemas is essentially the same as star schemas but instead of denormalizing dimensions into
as few tables per subject as possible we instead normalize the dimensions. This is done to optimize storage space by
avoiding redundant information and make updates more efficient.

In some cases your facts and dimensions may share many-to-many relationships. Storing the same attributes repeatedly for
each fact_key and dim_key combination can take up a lot of unnecessary space. It's preferred in these cases to create a
separate table that just stores the relationship between fact_key and dim_key without any additional attributes to use as
a bridge table from the fact to the dim. Other times you may not need some dimension attributes as often as others
so you may choose to store them separately in a different table so that queries are more efficient (in row-based databases).

There's really no rule about how much normalization there should be. It's often dictated by the systems the data are
sourced from, the ETL processes in place, personal/team preference, what other data are stored alongside the schemas,
where the data are stored in, etc. What is fairly constant though is that snowflake schemas will most often lead to
worse query performance due to the extra joins that need to happen between fact and dim tables to answer business
questions.

Are These Modeling Techniques Used In Practice?
###############################################
It depends. I have found that interviewers for data engineering positions focus a lot on star schema modeling but I have not
actually come across true star schemas that often on the job. I have seen relics of star schemas with dim tables here and
there but it always seems like people just abandon the approach and data tend to merge together into a set of core tables
combining both dims and facts.

Part of the reason why is that nowadays companies are moving away from traditional data warehousing techniques and
storing the data in key-value/object stores like AWS S3. With tools like Spark on EMR and Presto/Athena, data doesn't
really need to be stored in any data warehouse for analysts to derive value from it. They can also take on different
types of structure where the data are completely denormalized into single datasets or split together in ways that don't
really adhere to any sort of schema. The types of tools used to consume the data offer a lot more flexibility in how
the data are read and manipulated than traditional data warehousing solutions.

When data are stored in data warehouses like Redshift, they're typically stored in single tables that combine both facts
and dimensions. This is mainly because with efficient compute behind the scenes (either Redshift or Spark on data stored
in S3), it's easy to recompute large amounts of data (up to hundreds of terabytes) in a relatively short period of time.
That is if a dimension changes, the dataset owners can easily backfill that dimension into the one table that also has
facts within a matter of hours or days.

I think these techniques are still worth understanding as logical data models, but they're not requirements
when physically storing the data.
