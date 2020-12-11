******************
Python Parallelism
******************

:date: 2020-12-10 00:00
:modified: 2020-12-10 00:00
:tags: Python
:category: Python
:authors: Adams Rosales
:summary: Parallel processing with Python...or lack thereof?
:header_cover: /static/post3/header.jpg

Something About the GIL
#######################
The global interpreter lock. A mutex on Python objects that prevents multiple threads from executing at the same time.
Python is single-threaded. The end, right?

Yes and no. It's a bit more complicated than that. The real answer is that you can get some pretty sweet parallelism
going if you know which libraries to use.

The Threading Library
#####################
The first tool you should be aware of is the beautifully simple threading library. Say you have a function like the one
below:

.. code-block:: python

    def find_max(list):
        import time
        max_num = None
        for idx, elm in enumerate(list):
            if idx == 0:
                max_num = elm
            elif elm > max_num:
                max_num = elm
        time.sleep(10)
        print(max_num)
        return max_num

This finds the max element in a list of numbers but there is a delay of 10 seconds where the processor is simply waiting
for this function to finish and nothing is really being done. Let's run this function in separate threads and see how it
performs.

.. code-block:: python

    import random
    import time

    from datetime import datetime
    from threading import Thread

    def find_max(list):
        max_num = None
        for idx, elm in enumerate(list):
            if idx == 0:
                max_num = elm
            elif elm > max_num:
                max_num = elm
        print(max_num)
        time.sleep(10)
        return max_num

    def start_threads(threads):
        for thread in threads:
            thread.start()

    def wait_for_threads(threads):
        for thread in threads:
            thread.join()

    if __name__ == "__main__":
        # Create 10 lists of 10 random numbers
        list_count = 10
        lists = [[random.randint(-100, 100) for _ in range(list_count)]
            for x in range(list_count)]
        # Process each list in a separate thread
        threads = [Thread(target=find_max, args=(list,)) for list in lists]
        # Print time before execution
        print(datetime.now())
        # Start the threads and wait for them to finish
        start_threads(threads)
        wait_for_threads(threads)
        # Print the time after execution
        print(datetime.now())

If you run this you'll see that the individual threads appear to run in parallel since all of the max values are
printed almost at the same time. Also, the amount of time that elapses from the start of the program to its end is
only slightly more than the 10 seconds the find_max function waits for before returning.

.. image:: /static/post3/post3_threading.jpg
  :width: 80%
  :alt: Running threading function results in parallel execution when process is I/O bound

However, this is not actually the case. Because of the GIL, there's really just one thread running! The magic though is
that the thread is able to switch between function executions when one is stuck waiting for an I/O bound process to
finish.

In this case the first function execution is kicked off and immediately goes into the time.sleep(10). While it's waiting,
the CPU doesn't just sit around but runs the function for the second execution, which also waits for 10 seconds,
and so on until the 10 lists are processed in the 10 separate "threads" almost simultaneously.

This functionality really shines when your process is stuck waiting for a response from a server, reading/writing a file
to disk, etc. Anything that is I/O bound where the CPU is not doing anything but just waiting. On the other hand, when
your CPU is doing intensive computations, the threading module is pretty much useless and can actually slow your program
down.

The Multiprocessing Library
###########################
This library couldn't care less about the GIL. It just doesn't need to. What it does instead is execute your program in
separate Python interpreters within the same machine. The separate processes spawned will not share any memory space
or resources.

The obvious drawback to this is the overhead with having multiple Python interpreters and separate memory spaces. That
said though, it provides an actual method to achieve true parallelism in Python and speed CPU-bound tasks considerably
on multi-core CPU systems.

To test this out, let's modify our original function to not sleep for 10 seconds and instead we'll just run it on a
large amount of data to simulate a CPU-bound task.

.. code-block:: python

    from datetime import datetime

    def find_max(list):
        max_num = None
        for idx, elm in enumerate(list):
            if idx == 0:
                max_num = elm
            elif elm > max_num:
                max_num = elm
        print(max_num)
        return max_num

    if __name__ == "__main__":
        print(datetime.now())
        my_big_list = [x for x in range(100000000)]
        find_max(my_big_list)
        print(datetime.now())

This takes about 25 seconds to run on my machine.

.. image:: /static/post3/post3_multiprocessing1.jpg
  :width: 80%
  :alt: Single CPU-bound process takes 25 seconds to run

Below we perform the same task three times in separate threads using the threading library.

.. code-block:: python

    def generate_big_list():
            my_big_list = [x for x in range(100000000)]
            find_max(my_big_list)

    if __name__ == "__main__":
        # Run the function in separate threads
        threads = []
        print(datetime.now())
        for idx in range(3):
            threads.append(Thread(target=generate_big_list))
            threads[idx].start()
        for thread in threads:
            thread.join()
        print(datetime.now())

On my machine this took more than a minute to run! This makes sense because we have changed the find_max function to be
a CPU-bound process and threading just doesn't want to be our friend here.

.. image:: /static/post3/post3_multiprocessing2.jpg
  :width: 80%
  :alt: Running threading function results in bad performance when process is CPU-bound

So let's use the multiprocessing library to speed this bad boy up!

.. code-block:: python

    import multiprocessing

    from datetime import datetime

    def find_max(list):
        max_num = None
        for idx, elm in enumerate(list):
            if idx == 0:
                max_num = elm
            elif elm > max_num:
                max_num = elm
        print(max_num)
        return max_num

    def generate_big_list():
        my_big_list = [x for x in range(100000000)]
        find_max(my_big_list)

    if __name__ == "__main__":
        # Run the function in separate processes
        processes = []
        print(datetime.now())
        for idx in range(3):
            processes.append(multiprocessing.Process(target=generate_big_list))
            processes[idx].start()
        for process in processes:
            process.join()
        print(datetime.now())

By using multiprocessing we can run the three executions in 35 seconds, which is only 10 seconds more than the one
execution took to run.

.. image:: /static/post3/post3_multiprocessing3.jpg
  :width: 80%
  :alt: Multiprocessing speeds up CPU-bound processes significantly

As mentioned before, this performance comes at a price...three Python interpreters taking up three times the memory. One
for each process run by the multiprocessing library.

.. image:: /static/post3/post3_multiprocessing4.jpg
  :width: 80%
  :alt: Running multiprocessing takes up a lot of overhead

Are There Other Options?
#########################
Yes, the first option is not using any of these at all and just embracing the additional latency. There is beauty in
simplicity and sometimes an easy-to-follow single-threaded solution is preferable to the more efficient alternative.

The second option to consider is a higher level API that combines threading and multiprocessing in one module.
Concurrent.futures provides a simpler interface but pretty much does the same thing as these two libraries. You can
read more about it `here <https://docs.python.org/3/library/concurrent.futures.html>`_.

Then there's `asyncio <https://docs.python.org/3/library/asyncio.html>`_...that's a completely different beast best left
for a different time.