# Deployment Info


## Creating Deployment File

First an AWS lambda function must be created and the source must be properly zipped and uploaded.

[Creating a Python deployment package for AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

**Create Deployment zip file**

    cd ~/Code/news_fetch_lambda/virtualenv/lib/python3.5/site-packages
    zip -r9 ~/Downloads/RedditNews.zip .

**Add python code to zip**

    cd ~/Code/news_fetch_lambda/
	zip -g ~/Downloads/RedditNews.zip lambda_function.py

## Configure Role for Lambda

...


## Add Environment Variables to Lambda

...


## Create Cloudwatch Daily Trigger

...
