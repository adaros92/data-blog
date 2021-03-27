***********************
Scala Spark Hello World
***********************

:date: 2021-03-27 00:00
:modified: 2021-03-27 00:00
:tags: Data Engineering
:category: Data Engineering
:authors: Adams Rosales
:summary: A basic template for a Scala Spark project using SBT
:header_cover: /static/post15/header.jpg

Motivation
##########
Spark is a hot skill these days! There are so many tutorials out there on it but I find that most of them miss the mark
on how you actually get started with a Spark project from scratch. Unless you've worked in a professional environment
with Spark pipelines written from scratch it's unlikely that you've been introduced to how to properly structure
a project, set up build dependencies, and write unit tests. In this post I go through a bare-bones SBT template as an
example of how to do just that.

I'm assuming you already have Scala, SBT, and Apache Spark installed. If not, you can follow `the scala docs  <https://docs.scala-lang.org/getting-started/sbt-track/getting-started-with-scala-and-sbt-on-the-command-line.html>`_
to install SBT and Scala and `this from freecodecamp  <https://www.freecodecamp.org/news/installing-scala-and-apache-spark-on-mac-os-837ae57d283f/>`_ to
install Spark.

Create SBT Project
##################
We start by creating an empty directory, changing to it, and creating a hello world SBT project.

.. code-block:: bash

    > mkdir scala-spark-hello-world
    > cd scala-spark-hello-world
    > sbt new scala/hello-world.g8

This creates the following directory structure in the scala-spark-hello-world directory.

.. image:: /static/post15/post15_step1.png
  :width: 100%
  :alt: Step 1 in creating a Spark Hello World project

We don't need the top level project or target directories so let's just delete them and cd into cala-spark-hello-world.

.. code-block:: bash

    > rm -rf project target
    > cd cala-spark-hello-world

In cala-spark-hellow-world we are left with this structure.

.. image:: /static/post15/post15_step2.png
  :width: 100%
  :alt: Step 2 in creating a Spark Hello World project

Add Dependencies
################
The dependencies are specified in the build.sbt file. Spark needs to be listed as a dependency along with a compatible
Scala version to use according to the Spark version you choose. Here I'm using Spark 3.0.1, which requires Scala 2.12.
I'm also adding some additional dependencies like Scalactic and ScalaTest for unit testing and scopt for command line
parsing. We can also specify the assembly merge strategy for handling deduplication when building an uber/fat jar with
all of our dependencies.

We can go ahead and delete the existing build.sbt file and replace it with the code snippet below.

.. code-block:: scala

    scalaVersion := "2.12.1"

    name := "spark-hello-world"
    organization := "ch.epfl.scala"
    version := "1.0"

    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % "3.0.1",
      "org.apache.spark" %% "spark-sql" % "3.0.1"
    )
    libraryDependencies += "com.github.scopt" % "scopt_native0.2_2.11" % "3.6.0"
    libraryDependencies += "org.scalactic" %% "scalactic" % "3.2.5"
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.5" % "test"

    assemblyMergeStrategy in assembly := {
      case "reference.conf" => MergeStrategy.concat
      case "application.conf" => MergeStrategy.concat
      case PathList("META-INF", xs @ _*) => MergeStrategy.discard
      case _ => MergeStrategy.first
    }

Next we have to add the `assembly plugin  <https://github.com/sbt/sbt-assembly>`_ within the project directory in a
plugins.sbt file.

.. code-block:: bash

    > cd project
    > touch plugins.sbt

Here is the one line to add to this plugins.sbt file.

.. code-block:: scala

    addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "0.15.0")

Edit src Packages
#################
Now we're ready to start implementing the Spark logic. To do so let's reorganize the existing project a bit by creating
packages that will contain different components of our code and associated test packages for unit testing later on.

.. code-block:: bash

    > cd src
    # Create test directory
    > mkdir test
    # Create scala directory to mirror main
    > mkdir test/scala
    # Remove existing Main file that's not needed
    > rm main/scala/Main.scala
    # Create common package main and test directories
    > mkdir main/scala/common test/scala/common
    # Create apps package in main and test directories
    > mkdir main/scala/apps test/scala/apps

