*********
Be Normal
*********

:date: 2020-12-12 00:00
:modified: 2020-12-12 00:00
:tags: Data Modeling
:category: Data Modeling
:authors: Adams Rosales
:summary: The normal forms of OLTP data modeling
:header_cover: /static/post4/header.jpg

What is Data Normalization?
###########################
Normalization is a fancy term to describe the process of organizing data into relations or tables to remove redundancy
through decomposition.

There are 5 different forms of normalization:

1. First Normal Form
2. Second Normal Form
3. Third Normal Form
4. Boyce and Codd Normal Form
5. Fourth Normal Form

As we go down this list data becomes less redundant and the more tables we end up with in our database. I'll walk
through concrete examples of these different forms below!

A World Without Normalization
#############################
First let's take a look at what lack of data normalization means. It helps to picture a giant spreadsheet that collects
all kinds of data about some subject. Let's say someone in your neighborhood keeps a spreadsheet of every single person
that lives in the neighborhood. It contains the relationships between neighbors in separate columns, the colors of the
houses, how many cars each house has, when deliveries and public services like trash collection pass by each house, etc.

It looks something like this (shout out to https://www.behindthename.com/random/).

.. image:: /static/post4/post4_normalization1.jpg
  :width: 100%
  :alt: Creepy neighbordhood spreadsheet

If keeping a creepy list did not raise any red flags before, this atrocity of a data structure should. It's not difficult to
imagine how difficult it would be to maintain data in such a list as it grows. Updates would be a pain! For example,
if a neighbor paints their house you would need to update each household member's record in this list, not just
a single house record. If Alf has a baby, you will need to add a family_3 column to record the relationship between the
existing 3 members and the new addition to the family. This affects all records in the table. Same thing if someone gets
a new car or the garbage collection routes change.

So let's say your creepy neighbor wants to do better. What can they do?

First Normal Form
#################
First normal form refers to data models that have only atomic values in each column and where no table has repeating
groups. Atomic values are simply those that can't be broken down into many values. Fortunately all of the values in
this spreadsheet are atomic. If we had a column called cars and in that column we had a record like
Toyota Camry, Toyota Camry, Toyota Corolla then this value would need to be broken down so that each value is stored
in its own record.

What we do have here though are repeating groups. This refers to groups of values that can repeat for any one of the
primary keys in the tables. In this case, values that can repeat for each neighbor stored in the spreadsheet. Those
groups are the car, family, and friend columns.

The solution to get rid of these repeating groups is to split the one table into 3 individual tables - neighbors,
vehicles, and relationships.

.. image:: /static/post4/post4_fnf.jpg
  :width: 100%
  :alt: First normal form example

The vehicles table will have the name of each person and a vehicle in their household. It's easier to update the vehicles
in each household now because we don't need to amend all records in the table by changing a column. We can simply amend,
delete, or add rows in the vehicles table. The same is true for relationships between neighbors. To add new ones we can
simply append rows to the relationships table.

Second Normal Form
##################
Second normal form dictates that "all non-key attributes should be functionality dependent on the primary key." What
this means in plain English is that each table should contain only information about one topic and all attributes in
that table should serve to describe the topic and nothing else.

For example, in our first normal form model, the color of the house and the garbage routes are stored with the neighbors
table. The primary key of that table is the neighbor's name. Neither the house color nor the garbage route depend on
each neighbor. They instead depend solely on the house where the neighbors live in. Each house is uniquely identified
by an address in our data so each of these attributes should be stored in its own table as shown below.

.. image:: /static/post4/post4_snf.jpg
  :width: 100%
  :alt: Second normal form example

The advantage of this data model is that we remove the additional redundancy of having attributes related to the address
in the neighbors table where addresses can be repeated for each neighbor that lives in the same house as other neighbors.
For example, if we wanted to update the color of the house at 12234 NE 20th ST, we would only need to do it once in the
location_attributes table instead of 3 times in the neighbors table.

It also means that if we delete any records from the neighbors table because people move out of the neighborhood, we
will still preserve all of the information related to the houses at the locations where they used to live.

Third Normal Form
#################
Tables should contain columns that are non-transitively dependent on the primary key.

.. image:: https://media.giphy.com/media/zjQrmdlR9ZCM/giphy.gif
  :width: 60%
  :alt: Confused Marky Mark

This one sounds complicated but it actually just means that we shouldn't store columns that depend on the primary key
of a table AND on other columns in that table. For example, our garbage_collection table has a column for the route
number and for the day when the garbage truck swings by at an address. Garbage route depends on the address and the day
of collection depends on the garbage route so a transitive dependency exists.

The reason why we don't want these types of dependencies in our tables is because updates have to change multiple
attributes in a table when one attribute in the transitive dependency is updated, which can lead to inconsistencies.
For example, if we assign a different route to an address and that route runs on a different date then we also need to
update the date of collection for the address. We need to make sure to update both or else our data will be wrong.

To fix it we can just add an additional table that stores the relationship between route and collection day.

.. image:: /static/post4/post4_tnf.jpg
  :width: 100%
  :alt: Third normal form example

Boyce and Codd Normal Form
##########################
This normal form adds a minor restriction to the third normal form - attributes should depend only on a super key (a
column or collection of columns that uniquely identify records in a table).

Our data model above is both in 3NF and BCNF but suppose instead that we also stored the garbage collection crew number
in the garbage_routes table. The individual crew would determine the collection_day based on when they work in the week
so collection_day would depend on the crew number. However, crew number would not be a super key because one crew can
service multiple routes (crew number would not uniquely identify records in this table). This scenario would satisfy
3NF constraints but not BCNF constraints.

We could fix a scenario like this by splitting the garbage_routes table into two, one storing the relationship between
route and crew and another storing the relationship between crew and collection_day.

.. image:: /static/post4/post4_bcnf.jpg
  :width: 100%
  :alt: BCNF example

Fourth Normal Form
##################
Finally, the fourth normal form requires us to avoid multi-valued dependencies in tables. This means that for any
dependency A -> B in a table, if multiple values of B exist for any single value of A and there are more than 2 columns
in that table then there is a multi-valued dependency violating the 4NF.

Our BCNF data model above also satisfies 4NF but what if a single crew had multiple collection days and we also stored
the truck_id of each crew in the crew_collection_days table. Truck_id and collection_day here are independent of each
other so BCNF is satisfied but this would be a multi-valued dependency because the key crew_number can have multiple
collection days and can drive one or more trucks

We can further normalize this by splitting crew_collection_days into two tables, one that maintain the one to many
relationship between crew_number and collection_day and another the one to many relationship between crew_number and
truck_id.

.. image:: /static/post4/post4_4nf.jpg
  :width: 100%
  :alt: Fourth normal form example

Normalize All The Tables?
#########################
Normalization kicks ass, right? Well, not always. There are cases where we may want to do the opposite of normalizing
or as they say in the biz, "de-normalize."

Normalization works well in OLTP databases where tables are strongly tied to engineering systems that update them. These
are your point-of-sale, online checkout, messaging applications, etc. which are organized into individual
objects that maintain state and functionality for very specific components of the broader systems. The individual
objects may not be aware of other objects' state and so can only update the data for the specific table that backs
the one component. For example, a post class that's part of a forum web application updating a post table which just
contains information about individual posts on the forum and nothing else.

For OLAP workloads that seek to answer overarching business questions, normalized databases can actually be
a hindrance. This is because to answer the types of analytical questions typically asked in these settings, an analyst
would need to first understand how all of the tables in a complex model like the one shown below fit together and then
write a massive query to join all of the tables together. Such a query would be inefficient and error-prone.

.. image:: /static/post4/post4_complexdiagram.jpg
  :width: 90%
  :alt: Complex OLTP diagram

For example, say an analyst were asked to produce a summary of total quantity ordered for product categories that were
under special offer during some time range. The analyst would need to join the SalesOrderHeader, SalesOrderDetail,
SpecialOfferProduct, SpecialOffer, Product, ProductSubcategory, and ProductCategory tables together to produce an
answer. Not a fun exercise!

In these cases, pre-joining tables together or "de-normalizing" makes sense. We're willing to break normalization rules
and introduce some redundancy to our data models in order to make analytical queries more efficient and make the lives
of our analytics customers easier. This is where star and snowflake schemas come in handy but that's a different topic
for another day!