import json
import praw
from datetime import datetime


TOP_N = 25

def get_top_25_reddit_news():
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent='web')

    subreddit = reddit.subreddit('news').hot(limit=TOP_N)

    result = []
    for s in subreddit:
        result.append([s.id, s.score, s.title])

    return result


def write_news_to_file(news):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    filename = "reddit_scrape/dat.csv"

    with open(filename, 'a') as file:
        print("\t* writing data to '%s'" % str(filename))
        for entry in news:
            csv_entry = [unicode(todays_date)] + [u'"' + unicode(x) + u'"' for x in entry]
            line = u",".join(csv_entry)
            file.write(line.encode('utf-8'))
            file.write(u"\n")


def lambda_handler(event, context):
    news = get_top_25_reddit_news()
    write_news_to_file(news)
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!!!')
    }
