**************
My Friend, Sam
**************

:date: 2020-12-17 00:00
:modified: 2020-12-17 00:00
:tags: AWS
:category: AWS
:authors: Adams Rosales
:summary: Getting started with AWS Lambda
:header_cover: /static/post7/header.jpg

NoServer
########
Your own servers...

You don't need them!

.. image:: https://media.giphy.com/media/HteV6g0QTNxp6/giphy.gif
  :width: 50%
  :alt: Ron throws a computer away

Instead, you can use a cloud providers' servers to run code when you want. Scale up or down as you wish and pay only for
what you use.

One of the services that allows you to do that is AWS Lambda. Let's jump in!

Setting Up
##########
You will need:

1. An AWS account - `<https://tinyurl.com/y92rahe9>`_
2. The AWS CLI - `<https://tinyurl.com/y3exq8mg>`_
3. An admin IAM user - `<https://tinyurl.com/yybtpoy6>`_
4. SAM CLI - `<https://tinyurl.com/yepgnqtg>`_
5. The AWS CLI configured to use the admin IAM user - `<https://tinyurl.com/y6wp8vqo>`_
6. A Twitter developer account - `<https://tinyurl.com/yd9u8d5a>`_

Creating a Lambda Application
#############################
One of the ways to start building with Lambda is by using the AWS Serverless Application Model (SAM). This is
just a framework that allows developers to easily create, configure, and deploy serverless applications on AWS. We can
get started doing just that with the SAM CLI I linked to above.

Start with a sample SAM template by running the following.

.. code-block:: bash

    $ sam init

This will prompt you for a few things. Choose the options below:

1. Which template source would you like to use? -> AWS Quick Start Templates
2. What package type would you like to use? -> Zip
3. Which runtime would you like to use? -> python3.7
4. Project name: -> SampleApp
5. AWS quick start application templates: -> Hello World Example

The app you create should have the following structure.

.. image:: /static/post7/post7_lambda_tree.jpg
  :width: 60%
  :alt: A sample Lambda application structure

The Python package with the main application code is under hello_world. This is unit tested with the tests defined in
the tests directory. The events directory just contains JSON event payloads for testing. Finally, the template.yml file
has the CloudFormation template which defines the actual Lambda function to deploy and any other resource you want to
create along with the Lambda when deploying to AWS.

Deploying is a breeze. Just run the following:

.. code-block:: bash

    $ sam build && sam deploy --guided

If you go to the CloudFormation console on AWS, you should see the app being deployed along with SAM related resources.

.. image:: /static/post7/post7_sam_deployment.jpg
  :width: 100%
  :alt: Lambda deployment to CFN with SAM

Making the Lambda (Semi) Useful
###############################
Next we'll use this sample Lambda function that has already been deployed as a base for the Lambda we'll actually
write and deploy. We just need to write the code and add some additional resources like an EventBridge scheduler
and IAM roles to access other AWS services.

Now it's almost Christmas and so far I have missed out on gifting myself a PlayStation 5 because it has pretty much been
out of stock everywhere. Any time I hear about restocks it's always too late. However, I did notice the other day while I
was perusing Twitter that there are quite a few accounts that Tweet out when PS5s have been restocked online. Most of them
are garbage but there are a few golden leads.

One of them is a site called Newegg. They Tweet out these standardized restock alerts when they receive new inventory
of some hot product. The Tweets looks like this:

.. image:: /static/post7/post7_newegg_tweet.jpg
  :width: 100%
  :alt: Lambda deployment to CFN with SAM

I really like that little siren character. It means I can write a listener that just looks for a combination of that
one character with the words restock and PS5/PlayStation and sends me an e-mail when there's a match. This should hopefully
filter out a lot of the false positives, especially with all the random chatter about the PS5 being out of stock
everywhere.

Creating the AWS Resources
##########################
To create the resources needed for this I edited the template.yaml CloudFormation template. They include:

- The Lambda itself (already created but I edit it for my purposes and removed default API Gateway)
- The Lambda role with access to SNS
- The EventBridge scheduler running every 15 minutes
- The permission for the EventBridge scheduler to invoke the Lambda

This template is below.