After all of that, the src directory will look like this.

.. image:: /static/post15/post15_step3.png
  :width: 100%
  :alt: Step 3 in creating a Spark Hello World project

The common package will hold components that are common across all of the codebase and the apps package will just hold
our simple Spark applications for now. This is just a bare-bones structure that can be edited to fit your use case.

Add Spark Session Wrappers
##########################
When working with Spark you'll typically interact with the Spark session and context objects. Instead of instantiating
a bunch of these in different parts of the code base, you can define a single Spark session to be used across your
code. The way to do that naturally with Scala is with a trait that can be extended by objects and classes. Let's put
this wrapper in the common package.

.. code-block:: scala

    package common

    import org.apache.spark.sql.SparkSession
    import org.apache.spark.{SparkConf, SparkContext}

    trait SparkWrapper {

      // Set config
      protected val sparkConf: SparkConf = new SparkConf()
      protected def config(key: String, value: String): Unit = {
        this.sparkConf.set(key, value)
      }
      def conf: SparkConf = this.sparkConf

      def appName: String

      // Build the spark session and retrieve spark context
      protected def builder: SparkSession.Builder = {
        SparkSession
          .builder()
          .appName(appName)
          .config(this.conf)
      }
      def spark: SparkSession = builder.getOrCreate()
      def sc: SparkContext = spark.sparkContext

    }

    trait SparkLocalWrapper extends SparkWrapper{
      override def builder: SparkSession.Builder = {
        super.builder.master("local")
      }
    }

The components that extend these SparkWrapper and SparkLocalWrapper traits will be able to use the single session (spark)
and context (sc) instances instead of defining their own. It also allows us to set the common configuration settings in
one place in the code base, which is generally good practice.

Notice also how we have two traits - SparkWrapper and SparkLocalWrapper. The former is meant to be used in cluster mode
when the application is run on something like EMR or a Hadoop cluster. The latter is used when running Spark on a local
machine like your computer. If you try to run the former on your computer you will typically run into an exception that
a host is not provided or something like that.

We will want to use the SparkLocalWrapper while running unit tests on our local machines. We will also want to turn off
some Spark logs and add some additional configurations so that Spark knows which local host/port to use and to only use
one partition. A good way to do this is with an additional wrapper in the test directory called SparkTestWrapper, which
extends from the SparkLocalWrapper available in main/scala/common.

.. code-block:: scala

    package testutils

    import common.SparkLocalWrapper

    import org.apache.log4j.Level
    import org.apache.spark.SparkConf

    object SparkTestWrapper extends SparkLocalWrapper {
      {
        org.apache.log4j.Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
        org.apache.log4j.Logger.getLogger("org.apache.hadoop.input.LineRecordReader").setLevel(Level.ERROR)
        org.apache.log4j.Logger.getLogger(
          "org.apache.hadoop.mapreduce.lib.output.FileOutputCommitter").setLevel(Level.ERROR)
        org.apache.log4j.Logger.getLogger("org.apache.hadoop.output.FileOutputCommitter").setLevel(Level.ERROR)
        org.apache.log4j.Logger.getLogger(
          "org.apache.hadoop.mapreduce.lib.input.LineRecordReader").setLevel(Level.ERROR)
      }

      override def appName: String = "SparkTestWrapper"

      override def conf: SparkConf = {
        config("spark.sql.shuffle.partitions", "1")
        config("spark.ui.enabled", "false")
        config("spark.driver.bindAddress", "127.0.0.1")
        config("spark.driver.host", "localhost")
        config("spark.sql.catalogImplementation", "in-memory")
        config("spark.driver.port", "8888")
        config("spark.sql.autoBroadcastJoinThreshold", "-1")
        super.conf
      }
    }

I have placed this in a separate test package called testutils (test/scala/testutils). The updated file tree looks like
this.

.. image:: /static/post15/post15_step4.png
  :width: 100%
  :alt: Step 4 in creating a Spark Hello World project

