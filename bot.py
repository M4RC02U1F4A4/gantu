import telegram
import asyncio
import logging
import os
import pymongo

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
LOGLEVEL = os.getenv('LOGLEVEL').upper()


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level="WARNING")
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def send_message(): 
    telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)
    mongo_client = pymongo.MongoClient(f"mongodb://localhost:27017")
    db = mongo_client.ransomware
    dataDB = db['data']

    query = {'notified': False}
    documents = dataDB.find(query)

    for document in documents:
        if document:
            id = document.get('_id', '')
            title = document.get('victim', '')
            website = document.get('website', '')
            published = document.get('published', '')
            group = document.get('group', '')

            message = f"*{title}*\n\nWebsite: {website}\nCompromised by: {group}\n\n{published}" 
            
            dataDB.update_one({'_id': id}, {'$set': {'notified': True}})

            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
    

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
    loop.close()

if __name__ == '__main__':
    main()
