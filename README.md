# Reddit Fetch Top News Fetch - AWS Lambda

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Description

Data fetching application example using AWS Lambda. Runs on Python 3.6.7.

### Dependencies

    boto3
    praw

# Deployment Info


## Creating Deployment File (Mac/Linux)

First an AWS lambda function must be created and the source must be properly zipped and uploaded.

[Creating a Python deployment package for AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

**Use virtualenv to fetch dependency source** ([How to install/use virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)):

    cd ~/{path_to_repository}/
    virtualenv env
    source env/bin/activate
    pip3 install -r requirements.txt
    deactivate

**Create Deployment zip file:**

    zip -r9 ~/Documents/RedditNews.zip ~/{path_to_repository}/env/lib/python3.5/site-packages

**Add python code to zip:**

    zip -g ~/Documents/RedditNews.zip ~/{path_to_repository}/lambda_function.py

Now you can deploy the package with the `RedditNews.zip` in the `~/Documents/` folder.

## Configure Role for Lambda

In order for the script to write to S3, you will need a role with the proper permissions. I created a role and added the `AmazonS3FullAccess` policy.


## Setup Reddit Application

To read from the Reddit API, you must get your application keys [here](https://github.com/reddit-archive/reddit/wiki/OAuth2).

## Add Environment Variables to Lambda

The following environment variables are needed to run the script ([adding Lambda environment variables](https://docs.aws.amazon.com/lambda/latest/dg/env_variables.html)):

`BUCKET_NAME` : This is the name of the S3 bucket in which to deposit files

`REDDIT_CLIENT_ID` : Client ID from your registered Reddit App.

`REDDIT_CLIENT_SECRET` : Client secret from your registered Reddit App.

`FETCH_COUNT` : Number of articles to fetch.

## Create Cloudwatch Daily Trigger

I used CloudWatch to trigger this task once daily ([how to create a CloudWatch event rule](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/Create-CloudWatch-Events-Scheduled-Rule.html)). This cron expression will configure the trigger to run once daily at 4PM:

    0 16 * * ? *
