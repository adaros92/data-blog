****************
SparkFlow: Intro
****************

:date: 2021-02-28 00:00
:modified: 2021-02-28 00:00
:tags: Data Engineering
:category: Data Engineering
:authors: Adams Rosales
:summary: Building an EMR orchestration and ETL tool for distributed jobs
:header_cover: /static/post13/header.jpg

Motivation
##########
I have been working with Spark jobs on AWS EMR for a few years now and have found myself implementing the same pieces of
code to manage EMR clusters and submit applications on them each time I've switched teams. I have also had the pleasure
(and displeasure) of working with several internal tools that abstract away this process behind custom built UIs.

I've learned what works well and what doesn't work so well with these tools so I figured I would create something that
mixes all the best qualities from them to create a lightweight orchestration tool I can use in the future.

Background
##########
AWS EMR is service that allows users to deploy clusters of EC2 instances to run distributed data processing applications.
You can launch the compute power you need to run these applications when you need it and tear it down when you don't,
which provides a lot more flexibility and is much cheaper for transient workloads than maintaining an always-on on-premise
Hadoop cluster.

Managing clusters and submitting applications on them can be done in three ways: manually through the AWS console,
programmatically through the AWS API with the various SDKs made available by Amazon, and through CloudFormation or a
similar infrastructure as code tool. The manual way is obviously not suited for production pipelines and scaling
infrastructure automatically. Writing scripts to interact with the AWS API is easy enough but requires a lot of boiler
plate code and there are many configs to tweak. Designing something that works generally for different use cases is quite
time consuming. Finally, CloudFormation is more suited for always-on clusters or a fixed fleet that just gets restarted
without any inputs from users or applications.

Unfortunately, there is no open source tool (that I know of) as of the end of 2020 that provides an easy to set up and
use interface for running these EMR workflows. It would be nice if AWS offered a higher level abstraction on top of the
EMR API that would give users a full-featured ETL tool for Spark, Hive, Flink, etc. applications. I guess they sort of
have that with AWS Glue and the new managed AirFlow service but these are not quite there yet as more established ETL
and orchestration tools we've seen in the traditional data warehousing space.

Design
######
The system consists of three main components: the UI, Flask server, and AWS Lambdas that call various AWS API endpoints
to create and manage EMR clusters and steps on those clusters. A high level diagram is below.

.. image:: /static/post13/post13_design.png
  :width: 100%
  :alt: SparkFlow design diagram

The cluster manager Lambda receives input from the Flask server on how many clusters to create along with the types of
clusters and other configurations expected by EMR, launches those clusters, and stores their information in a DynamoDB
table. This Lambda is also tasked with deleting specific clusters by terminating them in EMR and deleting the records
from DynamoDB. When this Lambda is invoked, individual EMRs are created under a logical grouping based on compute
requirements (tiny, small, medium, large, extra large). These are easier to understand groups so the user doesn't have
to worry about the specific instance types and amounts to launch. Additionally, when a Spark application is submitted,
it will be launched within a group of clusters. Any available cluster within that group can pick up the work, which acts
as a simple load-balancing system.

The cluster poller Lambda is tasked with periodically polling the active clusters in EMR and updating their status in
Dynamo. These statuses will contain information about the current state of the cluster (running, launching, terminating, etc.)
as well as how many steps are running or pending on that cluster. It will also record the statuses of those steps so that
the Flask app can show the users the latest status of their jobs.

Finally, the step manager Lambda will just submit job runs of transforms executed by the user through the Flask app. It
will first check the status of clusters within the cluster pool that the transform to be executed is tied to and pick
the cluster that is most available. For now this will be based on having the fewer number of steps, but given that
individual steps may be more taxing than others, the availability metric will have to be improved in the long run.
However, once it does pick a cluster, the Lambda will submit the step and create a record in DynamoDB for the Flask app
to reference.

The user interface will be split into three main sections: Clusters, Transforms, and Job Runs. Users will be able to
create the cluster pools/logical groups mentioned above and delete them from the Clusters page. They will create
transforms or job profiles and assign them to specific pools of clusters in the Transforms page. Finally, the Job Runs
page will just show the status of transform executions. This will look something like the below working version.

.. image:: /static/post13/post13_sparkflow_ui.png
  :width: 100%
  :alt: SparkFlow user interface

Follow Along
############
The repos containing the code for this project are the following.

`sparkflow-awstools <https://github.com/adaros92/sparkflow-awstools/>`_ - contains Python AWS API wrappers using boto3
and logical models for EMR clusters, EMR steps, and Dynamo tables

`sparkflow-backend <https://github.com/adaros92/sparkflow-backend/>`_ - Flask app code defining the server routes and UI

`sparkflow-lambdas <https://github.com/adaros92/sparkflow-lambdas/>`_ - implementation of the cluster manager, cluster
poller, and step manager Lambdas

I'll be updating these repos as I work on the project and posting more detailed write-ups of the various components as
they're built on this page. Stay tuned!