.. code-block:: yaml

    AWSTemplateFormatVersion: '2010-09-09'
    Transform: AWS::Serverless-2016-10-31
    Description: Restock Notification App

    Resources:

      # SNS to send restock text messages to your e-mail
      RestockSns:
        Type: AWS::SNS::Topic
        Properties:
          Subscription:
            - Endpoint: "[EMAIL HERE]"
              Protocol: "email"
          TopicName: "RestockSns"

      # The Lambda function to deploy
      RestockListener:
        Type: AWS::Serverless::Function
        Properties:
          CodeUri: restock_listener/
          Handler: app.lambda_handler
          Runtime: python3.7
          Role: !GetAtt LambdaRole.Arn
          Timeout: 600
          MemorySize: 256
          Environment:
            Variables:
              sns_topic_arn: !Ref RestockSns

      # The role to attach to the Lambda that allows it to use other AWS services
      LambdaRole:
        Type: AWS::IAM::Role
        Properties:
          AssumeRolePolicyDocument:
            Statement:
              - Action: ['sts:AssumeRole']
                Effect: Allow
                Principal:
                  Service: [lambda.amazonaws.com]
            Version: '2012-10-17'
          Policies:
            - PolicyDocument:
                Statement:
                  - Action: ['sns:*']
                    Effect: Allow
                    Resource: '*'
                Version: '2012-10-17'
              PolicyName: LambdaRole

      # Runs the RestockListener Lambda function on a schedule
      RestockListenerSchedule:
        Type: AWS::Events::Rule
        Properties:
          Description: "ScheduledRule"
          ScheduleExpression: "rate(15 minutes)"
          State: "ENABLED"
          Targets:
            - Arn: !GetAtt RestockListener.Arn
              Id: "RestockListenerV1"

      # Provides scheduler access to the Lambda
      PermissionForEventsToInvokeRestockListener:
        Type: AWS::Lambda::Permission
        Properties:
          FunctionName: !Ref RestockListener
          Action: "lambda:InvokeFunction"
          Principal: "events.amazonaws.com"
          SourceArn: !GetAtt RestockListenerSchedule.Arn

    Outputs:
      RestockListener:
        Description: "Restock Listener Lambda function"
        Value: !GetAtt RestockListener.Arn
      LambdaRole:
        Description: "Restock Listener Lambda role"
        Value: !GetAtt LambdaRole.Arn

The [EMAIL HERE] in the SNS endpoint should be filled out with the e-mail address that the Lambda will send the
notifications to.

Implementing the Notification Component
#######################################
In order for the Lambda to send a notification to the SNS that was deployed with it, it needs to be able to access it
and call the SNS API endpoint with a message to send. The Lambda should already have access to SNS through the role
that is also included in the SAM/CloudFormation template but sending the actual message still needs to be implemented.

Since this is a Python Lambda, we can use AWS' Python SDK - `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>`_.
Below I implement a set of simple utility functions to send a message to an SNS endpoint using the boto3 SDK.

.. code-block:: python

    import boto3


    def _get_aws_client(service: str, client: boto3.client = None) -> boto3.client:
        """Retrieves a boto3 client for the given service name if one is not already provided"""
        if not client:
            client = boto3.client(service)
        return client


    def _get_sns_client(client: boto3.client = None) -> boto3.client:
        """Retrieves an SNS boto3 client"""
        return _get_aws_client("sns", client)


    def _send_message(message: str, subject: str, topic_arn: str, client: boto3.client) -> dict:
        """Sends a given message to an SNS topic ARN with the provided SNS client

        :returns the response received back from the request
        """
        response = client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        return response

The first two functions retrieve an SNS boto3 client which we can use to access the different SNS API endpoints. To
publish a message we just need to call the `publish <https://tinyurl.com/y72u9cbh>`_  method of this client object.

Implementing the Tweet Retriever
################################
Now I implement the logic to get a user's tweets and filter to just the ones that contain a list of search terms
and special unicode characters (to find the little Newegg siren). I'm keeping this as simple as possible by using just
the default Tweepy user_timeline functionality, which retrieves the last 20 tweets. This may not work when a user
tweets more often than that in between Lambda invocations but that's okay because I'm running the Lambda on a schedule
every 15 minutes and Newegg only tweets out a few times a day.

Also one of the drawbacks of the serverless approach is that individual Lambda functions cannot keep state in between
executions without using external data stores or more complex step functions state machines. This means that as is,
the Lambda won't be able to dedupe tweets that it has already received. If there's a matching tweet from Newegg, it will
send me the same alert over and over as long as it's part of the last 20 tweets. However, in this scenario, this is
actually a good thing because I really want that PS5. I want to make sure I receive the alert multiple times if I happen
to miss it the first time around. Alternatively, we can always put a filter on the tweet logic to limit the result set
to just the tweets in the X minutes prior to the time of invocation.

