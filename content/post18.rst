***********************************
ML Demystified: K Nearest Neighbors
***********************************

:date: 2022-04-25 22:10
:modified: 2022-04-25 22:10
:tags: ML
:category: Machine Learning
:authors: Adams Rosales
:summary: Implementing the K Nearest Neighbors algorithm from scratch using Python

Say Hi to Your Neighbor!
########################
KNN is a simple approach to classify data points based on some information that you have
about them and how other data has been classified before. For any new entity that needs classification,
KNN simply has us calculate some similarity score based on the variables being measured to previously
classified data. We then take the K values with the highest similarities and simply choose the resulting
class that comes up the most in that set of most similar items.

For example, say you want to predict who someone voted for. You happen to have the results of a random survey
that gives you who people plan to vote for along with two critical pieces of information: their age and distance to
the nearest Whole Foods. You then calculate some similarity score (you'll see how to in a second) based on these
two variables between all of the points in your data and the entity you're trying to classify and choose K of the most
similar. Say for example, you come up with 5 most similar candidates based on age and distance to Whole Foods:
(John Smith, John Smith, John Smith, Jane Doe, Jane Doe). What's the result? John Smith! Why? Because it appears the
most in this "most similar" set of values.

Calculating a Similarity Score
##############################
One way to calculate a data point's similarity to another data point is by measuring the distance of those
two points in Euclidean space. Simply put, some N-dimensional space where points are designated by coordinates.
For example, in a 2D space we have x and y coordinates. Say one point at coordinate (0, 1) and another at (2, 3).

You can calculate this distance with a simple formula:

.. image:: /static/post18/euclidean_distance.png
  :width: 60%
  :alt: The Euclidean distance formula

So in our example, that would be Sqrt( (x1 - x0)^2 + (y1 - y0)^2) ) = Sqrt( (2 - 0)^2 + (3 - 1)^2 ) = Sqrt( 8 ) = 2.83.

This distance can represent how similar two points are to each other. Basically the smaller the distance, the more
similar the points are to each other.

Implementation
##############
Let's jump right in! So all we have to do is for each value in our data, calculate the Euclidean distance
between data points, keep these distances along with the resulting labels in a list, sort the list in ascending order,
pick the top K labels that pop up in that sorted list, and choose the label that occurs the most.

Let's start with implementing the piece that calculates our similarity score

.. code-block:: python

    import numpy as np

    def euclidean_distance(point_a, point_b):
        """Calculates the Euclidean distance between two points
        :param point_a - a numpy array representing a coordinate
        :param point_b - another numpy coordinate array
        """
        assert(len(point_a) == len(point_b))
        return np.linalg.norm(point_b - point_a)

Easy peasy numpy implementation that does just what we spoke about in the similarity score section above.

Now let's implement the component that picks the resulting classes.

.. code-block:: python

    def classify(similarity_array, k):
        """Picks the class based on the largest frequency
        in K most similar list
        :param similarity_array - array containing classes and distances
        :param k - the K most similar items to filter to
        """
        # Sort and pick the top K items with smallest distances
        sorted_result = np.sort(
            similarity_array,
            order=['distance']
        )
        most_similar = sorted_result[:k]
        # Get the counts of classes in the most similar list
        classes = list(map(lambda x: x['class'], most_similar))
        unique, counts = np.unique(classes, return_counts=True)
        # Get the index of the class that appears the most
        max_index = np.argmax(counts)
        return unique[max_index]

Here we simply sort the given similarity array that contains the distance of the point
being classified to each of the individual data points that are already classified along
with their classes. Then we pick the K most similar values from that list and choose the
class in the resulting list with the highest occurrence.

Next let's write the code to iterate over every data point and calculate the distances.

.. code-block:: python

    def get_similarity_scores(point_to_classify, data):
        """Calculates an array of the class and the given point
        to classify's distance to the variables corresponding to
        each class in the data
        :param point_to_classify - NP array of point to classify
        :param data - NP array of classified data
        """
        dtype = [('class', 'S10'), ('distance', float)]
        # Create list of class to distance of two points for each point in data
        values = [
            (point['class'],
            euclidean_distance(
                np.array(
                    [point_to_classify['age'],
                    point_to_classify['whole_foods_distance']]
                ),
                np.array(
                    [point['age'],
                    point['whole_foods_distance']]
                ))
            ) for point in data
        ]
        return np.array(values, dtype=dtype)

Finally, we put it all together with some dummy data.

.. code-block:: python

    # Our fictitious candidate to age and Whole Foods distance data
    dtype = [('class', 'S10'), ('age', int), ('whole_foods_distance', float)]
    values = [
        ('Jane Doe', 27, 3.4),
        ('John Smith', 45, 20.3),
        ('Jane Doe', 30, 6.8),
        ('John Smith', 51, 32.4),
        ('Jane Doe', 19, 2.3),
        ('John Smith', 63, 23.2),
        ('Jane Doe', 29, 10.1),
        ('John Smith', 71, 50.6),
        ('John Smith', 43, 10.5),
        ('Jane Doe', 30, 32.4),
        ('John Smith', 51, 9.3),
        ('Jane Doe', 50, 6.1),
        ('John Smith', 54, 32.1),
        ('Jane Doe', 25, 4.5)
        ]
    data = np.array(values, dtype=dtype)

    # Value that needs classification
    dtype = [('age', int), ('whole_foods_distance', float)]
    value = [(29, 10.1)]
    point_to_classify = np.array(value, dtype=dtype)

    # Get distances to each point in the data
    similarity_array = get_similarity_scores(point_to_classify, data)

    # Start with some arbitrary K
    k = 4

    # Classify
    classify(similarity_array, k)

And who will our 29 year-old person whole lives 10.1 miles from a Whole Foods vote for?...Jane Doe!

Determining K
#############
You may have noticed that our choice of K matters. If we choose K = to the number of data points we have
then it's not difficult to see that the resulting classification is just the candidate that
appears the most in our data. On the other hand, if we choose a small K like 1 then our results
can be pretty wrong because we're basing the entire decision on just one other data point.

This actually comes up quite a lot with these non-parametric modeling techniques. It's called
hyperparameter tuning. Sounds fancy but in this case it's nothing more than choosing a K
value that will lead to the best classification (i.e. best model).

So how do we go about this? Well one way is by randomly splitting our already labeled data into
training and test cohorts. We already know what the labels are so we can compare what our model tells us
that we should choose for each data point with the "correct" answer that's available for each point. For
each point, we predict what the label should be based on the model run on the training split of the data. If
the prediction matches the correct label then hurray, we get a 1 for that pair. If the prediction doesn't match
then we get a 0. You sum up the 1s and divide by the number of elements in your test set to get an accuracy %.
You can repeat this process for each K value starting at 1 and make your way up. You will most likely find
that the accuracy % is maximized by some K value and this is what you choose! It's the K value that minimizes
the test error.

What I just described is called cross-validation and it's a common technique used to choose hyperparameters like K.


