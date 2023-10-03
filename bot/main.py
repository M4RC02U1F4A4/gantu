import telegram
import asyncio
import logging
import os
import pymongo
import requests

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
LOGLEVEL = os.getenv('LOGLEVEL').upper()
MONGODBSTRING = os.getenv('MONGODBSTRING')
BOT_HEALTHCHECKS_ID = os.getenv('BOT_HEALTHCHECKS_ID')


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level="INFO")
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def send_message(): 
    telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)
    mongo_client = pymongo.MongoClient(MONGODBSTRING)
    db = mongo_client.ransomware
    dataDB = db['data']

    query = {'notified': False, "country": "italy"}
    documents = dataDB.find(query)

    for document in documents:
        if document:
            id = document.get('_id', '')
            title = document.get('victim', '')
            website = document.get('website', '')
            published = document.get('published', '')
            group = document.get('group', '')
            country = document.get('country', '')

            message = f"*{title}*\n\nWebsite: {website}\nCompromised by: {group}\nCountry: {country}\n\n{published}" 
            logging.info(document)
            dataDB.update_one({'_id': id}, {'$set': {'notified': True}})
            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
    try:
        requests.get(f"https://hc-ping.com/{BOT_HEALTHCHECKS_ID}", timeout=10)
    except requests.RequestException as e:
        logging.error("Ping failed: %s" % e)
    

def main():
    try:
        requests.get(f"https://hc-ping.com/{BOT_HEALTHCHECKS_ID}/start", timeout=10)
    except requests.RequestException as e:
        logging.error("Ping failed: %s" % e)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
    loop.close()

if __name__ == '__main__':
    main()
