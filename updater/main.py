import pymongo
import ransomfeed
import logging
import os

LOGLEVEL = os.getenv('LOGLEVEL').upper()
MONGODBSTRING = os.getenv('MONGODBSTRING')
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=LOGLEVEL)

mongo_client = pymongo.MongoClient(MONGODBSTRING)
db = mongo_client.ransomware
dataDB = db['data']

if not dataDB.find_one():
    notified = True
else:
    notified = False

for r in ransomfeed.parse_ransomfeed(notified):
    try:
        logging.debug(r)
        dataDB.insert_one(r)
    except Exception as e:
        dataDB.update_one({"_id":r['_id']}, {"$set":{"victim":r['victim'], "country":r['country'], "website":r['website'], "group":r['group'], "published":r['published']}})
        logging.warn(e, exc_info=False)