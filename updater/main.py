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
        logging.warn(e, exc_info=False)
    