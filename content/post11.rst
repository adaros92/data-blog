*****************************
MySQL, YourSQL, OurSQL, NoSQL
*****************************

:date: 2021-01-17 00:00
:modified: 2021-01-17 00:00
:tags: Data Engineering
:category: Data Engineering
:authors: Adams Rosales
:summary: One node, two node, Redshift, Blueshift
:header_cover: /static/post11/header.jpg

What Does It All Mean?
######################
Learning about data storage solutions can be a daunting processing. There are so many technologies out there that
it's hard to keep track of everything. Behind all the buzzwords and branding though, the concepts underpinning these
technologies are actually quite easy to grasp. They can help us choose which databases to use for different problems and
really just make us better members of society. So be awesome, know your databases!

OLTP or OLAP
############
Online Transactional Processing and Online Analytical Processing are the two broad categories of data storage systems. Do
you need a database to handle lightning quick atomic transactions (OLTP) to support the systems powering your application
or do you want to answer complex business questions from your data (OLAP)? Answering this question is the quickest way
to narrow down the list to the right family of technologies, but it's surprisingly easy to get wrong.

OLTP queries typically involve entire collections of data around a certain subject. When data are stored and retrieved,
entire records need to be inserted or selected from the database. The queries don't typically need to do anything complex
beyond just recording data and retrieving information to serve up to the application and there is minimal joining and
aggregating of individual records. Because OLTP systems often impact the customer experience these insertion/retrieval
processes need to be as quick as possible (no one likes a slow website or app).

OLAP queries on the other hand are more for like that time that your boss asked you to get all of the orders that
were split into multiple boxes and contained at least one red item weighing 5 lbs or more. You know, oddly specific and
complex questions like that to support a statement in a doc or to be included in the 10th appendix page of next
week's business review meeting. These are the queries that populate all of the business reports and cutting edge analytics
to inform strategic decisions, budgeting, and big brain stuff like that. They don't need to be particularly quick and
it doesn't really matter much if the result is a bit off (unlike say displaying someone's account balance to them in an OLTP
system).

Below I've listed some of the popular OLTP and OLAP technologies.

.. image:: /static/post11/post11_olapoltp.png
  :width: 100%
  :alt: A list of OLTP and OLAP technologies

Of course it's not so black and white in the real world. Just like you could technically row a boat with a spatula, you
could also execute that complex analytical query on highly normalized tables in MySQL that takes 4 hours to run. But, yes
there's probably a better way of storing the data to support queries like that.

ACID or BASE
############
Another important factor to take into consideration is whether the system is ACID or BASE compliant. ACID stands for:

- **Atomicity**: transactions either do all of the work they're meant to or nothing at all
- **Consistency**: all tables in the system contain the same view of the data as it was committed by a transaction
- **Isolation**: concurrent transactions run independently of each other
- **Durability**: the data committed by transactions will remain in the database even after system failures

BASE on the other hand stands for:

- **Basically available**: the system will do its best to return data most of the time but the data may not be consistent
- **Soft state**: the state of the system may not be final because of the lack of a strong consistency model
- **Eventual consistency**: the system will eventually be consistent after any inputs but until then, reads may not
  receive the latest state available

A bank will want to ensure that when a user withdraws money, either both the user receives the money and the account is
debited for the change or neither of the two occur. There cannot be cases where the user receives money that still appears
in their account after the withdrawal. For these types applications companies will need to stick with ACID compliant
relational databases like MySQL, PostgreSQL, SQL Server, etc.

A profile page on a web application however does not need such a strict atomicity and consistency guarantee. Sections of
the page may be retrieved out of order and updates made by the user to their profile may be eventually consistent because
it's more important to guarantee super quick retrieval of data to ensure a smooth user experience. It may also be more
important to scale out horizontally with cheap commodity hardware and be able to handle larger volumes of data. BASE
systems like MongoDB, DynamoDB, Redis, Cassandra, Hbase, CouchDB, etc. are all great for these types of applications but
it would be risky to use them to support financial transactions.

SQL or NoSQL
############
NoSQL refers to a wide array of different data storage solutions that deviate away from the traditional relational database
model. The schemas in these systems are a lot more flexible than their relational counterparts and insertion/reads tend to
be faster as long as you query them using specific known keys corresponding to the records you want.

- **Document stores**: store data in schema-less objects that look a lot like JSON or XML. You can pretty much store your
  data however you want and individual records in any one table can have their own schemas independent of other records in
  the table.
- **Graph stores**: store data in graph-like objects consisting of nodes and relationship between those nodes. They excel
  at providing efficient lookups of how objects are related to each other, which is why they're great for social networking
  applications.
- **Key-value stores**: store data in the same way as hash tables where you have keys and values tied to those keys. These
  provide exceptional lookup and writing speed as long as you're searching for specific keys. Many document and key-value
  stores are quite similar in that records are identified by particular keys so they offer similar performance relative to
  relational databases but key-value stores are typically more optimized for fast reads and updates of single key-value pairs
  than document stores. This makes them great for caching.

Cold or Hot
###########
The temperature metaphor in this context is more relevant to OLAP systems. It refers to how frequently the data need to
be accessed. Nowadays you can store petabytes of data in a system like HDFS and S3 quite cheaply. However, storing that
amount of data in data warehouse clusters like Redshift, Vertica, or BigQuery would be a lot more expensive but much
faster to retrieve because the data would be more readily accessible. So in the context of a temperature spectrum we say
that efficient columnar data warehousing solutions like Redshift are hotter than object stores like S3/HDFS.

This is an important dimension to think about when you're choosing where to store each data. There is no use in taking up
valuable cluster space with logs that are not important to consumers of the data but may be important one day for audit
purposes or what have you. These logs should be stored in a cold location that will be a lot cheaper but provide
expensive and slower retrievals of the data when you do need it. On the other hand you should ensure that data accessed
every day is modeled and stored behind enough computing power to enable efficient access to it. You do not want important
business reports to be delayed because it's taking a long time to process all of that unstructured data somewhere in HDFS
or S3 (this not much of a problem today with all of the flexible compute options we have available but it's still a useful
framework to keep in mind).

So How Do You Choose?
#####################
Follow the flow chart below as a general guide.

.. image:: /static/post11/post11_flowchart.jpeg
  :width: 100%
  :alt: A flowchart of different data store technologies
