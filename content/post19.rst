*******************************
Creating a Gradle Scala Project 
*******************************

:date: 2022-05-21 19:15
:modified: 2022-05-21 19:15
:tags: Programming
:category: Programming
:authors: Adams Rosales
:summary: Setting up a Scala project with the Gradle build tool

Why Gradle?
###########
There are three main build tools out there for Scala projects: SBT, Maven, and Gradle. SBT is typically preferred when you're starting out with Scala and your project will purely be Scala based. I find that it's the most documented when learning how to write Scala online and has the most build plugins contributed by the Scala community. On the other hand, I haven't come across SBT-backed projects in the professional world. They tend to use either Maven or Gradle. I'm not quite sure why this is the case but my hunch is that these build tools play better with other JVM languages like Java, which is still a lot more popular than Scala at most companies, and most of the developers working on Scala codebases come from Java backgrounds. They started out building their projects with Maven or Gradle and since they're familiar with those tools, that's just what ends up being used. Then between Maven and Gradle, the latter is typically faster and offers a simpler way to control dependencies in your project than the XML-based format of Maven. 

There's no shortage of opinions on what's best online! Whatever the reasons why people choose the build tools they do, I think it's important to be familiar with what's used most in the industry so here is an easy guide on how to get started! 

Install Prerequsites
####################
The first thing you want to do is have an IDE, Scala, and Gradle installed. I recommend using the `Intellij <https://www.jetbrains.com/idea/download/#section=mac>`_ Community edition IDE. It will handle a lot of things for you and ensure a smoother development experience when working on the JVM. 

To install Scala simply follow the instructions `on their site <https://www.scala-lang.org/download/>`_ and Gradle `here <https://gradle.org/install/>`_. If you have a Mac, you can use Homebrew to install these pretty easily

.. code-block:: bash

    brew install gradle

You will also want to enable Scala support on Intellij by following `these <https://www.jetbrains.com/help/idea/discover-intellij-idea-for-scala.html#UserInterface>`_ directions. 

Create Scala Project on Intellij
################################
Once you have everything installed, you should be able to create a project on Intellij by selecting a Scala new project using IDEA like so.

.. image:: /static/post19/post19_1.png
  :width: 100%
  :alt: Intellij new project setup

.. image:: /static/post19/post19_2.png
  :width: 100%
  :alt: Intellij new project setup

Name it whatever you want and choose the lestest Java JDK on your system. 

.. image:: /static/post19/post19_3.png
  :width: 100%
  :alt: Intellij new project setup

Initialize the Gradle Project
#############################
Once you have your Intellij Scala project created all you need to do to pair it with Gradle is run the Gradle init command in your terminal. 

In Intellij, click on Terminal at the bottom of your IDE and run the following. Choose Groovy as the build script DSL.

.. code-block:: bash

    gradle init --type scala-library

This should create all of the necessary artifacts you need to use Gradle with your Scala project. 

.. image:: /static/post19/post19_4.png
  :width: 100%
  :alt: Gradle initialization

You can then get a list of available tasks by running:

.. code-block:: bash

    ./gradlew tasks

If you want to run your tests for example, you can run:

.. code-block:: bash

    ./gradlew test


Adding Dependencies
###################
To add dependencies to your project, you simply have to edit the build.gradle file inside of your lib folder. 

.. image:: /static/post19/post19_5.png
  :width: 50%
  :alt: Gradle dependencies

Typically, Maven is the default repository used to install dependencies with Gradle (this can be specified in build.gradle using the repositories struct). You can find all of the available artifacts `on the Maven Repository site <https://mvnrepository.com/>`_.

Clicking on any artifact on Maven will reveal the different ways to add it to your project. 

.. image:: /static/post19/post19_6.png
  :width: 100%
  :alt: Maven repositories

So to add a dependency, we just need to copy the Gradle (Short) specification here and add it to our build.gradle file. Once you do, Intellij should show a little elephant pop-up that you can then click on to update your project with that dependency. It should then not scream at you when you reference the respective libraries in your code.

.. image:: /static/post19/post19_7.png
  :width: 100%
  :alt: Maven repositories

Of course, it is A LOT more complicated than that. It's super overwhelming, but I recommend reading through the official `Gradle dependency documentation <https://docs.gradle.org/current/userguide/dependency_management.html>`_ to really understand how dependency management works. 