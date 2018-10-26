import praw
import boto3
import os
from datetime import datetime


def get_reddit_keys():
    return os.environ["REDDIT_CLIENT_ID"], os.environ["REDDIT_CLIENT_SECRET"]


def get_bucket_name():
    return os.environ["BUCKET_NAME"]


def get_fetch_count():
    return int(os.environ["FETCH_COUNT"])


def get_top_reddit_news():
    """
    Fetch top n reddit headlines.

    Returns:
        list[list]: a list of length three lists. Each sublist contains id, score, title
    """
    reddit_client_id, reddit_client_secret = get_reddit_keys()
    fetch_count = get_fetch_count()

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         user_agent="web")

    subreddit = reddit.subreddit("news").hot(limit=fetch_count)

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

    s3 = boto3.resource("s3")

    data = "Date,ID,Score,Title\n"
    for entry in news:
        line_entry = [str(todays_date)] + ['"' + str(x) + '"' for x in entry]
        line = ",".join(line_entry) + "\n"
        data += line

    bucket_name = get_bucket_name()
    s3.Bucket(bucket_name).put_object(Key=filename, Body=data)


def lambda_handler(event, context):
    """
    Invoked function for AWS Lambda
    """

    news = get_top_reddit_news()
    print("Fetched {0} headlines.".format(len(news)))

    write_news_to_s3(news)
    print("Wrote news to S3.")

    return {
               "statusCode": 200,
               "body": "Successfully wrote {0} headlines to S3.".format(len(news))
           }
