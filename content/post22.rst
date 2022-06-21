**********************
Boss Scala Spark Moves
**********************

:date: 2022-06-16 19:49
:modified: 2022-06-16 19:49
:tags: Programming
:category: Programming
:authors: Adams Rosales
:summary: Sharing some Spark syntax that will make you love Scala

Functional Heaven
#################
I started writing Spark code in Scala about 2 years ago after working mostly with PySpark before.
I've never looked back! The built-in functional syntax available in Scala pairs really well with
Spark. Below are some quick snippets so you can see what I'm talking about.

It Folds
########
Say you have a list of column names.

.. code-block:: scala

    val someList = Seq("column_a", "column_b", "column_c")

You can use the built in foldLeft method of this collection to apply transformations to a Spark data
frame for each value and keep track of the results. The data frame you get back will be the cumulative
result of all of those transformations. This works great for renaming columns such as in the example below.

.. code-block:: scala

    val renamedDf = someList.foldLeft(df){case(tmpDf, column) =>
        tmpDf.withColumnRenamed(column, s"renamed_$column")
    }

Here the tmpDf data frame will contain the intermediate results from the previous iteration. This will continue until
we traverse the entire collection. The result is that each one of those columns will now be prefixed with
"renamed" in renamedDf.

Reduction Junction
##################
If you have a collection of data frames instead, you can easily combine them with the reduce method of that collection.

.. code-block:: scala

    val dfs = Seq(df1, df2, df3, df4, df5)

One handy reduction here is simply unioning these data frames together into one.

.. code-block:: scala

    val combinedDf = dfs.reduce(_ union _)

As long as all of these data frames have the same columns, the result will be a single data frame containing the union of
all of them.

Variable Argument Sequences
###########################
You can pass collections of objects to data frame methods with the _* operator in Scala. Say you have some columns you
want to alias and select.

.. code-block:: scala

    val columns = Seq("column_a", "column_b", "column_c")
    val aliases = columns.map(columnName => {
        col(columnName).alias(s"alias_of_$columnName")
    })

You can pass this list of aliases to the select method as follows.

.. code-block:: scala

    val selectDf = df.select(aliases:_*)

You can also use this for other methods like groupBy and agg.

.. code-block:: scala

    val groupByColumns = Seq("partition_a", "partition_b")
    val measureColumns = Seq("measure_a", "measure_b", "measure_c")
    val maxOfMeasures = measureColumns.map(max)

    val resultDf = df
        .groupBy(groupByColumns.head, groupByColumns.tail:_*)
        .agg(maxOfMeasures.head, maxOfMeasures.tail:_*)

The result here is that we group by the group by columns and take the max of all the measures.

Case Class Schemas
##################
You can use collections of case classes to model records in a data frame. The case class defines the schema of the data
and each instance is a record. Take the following schema as an example

.. code-block:: scala

    case class Employee(
        id: Long,
        name: String,
        department: String
    )

Let's define a collection of employee records using this case class.

.. code-block:: scala

    val employees = Seq(
        Employee(1, "John Smith", "Finance"),
        Employee(2, "Pocahontas", "Engineering")
    )

Now we can easily create a data frame from this data.

.. code-block:: scala

    import spark.implicits._
    val df = employees.toDF

The data frame will have a bigint/long column for id, a string name column, and a string department
column with the 2 employee records.

Monkey Patching Spark
#####################
With the use of implicit classes, you can even add your own functionality to Spark data frames. This allows you to
extend them beyond the set of methods built-in natively, which can be pretty useful to cut down repetitive boiler
plate code if used with caution. I've written about this in detail before here:
`Modularizing and Chaining Scala Spark Transformations <https://decipheringbigdata.com/modularizing-and-chaining-scala-spark-transformations.html>`_