import praw
import json
import boto3
import csv
import decimal
import datetime
from botocore.exceptions import ClientError
from controllers import databaseController


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

dynamodb = boto3.resource('dynamodb')
StockMentionCountTable = dynamodb.Table('StockMentionCount')
SubredditTrackTable = dynamodb.Table('SubredditMentionCount')


def CountSubmission():
    global reddit

    subredditDisplayName = 'wsb'

    subreddit = reddit.subreddit(subredditDisplayName)

    fullname = subreddit.fullname
    lastCheck = 0
    previousLastCheck = 0

    subredditMentionCount = databaseController.GetSubreddit(fullname)
    if subredditMentionCount == None:
        obj = databaseController.CreateSubredditObject(
            subreddit.fullname,
            subName=subreddit.display_name,
            lastCheck=0)
        databaseController.SetSubreddit(obj)
        subredditMentionCount = databaseController.GetSubreddit(fullname)

    stockCounts = {}
    for submission in subreddit.new(limit=1):
        lastCheck = submission.created_utc

    previousLastCheck = subredditMentionCount['lastCheck']
    for submission in subreddit.new(limit=None):
        # for submission in subreddit.new(limit=30):
        # Only check new submission
        if submission.created_utc < previousLastCheck:
            continue

        created_utc = submission.created_utc
        date = datetime.datetime.fromtimestamp(
            created_utc).strftime('%Y-%m-%d')
        title = submission.title
        title = title.split()
        # submissionFullname = submission.fullname

        for word in title:
            if word in stockList:
                if word in stockCounts:
                    if date in stockCounts[word]:
                        stockCounts[word][date]['count'] += 1
                    else:
                        stockCounts[word][date] = {
                            'count': 1,
                            'date': date
                        }
                else:
                    stockCounts[word] = {}
                    stockCounts[word][date] = {
                        'count': 1,
                        'date': date
                    }

    subredditObj = databaseController.CreateSubredditObject(
        fullname=fullname, lastCheck=lastCheck)
    databaseController.SetSubreddit(subredditObj)

    for symbol in stockCounts:
        stock = databaseController.GetStock(symbol)
        if stock == None:
            databaseController.SetStock(symbol)

        stockCount = stockCounts[symbol]
        databaseController.IncrementStockCount(symbol, stockCount)
    print()
    # AddRedditSubmissionTrack(fullname, count)


def CountComment():
    global reddit

    subreddit = reddit.subreddit('wsb')

    for submission in subreddit.new(limit=1000):
        # submission.comments.replace_more(limit=None)
        title = submission.title
        title = title.split()

        count = 0
        for word in title:
            if word in stockList:
                count += 1

        # for comment in submission.comments.list():
        #     print("\t" + comment.body)
        print()


def AddRedditSubmissionTrack(fullname, count):
    global SubredditTrackTable

    item = {
        'fullname': fullname,
        'count': count
    }
    AddItemToDB(SubredditTrackTable, item)


def AddSubRedditTrack(fullname, displayName):
    global SubredditTrackTable

    item = {
        'fullname': fullname,
        'mentionCount': 0,
        'lastCheck': 0,
        'displayname': displayName
    }
    AddItemToDB(SubredditTrackTable, item)


def GetSubredditMentionCount(fullname):
    global SubredditTrackTable

    try:
        result = SubredditTrackTable.get_item(
            Key={
                'fullname': fullname
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    else:
        if 'Item' not in result:
            return None
        else:
            return result['Item']


def CheckIfStockCountExist(symbol):
    global StockMentionCountTable

    try:
        result = StockMentionCountTable.get_item(
            Key={
                'symbol': symbol
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        if 'item' not in result:
            return False
        else:
            return True
        return True


def AddStockMentionCount(symbol, mentionCount):
    global StockMentionCountTable

    item = {
        'symbol': symbol,
        'mentionCount': mentionCount
    }
    AddItemToDB(StockMentionCountTable, item)


def UpdateSubredditTrack(fullname, mentionCount, lastCheck):
    global SubredditTrackTable

    key = {
        "fullname": fullname
    }

    updateExpression = "set mentionCount = mentionCount + :val, lastCheck = :lastCheck"

    expressionAttributeValues = {
        ':val': mentionCount,
        ':lastCheck': decimal.Decimal(lastCheck)
    }

    UpdateItemToDB(SubredditTrackTable,
                   key,
                   updateExpression,
                   expressionAttributeValues)


def UpdateStockCountTrack(symbol, mentionCount):
    global StockMentionCountTable

    key = {
        "symbol": symbol
    }

    updateExpression = "set mentionCount = mentionCount + :mentionCount"

    expressionAttributeValues = {
        ':mentionCount': mentionCount,
    }

    UpdateItemToDB(SubredditTrackTable,
                   key,
                   updateExpression,
                   expressionAttributeValues)


def UpdateStockTrack(symbol, mentionCount):
    global StockMentionCountTable

    key = {
        "symbol": symbol
    }

    updateExpression = "set mentionCount = mentionCount + :val"

    expressionAttributeValues = {
        ':val': mentionCount,
    }

    UpdateItemToDB(StockMentionCountTable,
                   key,
                   updateExpression,
                   expressionAttributeValues)


def AddItemToDB(table, item):
    table.put_item(Item=item)


def UpdateItemToDB(table, key, updateExpression, expressionAttributeValues):
    table.update_item(
        Key=key,
        UpdateExpression=updateExpression,
        ExpressionAttributeValues=expressionAttributeValues,
        ReturnValues="UPDATED_NEW"
    )


def Count():
    CountSubmission()


Count()