Add Spark Applications
######################
To add a Spark application we can create a new entry point in the apps package. Below is just a simple application to
count the words in a given block of text. It just parses the text using the scopt library and calls the countWords method
on it to perform the word counting. Notice how it extends the SparkWrapper from the common package and overrides the
appName. The spark object referenced here is defined in the SparkWrapper.

.. code-block:: scala

    package apps

    import common.SparkWrapper
    import org.apache.spark.rdd.RDD

    object SparkWordCount extends SparkWrapper {

      override def appName = "Spark Word Count"

      case class CliArgs(textToCount: String = "")

      def parseCli(args: Seq[String]): CliArgs = {
        val parser = new scopt.OptionParser[CliArgs]("SparkWordCountApp") {
          head("Spark word count app")
          opt[String]("textToCount")
            .required()
            .text("The text to count words with")
            .action((param, args) => args.copy(textToCount = param))
        }
        parser.parse(args, CliArgs()).getOrElse({
          parser.showUsage
          throw new Exception("could not parse command")
        })
      }

      /**
       * Calculates the count of unique words in a collection of strings
       * @param text a sequence of individual strings to count words from
       * @return an RDD of word to count tuples
       */
      def countWords(text: Seq[String]): RDD[(String, Int)] = {
        val lines = spark.sparkContext.parallelize(text)
        lines.flatMap(line => line.split(" ")).map(word => (word, 1))
          .reduceByKey(_ + _)
      }

      def main(args: Array[String]): Unit = {
        val cliArgs = parseCli(args)
        val textToCount = cliArgs.textToCount.split(",").toSeq

        val counts = countWords(textToCount)
        counts.foreach(println)
      }
    }

Add Unit Tests
##############
To run unit tests on our Spark applications we can use the ScalaTest library. We'll just create corresponding files
in the test directory with the same name as the classes/objects defined in the main directory but suffixed with the word "Test."
Below is a sample unit test for the countWords method in the SparkWordCount object defined above.

.. code-block:: scala

    package apps

    import org.scalatest.funsuite.AnyFunSuite
    import org.apache.spark.sql.SparkSession

    import testutils.SparkTestWrapper

    class SparkWordCountTest extends AnyFunSuite {

      implicit val spark: SparkSession = SparkTestWrapper.spark

      test("testing that countWords can correctly generate a count of words from a block of text"){
        val wordsToCount = Seq("some words to count", "some other words to count")
        val countsOne = SparkWordCount.countWords(wordsToCount)
        val expectedCount = Set(("some",2), ("words",2), ("count",2), ("other",1), ("to",2))
        assert(countsOne.collect().toSet == expectedCount)
      }

    }

The final tree from the root project directory looks like this.

.. image:: /static/post15/post15_step5.png
  :width: 100%
  :alt: Step 5 in creating a Spark Hello World project

Build It
########
To build our project we can simply run the SBT assembly process with the following command.

.. code-block:: bash

    > sbt assembly

This should download the required dependencies, compile your code, and package all the necessary files into a fat or uber
jar that can be executed on your cluster of choice. This should also run your tests, which you will see in the terminal
as shown below.

.. image:: /static/post15/post15_step6.png
  :width: 100%
  :alt: Step 6 in creating a Spark Hello World project

Run It!
#######
To run your application you first need to find the uber jar created by sbt assembly. After running sbt assembly, you will
notice that a target directory was created in your root project directory. Travel there and into the scala-2.x subdirectory.

.. code-block:: bash

    > cd target/scala-*

Here you will find an assembly jar as shown in the screenshot below.

.. image:: /static/post15/post15_step7.png
  :width: 100%
  :alt: Step 7 in creating a Spark Hello World project

You can then deploy this jar to wherever your cluster needs it to be. For example, if you're using EMR, you can deploy to
some S3 bucket. Then your spark-submit command can be something like the following. Notice the S3 path, which points to
the bucket I deployed my jar to.

.. code-block:: bash

    spark-submit --deploy-mode cluster --executor-memory 1g --class apps.SparkWordCount
    s3://sparkjarsar/sparkflow-sparkapps-assembly-1.0.jar --textToCount "some words to count"

An example of all of this can be found in my `Github  <https://github.com/adaros92/sparkflow-sparkapps>`_. Happy coding!