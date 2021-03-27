*********************
Redshift Optimization
*********************

:date: 2021-03-26 00:00
:modified: 2021-03-26 00:00
:tags: Data Engineering
:category: Data Engineering
:authors: Adams Rosales
:summary: How to improve query efficiency on AWS Redshift
:header_cover: /static/post14/header.jpg

An Overview of Redshift
#######################
`Redshift  <https://aws.amazon.com/redshift/>`_ is a fully managed cloud data warehouse available on AWS. It's the most
popular data warehousing solution in use today due to its efficient columnar data storage, distributed parallel
processing capabilities, and seamless scalability. It also integrates quite well with other AWS services like S3, Athena,
and Glue, making it easier to move data in and out of the warehouse in addition to simply using Redshift as a compute
engine on data physically stored in S3 without having to move the data out of S3.

A Redshift cluster includes a single driver node and a collection of worker nodes. How many worker nodes exactly depends
on the node types used (dc2, ds2, ra3) and how the cluster was configured when launched. Typically the number of worker
nodes ranges from 1-128. These worker nodes are further divided into slices, which represent compute and storage units
using equally sized portions of each node's memory and disk space. The number of slices per node also depends on the
types of nodes being used, ranging from 2 to 32 slices per node.

.. image:: /static/post14/post14_redshift_diagram.jpeg
  :width: 100%
  :alt: A diagram of the Redshift architecture

The data are physically stored in the worker node slices and each slice is operated on in parallel to achieve
distributed data processing. How the data are distributed among the slices is one of the important considerations an
engineer must have to allow efficient access to that data. There are three different ways to do this:

- Even - a round-robin distribution of records. Imagine going down a list of rows and alternating slices as you go so
  that the data are evenly split across all the nodes.
- All - includes a full copy of the data in the first slice of each worker node.
- Key - acts like a hash table by first creating a unique hash key off of a column specified by the user during table
  creation and then co-locating the records with the same hashed value in the same slices. This means that all records
  pertaining to a certain column's value will be in the same slice together (for example, distributing on country code
  will result in all US records being stored in the same slice).

While you can think of the records as being distributed a certain way according to the table's distribution style, the
actual data is organized on disk such that the individual columns are stored in separate files, which are further
broken down into 1MB blocks on disk. Because the data are stored in a column-oriented format as opposed to a row-oriented
format where individual files contain entire rows of data, fewer data need to be retrieved for analytical queries
which only need certain column from the data. It also makes it possible to compress the block files more than if they
contained entire rows of data because only the same type of data are stored together in single files depending on the
column types.

Optimizing Query Filters
########################

Optimizing Joins and Aggregations
#################################

Optimizing Spectrum Queries
###########################

Use the Explain Plan
####################

Additional Resources
####################

`Best practices overview  <https://www.youtube.com/watch?v=13iIj34nkQE>`_ -
a good overview of Redshift best practices shown during the most recent AWS re:Invent

`Advanced table design playbook  <https://aws.amazon.com/blogs/big-data/amazon-redshift-engineerings-advanced-table-design-playbook-preamble-prerequisites-and-prioritization/>`_ -
the single best resource on Redshift optimization I've read to date

`Using Automatic Table Optimization  <https://aws.amazon.com/blogs/big-data/optimizing-tables-in-amazon-redshift-using-automatic-table-optimization/>`_ -
a relatively new feature that recommends optimal distribution and sort key configurations from data on historical query
performance