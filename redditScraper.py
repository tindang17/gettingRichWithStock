import praw
import json
import boto3
import csv

with open('config.json', 'r') as f:
    config = json.load(f)

redditConfig = config['reddit']
client_id = redditConfig['clientId']
client_secret = redditConfig['clientSecret']
username = redditConfig['username']
password = redditConfig['password']

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                     password=password, user_agent='USERAGENT',
                     username=username)

temp = []
with open('stockList.csv', 'r') as file:
    stockList = csv.reader(file)
    for row in stockList:
        temp.append(row[0])

stockList = temp

subreddit = reddit.subreddit('wsb')
for submission in subreddit.new(limit=100):
    submission.comments.replace_more(limit=None)
    title = submission.title
    print(submission.title)
    title = title.split()
    for word in title:
        if word in stockList:
            print('yes')

    # for comment in submission.comments.list():
    #     print("\t" + comment.body)
    print()

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('StockMentionCount')
# response = table.put_item(
#     Item={
#         'symbol': 'MFST',
#         'count': 1
#     }
# )
