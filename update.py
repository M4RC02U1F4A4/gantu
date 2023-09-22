import pymongo
import ransomfeed
import logging
import os

LOGLEVEL = os.getenv('LOGLEVEL').upper()
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=LOGLEVEL)

def main():
    mongo_client = pymongo.MongoClient(f"mongodb://localhost:27017")
    db = mongo_client.ransomware
    dataDB = db['data']
    statsDB = db['stats']
  
    # Only first time
    if not dataDB.find_one():
        for r in ransomfeed.all_ransomfeed():
            logging.debug(r)
            dataDB.insert_one(r)
    else:
        for r in ransomfeed.parse_ransomfeed():
            try:
                dataDB.insert_one(r)
            except:
                pass

if __name__ == "__main__":   
    main()
    