import json
import praw
import boto3
import os
from datetime import datetime


def get_keys_from_environ():
    return (os.environ['REDDIT_CLIENT_ID'], os.environ['REDDIT_CLIENT_SECRET'])
def get_bucket_name():
    return os.environ['BUCKET_NAME']


def get_top_n_reddit_news(top_n):
    """
    Fetch top n reddit headlines.

    Args:
        top_n (int): number of headlines to return

    Returns:
        list[list]: a list of length three lists. Each sublist contains id, score, title
    """
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET = get_keys_from_environ()

    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent='web')

    subreddit = reddit.subreddit('news').hot(limit=top_n)

    result = []
    for s in subreddit:
        result.append([s.id, s.score, s.title])

    return result


def write_news_to_s3(news):
    """
    Write news article headlines to CSV file in S3

    Args:
        news (list[list]): takes the output of get_top_n_reddit_news()

    Returns:
        None
    """

    todays_date = datetime.now().strftime("%Y-%m-%d")
    filename = "data_{0}.csv".format(todays_date)

    s3 = boto3.resource('s3')

    data = "Date,ID,Score,Title\n"
    for entry in news:
        line_entry = [str(todays_date)] + ['"' + str(x) + '"' for x in entry]
        line = ",".join(line_entry) + "\n"
        data += line

    bucket_name = get_bucket_name()
    s3.Bucket(bucket_name).put_object(Key=filename, Body=data)


def lambda_handler(event, context):
    """
    Invoked function for Amazon Lambda
    """
    NUM_ARTICLES = 50

    news = get_top_n_reddit_news(NUM_ARTICLES)
    print("Fetched {0} headlines.".format(NUM_ARTICLES))

    write_news_to_s3(news)
    print("Wrote news to S3.")

    return {
        "statusCode": 200,
        "body": "Successfully wrote {0} headlines to S3.".format(len(news))
    }