.. code-block:: python

    def _get_authorized_tweepy_client(
        consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> tweepy.API:
        """Retrieves an authorized Tweepy API client to use when extracting Tweets

        :param consumer_key
        :param consumer_secret
        :param access_token
        :param access_token_secret
        :returns a signed Tweepy client
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)


    def _get_matching_tweets(screen_name: str, search_terms: list, special_unicode: list, client: tweepy.API) -> list:
        """Retrieves the last 20 Tweets in the given user's timeline and filters them to those containing the given terms
        and unicode characters

        :param screen_name - the Twitter user handle to search for
        :param search_terms - a list of terms to filter Tweets by (must contain all terms in the list)
        :param special_unicode - a list of unicode values (equivalent of ord(char)) for any special characters (emojis)
        :param client - the Tweepy client to use for the request to retrieve Tweets
        :returns a list of matching Tweets containing the required terms and special characters
        """
        # Get the last 20 tweets in the user's timeline
        user_tweets = client.user_timeline(screen_name=screen_name)
        matching_tweets = []
        # Find matching tweets in the user's timeline
        for tweet in user_tweets:
            tweet_text = tweet.text
            # Retrieve individual unicode characters in the tweet text to check for any special characters
            unicode_chars_in_tweet = set([ord(character) for character in tweet_text])
            matching = True
            # If any of the search terms are not in the tweet, skip it
            for search_term in search_terms:
                if search_term.lower() not in tweet_text.lower():
                    matching = False
                    break
            # If any of the special unicode characters are missing from the tweet, also skip it
            for special_unicode_char in special_unicode:
                if special_unicode_char not in unicode_chars_in_tweet:
                    matching = False
                    break
            # If all of the required search terms and special unicode characters are in the tweet, keep track of it
            if matching:
                matching_tweets.append(tweet_text)
        return matching_tweets

All this is doing is retrieving the last 20 tweets and retuning just those that contain all of the search terms we
require and any special characters provided. More information about the Tweepy API can be found `here <http://docs.tweepy.org/en/latest/>`_.

Implementing the Lambda Handler
###############################
To finish up, all we need to do is implement the handler itself. This is the function exposed through Lambda and what
will be called by EventBridge every 15 minutes.

.. code-block:: python

    def _verify_event_payload(event: dict) -> None:
        """Raises exception if the Lambda input is invalid

        :param event - a dictionary containing the key/value pairs passed in as an event payload to the Lambda
        """
        required_inputs = [
            "subject", "consumer_key", "consumer_secret", "access_token",
            "access_token_secret", "screen_name", "search_terms", "special_unicode"]
        for required_input in required_inputs:
            if required_input not in event:
                raise ValueError("The provided event payload is missing required input - {0}".format(required_input))
        assert type(event["search_terms"]) == list and type(event["special_unicode"]) == list

    def lambda_handler(event: dict, _) -> dict:
        """ The main handler function that will run as a Lambda

        :param event - a dictionary of key/value data to operate with
        :returns a response from the SNS service when the Lambda sends out a notification, otherwise an empty dictionary
        """
        # Get event input provided to Lambda and verify it (exception will be thrown at this point if anything is off)
        _verify_event_payload(event)
        # Retrieve matching tweets for the given user
        tweepy_client = _get_authorized_tweepy_client(
            event["consumer_key"], event["consumer_secret"],
            event["access_token"], event["access_token_secret"]
        )
        matching_tweets = _get_matching_tweets(
            event["screen_name"], event["search_terms"],
            event["special_unicode"], tweepy_client
        )
        message = "\n\n".join(matching_tweets)
        response = {}
        # Send a message if there are any matching tweets
        if len(matching_tweets) > 0:
            # Get the SNS topic ARN to send an alert message to from Lambda's environment variables
            sns_topic_arn = os.environ["sns_topic_arn"]
            # Retrieve the SNS client
            sns_client = _get_sns_client()
            # Send the message
            response = _send_message(message, event["subject"], sns_topic_arn, sns_client)
        return response

The Lambda will receive an event payload from EventBridge containing all of the necessary inputs to run the alarming
with. Those include the subject of the alarm (e-mail subject when sending to the user), the Twitter developer keys and
tokens (bad practice - don't do this!), the Twitter screen name to retrieve tweets for, and the search terms/special
unicode characters to filter by.

Here I'm providing the Twitter keys as an input because I'm sure no one else is using this and it's a toy example.
In practice you would want to store these keys in a secure location that your Lambda can access. AWS offers a service
for this called `SecretsManager <https://aws.amazon.com/secrets-manager/>`_.

Anyway, to include this payload in the EventBridge scheduler we can just add it to the CloudFormation template like so:

.. code-block:: yaml

  # Runs the RestockListener Lambda function on a schedule
  RestockListenerSchedule:
    Type: AWS::Events::Rule
    Properties:
      Description: "ScheduledRule"
      ScheduleExpression: "rate(15 minutes)"
      State: "ENABLED"
      Targets:
        - Arn: !GetAtt RestockListener.Arn
          Id: "RestockListenerV1"
          Input: '{
            "subject": "RESTOCK ALERT!",
            "consumer_key": "",
            "consumer_secret": "",
            "access_token": "",
            "access_token_secret": "",
            "screen_name": "Newegg",
            "search_terms": [
                "restock", "ps5"
            ],
            "special_unicode": [
                128680
            ]
          }'

Deploying and Testing
#####################
To deploy I run:

.. code-block:: bash

    $ sam build && sam deploy

With a bit of luck everything works and I'll have a PS5 in no time.

To test this at runtime I can configure a test event in the AWS console. Since I'm sure Newegg has tweeted some restock
alerts recently I will run the Lambda with the following payload (just including "restock" as a term without the
additional "ps5" requirement).

.. code-block:: python

      {
          "subject": "RESTOCK ALERT!",
          "consumer_key": "",
          "consumer_secret": "",
          "access_token": "",
          "access_token_secret": "",
          "screen_name": "Newegg",
          "search_terms": [
            "restock"
          ],
          "special_unicode": [
            128680
          ]
      }

.. image:: /static/post7/post7_lambda_test_configuration.jpg
  :width: 100%
  :alt: A Lambda restock alarm test configuration

Hit Test and voila!

.. image:: /static/post7/post7_restock_email.jpg
  :width: 100%
  :alt: An e-mail from the restock Lambda service

