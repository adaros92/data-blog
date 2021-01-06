*****************************
The Role of the Data Engineer
*****************************

:date: 2021-01-03 00:00
:modified: 2021-01-03 00:00
:tags: Career
:category: Career
:authors: Adams Rosales
:summary: Data engineers should do more than just build and maintain ETL jobs
:header_cover: /static/post10/header.jpg

What Data Engineers Actually Do
###############################
The textbook definition of a data engineer is a person who builds pipelines that prepares data for scientists to consume.
This is true to some extent but in the real world, the role varies widely.

From my experience, the data engineering crowd is composed of the following members.

- Old school BI/ETL engineers
- Younger professionals who sought out the role lured by the shiny big data frameworks and DS hype
- Seasoned software engineers who chose to specialize in big data (or were tasked with a problem and had no other choice)

Just like the crowd, the roles are mixed as well.

- Traditional data warehousing with drag and drop ETL tools like Informatica
- Writing SQL queries to extract data from a data warehouse
- Building custom ETL orchestration with programmatic frameworks like Airflow in languages like Python/Java/Scala
- Big data processing and storage using Spark/MapReduce with languages like Python/Java/Scala on cloud technologies/on-prem Hadoop clusters
- Building scalable data processing systems and infrastructure to automate the above and/or enable self-service access to data

What you end up doing largely depends on the team you're on and what the needs are. However, I think we can all agree
on which roles are the most interesting to engineers if engineers are what companies actually want when they hire DEs.

Moving Data From Point A to B Is Not Fun
########################################
If you think the textbook definition of a data engineer sounds boring it's because it is. People don't go into data
engineering because they like to set up an ETL to join a few tables, aggregate some columns, and spit the result out to
the analysts. Certainly not good engineers anyway.

Yet the expectation from most of my customers assumes that we enjoy building ETLs and solely exist to hand over the
precious data upon request. This is a silly expectation for a few reasons.

1. If you can get a Master's or PhD in Math/Econ/Stats/whatever and be a fancy data scientist you can also write SQL
2. Given that the process of transforming data is tedious, it will never be the end goal for talented engineers and they will most likely get bored and leave
3. Enforcing a contract where data engineers provide and data scientists receive sets up the system so that no one is building anything end-to-end, which is not rewarding to anyone involved
4. Enforcing this contract also leads to increased latency from scientists sitting around waiting for data engineers to prioritize their work

Data Engineers Should Focus on the Infra
########################################
Instead of building and maintaining the ETL, engineers should instead focus on enabling self-service and building sound infrastructure. There
is no reason why scientists can't structure and pull their own data. They should be empowered to own the entire analytics
process end-to-end and engineers should be given the time to make this as easy and fool-proof as possible.

This means cataloguing the data, building automatic alarming and outlier detection systems, optimizing bottleneck pipelines,
improving data quality, enforcing data governance processes, building self-service tools to remove friction, and implementing
complex data pipelines that require more than just SQL.

Unless the data is in a super raw format or needs to be processed with very little latency, specialized knowledge in
data processing and modeling is not required. The tools exist so that data does not really need to be structured in a data warehouse
to be useful to analysts. If you want to query those JSON logs in S3 you can. The same is true for denormalized parquet files or
raw CSVs. Data engineers should build the right abstractions that leverage these tools and make new ones available instead of
being stuck maintaining a bunch of ETL jobs that the scientists can own themselves.

The Future of the Role
######################
With third-party ETL tools becoming more sophisticated and cloud computing providers making more automation and data discovery
services available, data engineers will be taking on more engineering and infrastructure heavy roles. The role of a data engineer
should be seen as another branch of software engineering requiring the same fundamental way of thinking. They will need to
adopt the same software and system design practices as software engineers but use them to build scalable and intuitive
data infrastructures.