import pymongo
import ransomfeed
import logging
import os
from datetime import datetime, timedelta

LOGLEVEL = os.getenv('LOGLEVEL').upper()
MONGODBSTRING = os.getenv('MONGODBSTRING')
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=LOGLEVEL)

def stats():
    total = dataDB.count_documents({})
    data_limit = datetime.now() - timedelta(days=90)
    last_90_days = dataDB.count_documents({"published": {"$gte": data_limit}})
    data_limit = datetime.now() - timedelta(days=7)
    last_7_days = dataDB.count_documents({"published": {"$gte": data_limit}})
    
    country = dataDB.distinct("country")
    by_country = {}
    for c in country:
        by_country[c] = dataDB.count_documents({"country": c})
    
    group = dataDB.distinct("group")
    by_group = {}
    print(group)
    for g in group:
        by_group[g] = dataDB.count_documents({"group": g})

    result = {
        "_id": "stats",
        "total": total,
        "last_90_days": last_90_days,
        "last_7_days": last_7_days,
        "by_country": by_country,
        "by_group": by_group
    }
    try:
        logging.debug(result)
        statsDB.insert_one(result)
    except:
        statsDB.update_one({"_id":"stats"},{"$set":result})
    

mongo_client = pymongo.MongoClient(MONGODBSTRING)
db = mongo_client.ransomware
dataDB = db['data']
statsDB = db['stats']


# Only first time
if not dataDB.find_one():
    for r in ransomfeed.all_ransomfeed():
        logging.debug(r)
        try:
            dataDB.insert_one(r)
        except Exception as e:
            logging.error(e, exc_info=True)
else:
    for r in ransomfeed.parse_ransomfeed():
        try:
            logging.debug(r)
            dataDB.insert_one(r)
        except Exception as e:
            logging.error(e, exc_info=True)

# Update stats
stats()
    