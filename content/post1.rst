****************************************************
ML Demystified: Text Classification with Naive Bayes
****************************************************

:date: 2020-12-01 19:54
:modified: 2020-12-01 19:54
:tags: ML
:category: Machine Learning
:authors: Adams Rosales
:summary: Implementing Naive Bayes from scratch using Python
:header_cover: /static/post1/header.jpg

Enter Bayes
###########
Say you have a collection of documents and some classes those documents belong to. You want to create some model to help
you label other documents with the most likely class based on these data. For example, you have data on thousands of
e-mails and whether those e-mails contain spam or not and want to use this information to filter future spam e-mails
from ever reaching your inbox. Let's code a simple Naive Bayes algorithm in Python to help us do that!

First Some Math
###############
Naive Bayes is based on Bayes' Rule. This theorem provides a way to estimate the probability of some event A occurring
when another event B has occurred when we know the likelihood of B occurring when A has occurred and the probability of
A and B. The formula is P(A|B) = P(A) P(B|A)/P(B).

As an example, say you have a standard deck of 52 cards.
What is the probability of drawing a queen if you draw a face card (queen, king, or jack)? Let's use Bayes' Rule.
The probability of drawing a queen given a face card = [(probability of drawing a queen) X (the probability of drawing a
face card given that you drew a queen)] / (the probability of drawing a face card). Well the probability of drawing a
face card given that you drew a queen is just 1 because queens are always considered a face card. The probability of
drawing a queen is 4/52 (4 queens in a deck) and the probability of drawing a face card is 12/52 (4 jacks, 4 queens,
and 4 kings in a deck) so ((4/52) X 1)/(12/52) = 4/12 or 1/3.

Naive Bayes Algorithm for Text Classification
##############################################
Now that we've gotten that out of the way, let us dive into the algorithm with the spam filtering example!
Suppose you have the following condensed e-mail: "Dear sir, I am Dr. Tunde, brother of Nigerian Prince." We want to
classify it as either spam or not spam. We can utilize Bayes' Rule here as follows.

.. code-block:: python

    P(Spam | "Dear sir, I am...") =
        [P("Dear sir, I am..." | Spam) P(Spam)] / P("Dear sir, I am...") P(Not Spam | "Dear sir, I am...") =
            [P("Dear sir, I am..." | Not Spam) P(Not Spam)] / P("Dear sir, I am...")

We will simply calculate these conditional probabilities and choose the class (spam or not spam) that gives us the
highest one. Knowing this, we can remove the denominator since it's the same in both equations and we just want to
determine which yields the highest probability.

.. code-block:: python

    P(Spam | "Dear sir, I am...") = P("Dear sir, I am..." | Spam) P(Spam)

    P(Not Spam | "Dear sir, I am...") = P("Dear sir, I am..." | Not Spam) P(Not Spam)

Okay so now we have a simple equation we can work with. Look at all your previous e-mails in your training data that
were classified as spam and not spam. Then count the number of times "Dear sir, I am Dr. Tunde, brother of Nigerian
Prince" appears in both sets of e-mails. Assuming an equal number of spam and not spam e-mails, the class with the
highest count of this phrase will result in the highest probability and this is the class we'll choose for this
particular e-mail.

There is one major obstacle here. What if this phrase doesn't exist in our past e-mails data? We'll have a probability
of zero for both spam and not spam, rendering the algorithm useless. Well instead of looking at whole phrases, let's
consider the individual words that make up those phrases. We can rewrite the conditional probabilities as follows if we
assume that words in a phrase are independent:

.. code-block:: python

    (Spam | "Dear sir, I am...") = P("Dear" | Spam) P("sir" | Spam)...P("Prince" | Spam) P(Spam)

    P(Not Spam | "Dear sir, I am...") = P("Dear" | Not Spam) P("sir" | Not Spam)...P("Prince" | Not Spam) P(Not Spam)

