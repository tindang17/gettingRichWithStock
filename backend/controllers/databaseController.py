import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google

cred = credentials.Certificate('google_ service_account.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

stocksCollection = u'stocks'
stockDailyCountCollection = u'stockDailyCount'
redditCollection = u'reddit'


def GetDoc(collection, docName):
    doc_ref = db.collection(collection).document(docName)

    try:
        doc = doc_ref.get()
        return doc.to_dict()
    except google.cloud.exceptions.NotFound:
        return None


def SetDoc(collection, docName, doc):
    doc_ref = db.collection(collection).document(docName)
    doc_ref.set(doc)


def UpdateDoc(collection, docName, doc):
    doc_ref = db.collection(collection).document(doc)
    doc_ref.update(doc)


def IncrementDoc(collection, docName, field, amount):
    doc_ref = db.collection(collection).document(docName)
    doc_ref.update({field: firestore.Increment(amount)})


# Stock
def CreateStockObject(symbol, count=None):
    doc = {
        'symbol': symbol
    }

    if count != None:
        doc['count'] = count

    return doc


def GetStock(symbol):
    return GetDoc(stocksCollection, symbol)


def SetStock(doc):
    SetDoc(stocksCollection, doc['symbol'], doc)


def UpdateStock(doc):
    UpdateDoc(stocksCollection, doc['symbol'], doc)


def IncrementStockDailyCount(symbol, count, date):
    doc_ref = db.collection(stocksCollection).document(
        symbol).collection(stockDailyCountCollection)


def IncrementStockCount(symbol, count):
    IncrementDoc(stocksCollection, docName=symbol, field='count', amount=count)


# Reddit
def CreateSubredditObject(fullname, subName=None, lastCheck=None):
    doc = {
        'fullname': fullname
    }

    if subName != None:
        doc['subName'] = subName

    if lastCheck != None:
        doc['lastCheck'] = lastCheck

    return doc


def SetSubreddit(doc):
    SetDoc(redditCollection, doc['fullname'], doc)


def UpdateSubreddit(doc):
    UpdateDoc(redditCollection, doc['fullname'], doc)


def GetSubreddit(subName):
    return GetDoc(redditCollection, subName)
