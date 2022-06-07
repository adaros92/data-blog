*********
I See You
*********

:date: 2020-12-19 00:00
:modified: 2020-12-19 00:00
:tags: Programming
:category: Programming
:authors: Adams Rosales
:summary: The Observer design pattern
:header_cover: /static/post8/header.jpg

Overview
########
The Observer software design pattern is a commonly used approach for decoupling subjects/events from observers of the
subjects. The class diagram can be expressed like so:

.. image:: /static/post8/post8_observer_ulm.jpg
  :width: 100%
  :alt: Observer design patter ULM

There is one independent subject class which is coupled with an abstract observer class by way of an update method the
subject calls when it needs to broadcast updates to all of its registered observers. Concrete observers that
depend on the one subject implement this update method, which will typically pull the state they need from the subject
and carry out their work based on changes in that state.

When concrete objects are instantiated, they register themselves to the subject they need to observe via the subject's
public register method. This will let the subject know to add the observer to its list of observers that need to be
notified when the subject's state changes.

Applications
############
Most publisher/subscriber relationships you've come across can be modeled with the observer design pattern.

- A YouTube channel uploads a new video and the service updates all of that channel's subscribers
- New data becomes available in a table and downstream jobs that depend on the table are notified of the data being
  available
- A metrics aggregator collects a bunch of stats about a running system and notifies attached alarm objects about when
  new data is available; the "alarmers" check their respective metrics and send out an alarm if the metrics pass some
  threshold
- E-bay's bidding mechanism broadcasts the highest bid and whether the item has sold yet to all the watchers of an
  item
- A social media post sends out notifications of new activity on the post to people who have left a reaction and/or
  commented

Example Implementation
######################
As shown in the diagram above, the subject has an attach/register method that observers can call to register themselves
as active observers of the subject. When this happens below, the subject will just add the observer object to a set of
unique observers that need to be notified.

The notification happens with the _notify method. This just iterates over each observer in the collection of registered
observers and calls each one's update method. That's the only coupling of logic between the subject and its observers.

Finally, the run method just keeps generating random integers from 0 to 100 and appending them to a list. The observers
are notified as soon as a new number is appended. If the randomly generated integer is equal to 50 then the subject stops
updating.

.. code-block:: python

    import random


    class Subject(object):
    """The mutable subject that's being observed

    @param name - the name of the subject
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.observers = set()
        self.data = []

    def attach(self, observer) -> None:
        """Adds the given observer to a set of unique observers that are interested in some
        aspect of this subject's state

        :param observer - an observer object that will want to be notified of changes in state
        """
        self.observers.add(observer)

    def _notify(self) -> None:
        """Notifies every observer that something about the subject state has changed"""
        for observer in self.observers:
            observer.update()

    def run(self) -> None:
        """Run some business logic or process that updates the subject's state"""
        while True:
            random_int = random.randint(0, 100)
            self.data.append(random_int)
            self._notify()
            if random_int == 50:
                break

Now I implement one abstract observer that defines the interface between all observers and two concrete observers. The
LengthObserver object just reports the length of the subject's data each time it's notified. The ValueObserver object
will report if it finds that a new even number in the range of 0 to 98 has been added to the subject's data.

.. code-block:: python

    from abc import ABC, abstractmethod


    class Observer(ABC):
        """An abstract observer class defining the common interface that all observers share

        @param subject_to_observe - the subject the observer is interested in
        @param name - the name of the observer
        """

        def __init__(self, subject_to_observe: Subject, name: str):
            self.name = name
            self.subject = subject_to_observe
            self.subject_name = self.subject.name
            self.subject.attach(self)

        @abstractmethod
        def update(self):
            """Defines what to do when the observer receives an update from the subject"""
            pass


    class LengthObserver(Observer):
        """Checks for the length of the subject's data and reacts accordingly

        @param subject_to_observe - the subject the observer is interested in
        @param name - the name of the observer
        """

        def __init__(self, subject_to_observe, name="LengthObserver"):
            super().__init__(subject_to_observe, name)

        def update(self):
            """Emits an alert about the subject data length"""
            subject_data = self.subject.data
            subject_data_length = len(subject_data)
            print("Observer {0} noticed that {1}'s data contains {2} elements".format(
                self.name, self.subject_name, subject_data_length
            ))


    class ValueObserver(Observer):
        """Checks that certain values are present in the subject it's observing

        @param subject_to_observe - the subject the observer is interested in
        @param name - the name of the observer
        """

        def __init__(self, subject_to_observe, name="ValueObserver"):
            super().__init__(subject_to_observe, name)
            self.values_to_check = [x for x in range(100) if x % 2 == 0]
            self.values_seen = set()

        def update(self):
            """Emits whether it finds certain values in the subject's data and keeps track of values
            already seen"""
            subject_data = self.subject.data
            for value_to_check in self.values_to_check:
                if value_to_check in subject_data and value_to_check not in self.values_seen:
                    self.values_seen.add(value_to_check)
                    print("Observer {0} noticed that {1}'s data contains value {2}".format(
                        self.name, self.subject_name, value_to_check
                    ))

Running this below we can see the different observers doing their thing based on the subject's changes in state.

.. code-block:: python

    if __name__ == "__main__":
        subject = Subject("SomeSubject")
        length_observer = LengthObserver(subject)
        value_observer = ValueObserver(subject)
        subject.attach(length_observer)
        subject.attach(value_observer)
        subject.run()

.. image:: /static/post8/post8_observer_example_run.jpg
  :width: 60%
  :alt: Observer design patter ULM