Now the algorithm shifts from counting whole phrases to counting individual words within the two types of e-mails in
the data and multiplying the individual word counts or probabilities. This puts the "Naive" in Naive Bayes because
we're making a big assumption that the words are independent of each other. That is what gives us the freedom to
multiply the individual word probabilities. The tradeoff is that words in a phrase are not actually independent of
each other. For example, the position of the word "and" depends on other words before and after it in a phrase.

Back to the algorithm! All we need to do is calculate these probabilities. The probability of spam/not spam is simple
to determine. Just count the number of spam and not spam e-mails and divide by the total number of e-mails. Let's say
we have 100 spam e-mails and 200 not spam e-mails in our training data. The probability of spam is 1/3 and the
probability of not spam is 2/3. The individual word probabilities are a little more nuanced. We count the number of times
each word appears in the training data for each type of e-mail and divide by the total number of words in each type.
Suppose "Dear" appears 50 times in all spam e-mails and 25 times in non-spam e-mails and there are 500 words in total
across all spam e-mails and 600 across non-spam e-mails. The probability of "Dear" given spam is 50/500 or 1/10 and
given not spam is 25/600 or 1/24.

Let's consider the case where the word "Dear" does not appear in any of the spam e-mails in the training data. The
probability of "Dear" would then be 0 and since we're multiplying probabilities, the total probability of all words
multiplied together would be 0. The way to get around this is to add 1 to each word probability numerator. Then to
ensure that we always have a number between 0 and 1 for our probabilities, we add a larger number to the denominator.

Each individual word's probability is then [(number of times the word appears in a class of documents) + 1]/[(number of
words in the class of documents) + vocabulary]. The vocabulary value is just the number of unique words in all documents
of all classes in the training data. This procedure is termed additive or Laplace smoothing and it ensures that none of
the individual word probabilities can be 0 or greater than 1.

Implementing the Algorithm
##########################
Now that we have a general understanding of how the Naive Bayes algorithm works, let's code it up in Python!

Let's start by declaring the functions we will implement one by one.

.. code-block:: python

    def parse_training_data(data_obj):
        """ Given an object of document sets per class this function extracts the vocabulary
        across all documents, the count of unique words by class of document, and the count
        of document types. It returns a tuple like the one below.

        (
            count of unique words across all documents (number),
            count of words by class (dictionary - {cls_name:{word:count, total:total words}}),
            count of documents of each class (dictionary - {cls_name:count, total:total_docs})
        )
        """
        pass


    def calculate_probability(word_counter, vocab, class_count, test_documents):
        """ This function takes in a dictionary of word counts , the total
        vocabulary across all documents in the training data, the of documents by class,
        and documents we want to classify and calculates the probability of the test
        documents to belonging each class. It returns a list of dictionaries containing
        the class of document as the key and the probability of belonging to that
        class as the value.
        """
        pass


    def predict(parsed_train_data, test_data):
        """ This function takes in the parsed training data object from parse_training_data
        above and the test data as a list of documents that we want to classify.
        It then calls calculate_probability, which returns all the probabilities of belonging
        to each class. It iterates over this list which will have one dictionary for each
        test document and it chooses the class of document that has the largest probability
        value. The function then returns a list of predicted document types for each test
        document.
        """
        pass


    def naive_bayes_text(train_data, test_data):
        """ Takes in a training data object with the class of document as the key and a
        list of documents as the value. Calls parse_training_data bove and predict to label
        each document with a class based on the training data. Returns  a list of predicted
        classes corresponding to each document in the test data.
        """
        pass

Now let's implement the parse_training_data function. This function takes a Python dictionary as input. The dictionary
will be structured just like our toy training data at the bottom of this page (the class of document as the key and a
list of documents as the value for each key). It will iterate over each key and value pair in this dictionary, iterate
over each document in the list of documents for each class, and over each word in each document. As it does this, it
will keep track of the unique words it encounters in the set called vocab_set, maintain a class counter dictionary which
has the count of unique documents by type, and a word counter dictionary which has the count by word for each class. It
will then return a tuple with the length of the vocab_set (unique words across all documents which acts as our
vocabulary), the word counts by class of document, and the count of unique documents by class of document.

