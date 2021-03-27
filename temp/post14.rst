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

These column block files also benefit from an additional optimization called zone mapping. Zone maps are metadata stored
in memory that provide the min and max values of the data in each block. When any sort of filtering is applied
on the data (for example, where date between '2021-01-01' and '2021-01-31'), Redshift is able to skip files where the
values being filtered for are not within the min and max range contained in the zone maps. This reduces expensive I/O from
disk thereby improving performance substantially.

.. image:: /static/post14/post14_zonemaps.png
  :width: 100%
  :alt: A diagram of how zone maps work in Redshift

How effective these zone maps are at reducing the data scanned depends on how well the data are sorted on disk.
As shown in the diagram above, if the data are not sorted, files can contain wide ranges of values in the zone maps,
rendering them pretty useless at reducing the amount of files that need to be read. Thankfully, Redshift provides
the ability to physically sort the data on disk via sort keys, which are defined at table creation time along with
distribution styles. There are two types of sort keys:

- Compound - sorts data based on the columns in the order they're specified in. It behaves the same way as order by
  column1, column2, column3, etc. It will first sort on column1, followed by column2, then column3, etc. These are used
  most often and it's the default type of sort key applied by Redshift. They work well when there are clear filtering
  patterns on the data, during aggregations which require grouping and/or sorting, and joins.
- Interleaved - uses Z-order curves through N-dimensional space to give equal weights to the columns being used in the
  sort key. Interleaved sort keys are not used much in practice but they do provide an advantage with very large tables and when
  there is no clear filtering pattern on the data (users may filter by many different columns when querying).

One important caveat to note is that when records are inserted in Redshift they will not be automatically sorted
according to the sort keys specified with the tables unless the data are copied in from S3 for the first time.
Historically tables in Redshift would become unsorted over time as new records were inserted unless someone went in
and ran a vacuum sort operation on those tables from time to time. This operation deletes any records marked for
deletion and physically sorts the data according to a table's sort key. However, in 2019 `auto vacuum sort  <https://aws.amazon.com/about-aws/whats-new/2019/11/amazon-redshift-introduces-automatic-table-sort-alternative-vacuum-sort/>`_
introduced which sorts data behind the scenes periodically so it's not much of an issue anymore. It's still good
practice to ensure that 1) tables are indeed sorted by querying `SVV_TABLE_INFO  <https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_TABLE_INFO.html>`_
and 2) that there is enough disk space on the Redshift cluster to actually perform the sorting, which requires
additional temporary space for intermediate results.

Optimizing Query Filters
########################
You'll often hear that you should filter on the sort keys of a Redshift table. Hopefully with the overview on zone maps
above you can see why. If you filter on the sort keys and the data are actually sorted on disk, queries can be sped up
significantly just because Redshift avoids reading unnecessary data from disk.

Choosing the right sort keys is *key* here.

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