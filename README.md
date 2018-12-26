# Reddit Fetch Top News Fetch - AWS Lambda

### Description

Data fetching application example using AWS Lambda. Runs on Python 3.6.7.

### Dependencies

    praw

# Deployment Info


## Creating Deployment File (Mac/Linux)

First an AWS lambda function must be created and the source must be properly zipped and uploaded.

[Creating a Python deployment package for AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

**Create Deployment zip file**

    cd ~/{path_to_repository}/virtualenv/lib/python3.5/site-packages
    zip -r9 ~/Downloads/RedditNews.zip .

**Add python code to zip**

    cd ~/{path_to_repository}/
	zip -g ~/Downloads/RedditNews.zip lambda_function.py

## Configure Role for Lambda

In order for the script to write to S3, you will need a role with the proper permissions. I created a role and added the `AmazonS3FullAccess` policy.


## Setup Reddit Application

To read from the Reddit API, you must get your applcation keys [here](https://github.com/reddit-archive/reddit/wiki/OAuth2).

## Add Environment Variables to Lambda

Three environment variables are needed to run the script:

`BUCKET_NAME` : This is the name of the S3 bucket in which to deposit files

`REDDIT_CLIENT_ID` : Client ID from your registered Reddit App.

`REDDIT_CLIENT_SECRET` : Client secret from your registered Reddit App.

`FETCH_COUNT` : Number of articles to fetch.

## Create Cloudwatch Daily Trigger

I used cloudwatch to trigger this task once daily. This cron expression will configure the trigger to run once daily at 4PM:

    0 16 * * ? *