.. code-block:: python

    def parse_training_data(data_obj):
        """ Given an object of document sets per class this function extracts the vocabulary
        across all documents, the count of unique words by class of document, and the count
        of document types. It returns a tuple like the one below.
        (
            count of unique words across all documents (number),
            count of words by class (dictionary - {cls_name:{word:count, total:total words}}),
            count of documents of each class (dictionary - {cls_name:count, total:total_docs})
        )
        """
        vocab_set = set()
        word_counts = {}
        class_counts = {}
        class_total = 0
        # Break data object into class_name, documents
        for cls_name, docs in data_obj.items():
            class_counts[cls_name] = 0
            word_counts[cls_name] = {}
            word_total = 0
            # Iterate over each document in list of documents
            for doc in docs:
                # Increment the count of document type
                class_counts[cls_name] += 1
                class_total += 1
                # Iterate over each word in the document
                for word_orig in doc.split(" "):
                    # Convert all words to same case
                    word = word_orig.lower()
                    # Add the word to the vocabulary set
                    vocab_set.add(word)
                    word_total += 1
                    # Increment the count of word in the current class
                    if word_counts[cls_name].get(word):
                        word_counts[cls_name][word] += 1
                    else:
                        word_counts[cls_name][word] = 1
            # Add the count of total words in the class to word counts dict
            word_counts['total'] = word_total
        # Add the count of total classes to the class counts dict
        class_counts['total'] = class_total
        # Return (unique vocabulary, count of words by class, and count of docs by class)
        return len(vocab_set), word_counts, class_counts

Next let's implement the calculate_probability function. Here we're going to take in a dictionary of word counts by
document class, a vocabulary number (count of unique words in the training data),  a dictionary of document counts by
document class, and a list of documents to calculate probabilities for. The probabilities will denote the likelihood of
belonging to each document class by test document. The function will return a list of dictionaries where each dictionary
corresponds to each document in the test document input list and contains key-value pairs with the class of document as
the key and the probability of belonging to that document as the value.

As defined in the algorithm section above, the total probability of belonging to a certain class of document is
calculated by multiplying the individual word probabilities and the probability of the document class itself. However,
when actually implementing this calculation, we need to be able to handle very small floating point numbers. Since we're
multiplying probabilities between 0 and 1, we can get very small floats that may result in arithmetic underflow. This
happens when the result of a calculation is a number that is too small for the computer to store in memory. A solution
to this is to take the log of the individual word probabilities and add these log values (recall from math class long
ago that log(xy) = log(x) + log(y)). Let's do it!

.. code-block:: python

    def calculate_probability(word_counter, vocab, class_count, test_documents):
        """ This function takes in a dictionary of word counts , the total
        vocabulary across all documents in the training data, the of documents by class,
        and documents we want to classify and calculates the probability of the test
        documents to belonging each class. It returns a list of dictionaries containing
        the class of document as the key and the probability of belonging to that
        class as the value.
        """
        rslt = []
        # Iterate over each document in the list of test documents we want to classify
        for doc in test_documents:
            probabilities = {}
            # Iterate over each document class in word_counter
            for doc_cls, word_counts in word_counter.items():
                # Skip if the class is total, which is the total count of words
                if doc_cls == 'total':
                    continue
                # Start with probability of that class based on training data
                probabilities[doc_cls] = math.log(class_count[doc_cls]/
                    (class_count['total']*1.0))
                # Iterate over each word in the document
                for word_orig in doc.split(" "):
                    word = word_orig.lower()
                    # Get word count or 0 if not found in training data
                    word_instance = word_counts.get(word)
                    if not word_instance:
                        word_instance = 0
                    # Add in the log of (count of word + 1)/(total words + vocab) to probability
                    probabilities[doc_cls] += math.log((word_instance + 1)
                        / ((word_counter['total'] + vocab)*1.0))
            # Add in the probability by document class to results list
            rslt.append(probabilities)
        return rslt

