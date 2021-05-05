*****************************************************
Modularizing and Chaining Scala Spark Transformations
*****************************************************

:date: 2021-05-04 00:00
:modified: 2021-05-04 00:00
:tags: Data Engineering
:category: Data Engineering
:authors: Adams Rosales
:summary: How to use existing Data Frame functionality and extend it to cut down on Spark boiler plate
:header_cover: /static/post17/header.jpg

The Base Approach
#################
When moving beyond a single-file processing script, you may decide to modularize different transforms used in your
Spark application for reuse by multiple jobs. A simple way to do that may be by creating a Transforms singleton
that defines different transformation functions which take a data frame and any other necessary arguments as inputs.
Take the two simple transforms below as an example.

.. code-block:: scala

    package transforms

    import org.apache.spark.sql.DataFrame
    import org.apache.spark.sql.functions.lit


    object Transforms {

      def filterByValue(df: DataFrame, column: String, value: String): DataFrame = {
        df.filter(s"$column = '$value'")
      }

      def appendId(df: DataFrame, column: String, value: String): DataFrame = {
        df.withColumn(column, lit(value))
      }

    }

This is a step in the right direction but it's not the best implementation because it requires explicitly
passing the results of one transformation to the other as seen below. This can lead to a lot of clutter in your code
with transformation chains that can become difficult to follow. They're also defined in such a way that you can only
use them for string values when you may also want to use them with other data types.

.. code-block:: scala

    package jobs

    import transforms.Transforms
    import org.apache.spark.sql.DataFrame

    class Processor {

      def process(df: DataFrame): DataFrame = {
        Transforms.appendId(Transforms.filterByValue(df, "marketplace", "us"),
          "processed_by", "processor")
      }

    }


Generalizing the Base Approach
##############################
So you may take it a step further and generalize these transform utility functions some more by maybe including type
parameters and using functional currying. Separating out the data frame input from the main function itself that needs to be
applied to the data helps split out the transformation from the data the transformation is acting on. This makes the code a
little easier to understand when calling the transformations.

.. code-block:: scala

    package transforms

    import java.util.Date
    import org.apache.spark.sql.DataFrame
    import org.apache.spark.sql.functions.lit


    object Transforms {

      def filterByValue[T](column: String, value: T)(df: DataFrame): DataFrame = {
        val filterExpression = value match {
          case s: String => s"$column = '$value'"
          case d: Date => s"$column = '${value.toString}'"
          case _ => s"$column = $value"
        }
        df.filter(filterExpression)
      }

      def appendId[T](column: String, value: T)(df: DataFrame): DataFrame = {
        df.withColumn(column, lit(value))
      }

    }

As you can see below, the code is a little cleaner. You can clearly tell that you're applying some transformation function
that takes specific arguments from the data to the data provided. However, it still requires you to explicitly pass the
result of one transformation to other, which can lead to long chains of repetitive code and data frame instantiations.

.. code-block:: scala

    package jobs

    import transforms.Transforms
    import org.apache.spark.sql.DataFrame

    class Processor {

      def process(df: DataFrame): DataFrame = {
        val filteredDf = Transforms.filterByValue("marketplace", "us")(df)
        Transforms.appendId("processed_by", "processor")(filteredDf)
      }

    }


Using the Dataframe Transform Method
####################################
It turns out we can avoid passing the results of one transformation to the other and defining multiple instances of
dataframes by passing functions to the dataframe's transform method. This method can be chained to apply multiple
transformations to the original dataframe as seen below. To use this functionality you need to use functional currying
in your transform definitions as shown above.

.. code-block:: scala

    package jobs

    import transforms.Transforms
    import org.apache.spark.sql.DataFrame

    class Processor {

      def process(df: DataFrame): DataFrame = {
        df.transform(Transforms.filterByValue("marketplace", "us"))
          .transform(Transforms.appendId("processed_by", "processor"))
      }

    }

This is the recommended way to chain transformations in Spark and it works pretty well!

Extending the Data Frame Class
##############################
But, you can even get around the transform method by extending the Dataframe class itself with the use of implicit classes.
This is a Scala feature that allows us to add functionality to existing classes without editing the original implementation
of those classes. Used here, this feature allows us to simply chain the names of the transformation methods themselves
without having to pass in a copy of the dataframe to each transformation method and without having to call transform repeatedly
to chain each transformation. Notice below how I've wrapped the transforms within an implicit class declaration that takes
the dataframe as input and wrapped that within an object.

.. code-block:: scala

    package transforms

    import java.util.Date
    import org.apache.spark.sql.DataFrame
    import org.apache.spark.sql.functions.lit


    object Transforms {

      implicit  class Transforms(df: DataFrame) {

        def filterByValue[T](column: String, value: T): DataFrame = {
          val filterExpression = value match {
            case s: String => s"$column = '$value'"
            case d: Date => s"$column = '${value.toString}'"
            case _ => s"$column = $value"
          }
          df.filter(filterExpression)
        }

        def appendId[T](column: String, value: T): DataFrame = {
          df.withColumn(column, lit(value))
        }
      }

    }

To use the implicit transformations, all we have to do is import them into the local scope and they will be immediately
available as methods of all dataframes in that scope.

.. code-block:: scala

    package jobs

    import transforms.Transforms
    import org.apache.spark.sql.DataFrame

    class Processor {

      import Transforms._

      def process(df: DataFrame): DataFrame = {
        df.filterByValue("marketplace", "us")
          .appendId("processed_by", "processor")
      }

    }

While this approach helps us cut down on repetitive code quite a bit, it's not without its flaws. You're adding
functionality to existing classes that is unknown by regular users of those classes who are not aware of your particular
extensions. It may be confusing to other users who may interpret one of your custom methods as native to the Dataframe
class, making it difficult to trace the code's functionality. This approach, commonly referred to as monkey patching, is
also generally frowned upon by the software engineering community because it can add confusing behavior to existing libraries
and even introduce major code incompatibilities and bugs.

However, I think that when used in this context, it can help clarify the code quite a bit by avoiding the long chain
of transform calls and simply cutting down on the total amount of code written. In order to use the implicit transformations
you need to import them and they only really affect the scope into which they're imported so it's not as bad as if you
were to monkey patch the behavior of the Dataframe class in the global scope of your application like developers are used
to in other languages like Ruby.

Happy coding!