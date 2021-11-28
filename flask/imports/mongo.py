import pymongo
from . import neostring
import time

def inject_mongo(df, data):
    # temp_db = database / datas = table
    conn = pymongo.MongoClient("mongodb://mongo:27017/", username='root', password='mongodb')
    #conn = MongoClient(MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True), u'temp_db')
    databasename = neostring.random(50)
    collectionname = neostring.random(50)
    mydb = conn[databasename]
    collection = mydb[collectionname]
    start_time = time.time()
    for key in data['data']:
        rec_id1 = collection.insert_one(key)
    return (time.time() - start_time)