Next let's implement the predict function. This function is just tasked with taking the list of probabilities by class
that we get from calculate_probability and choosing the document class corresponding to the largest probability for
each document in the test list. The result of this function are the actual predicted values for each document we fed
the algorithm.

.. code-block:: python

    def predict(parsed_train_data, test_data):
        """ This function takes in the parsed training data object from parse_training_data
        above and the test data as a list of documents that we want to classify.
        It then calls calculate_probability, which returns all the probabilities of belonging
        to each class. It iterates over this list which will have one dictionary for each
        test document and it chooses the class of document that has the largest probability
        value. The function then returns a list of predicted document types for each test
        document.
        """
        vocab, word_counts, class_counts = parsed_train_data
        probabilities = calculate_probability(word_counts, vocab, class_counts, test_data)
        rslt_classes = []
        # Iterate over each doc class : probability dictionary
        for prob_obj in probabilities:
            max_prob = None
            max_cls = None
            # Select the class from the probability dictionary that has the largest probability
            for cls_name,prob in prob_obj.items():
                if max_prob == None or prob > max_prob:
                    max_prob = prob
                    max_cls = cls_name
            # Add the document class corresponding to the largest probability to the result
            rslt_classes.append(max_cls)
        return rslt_classes

Finally we implement the main interface function we can expose and call with our training and test data.

.. code-block:: python

    def naive_bayes_text(train_data, test_data):
        """Takes in a training data object with the class of document as the key and a
        list of documents as the value. Calls parse_training_data bove and predict to label
        each document with a class based on the training data. Returns  a list of predicted
        classes corresponding to each document in the test data."""
        parsed_obj = parse_training_data(train_data)
        return predict(parsed_obj, test_data)

Let's call our naive_bayes_text function with some toy training and test data.

.. code-block:: python

    if __name__ == '__main__':

        # Create toy training data
        training_data = {
            'spam': [
                "Dear sir, I am Dr Tunde, brother of Nigerian Prince",
                "Win a million dollars today",
                "48 hours clearance ends now 48 hours 48 hours Free stuff",
                "Private invite to exclusive event",
                "Discount inside 90 percent off everything",
                "12 days of deals happening now Closeout sale Free giveaways and more",
                "This is your last chance to register for the biggest giveaway of the year",
                "Your attention is needed for this very important message",
                "Tick-tock it's the last day for 30 percent off your purchase",
                "Final hours Mega mega mega mega mega free shipping on all items",
                "Checkout these last minute deals on all electronics",
                "Dear sir, please join me in this one of a lifetime opportunity"
            ],
            'not spam': [
                "It was great catching up with you yesterday give me a call anytime",
                "Please remember to bring the drink ingredients to the party",
                "How did your final exam go yesterday",
                "Please give me a call back",
                "Thanks for inquiring about transferring the non-IRA assets from your personal account",
                "You have a package to pick up at the lobby hub",
                "You have a package to pick up at the lobby hub",
                "Thanks for reaching out, a member of our team will get back to you",
                "You have a package to pick up at the lobby hub",
                "Payment successfully processed for account ending in",
                "I am attaching mom's favorite mulled wine recipe that you can use for this weekend",
                "How are the kids doing"
            ]
        }

        # Train the naive bayes model and predict classes for some toy test data
        print(naive_bayes_text(training_data, [
            "How did your final exam go",
            "Last minute clearance discount",
            "Nigerian Prince",
            "Payment for your kids processed successfully"
        ]))

We get the following result for our document list (["How did your final exam go", "Last minute clearance discount",
"Nigerian Prince","Payment for your kids processed successfully"]):

['not spam', 'spam', 'spam', 'not spam']

There you go. We have successfully implemented a basic Naive Bayes algorithm for text classification just by applying
some simple counting. The final code can be retrieved from my
`Github repository <https://github.com/adaros92/ml_demystified/blob/master/naive_bayes.py>`_ for this
series. Try experimenting with it and running it on real world data. You can change it up so that you don't have to
process the entire training data each time. You can also create the ability to feed the model new data and improve it
incrementally. Have fun!