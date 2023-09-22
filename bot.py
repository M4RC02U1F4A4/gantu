import telegram
import asyncio
import logging
import os
import pymongo

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def send_message(): 
    print(TELEGRAM_API_KEY)
    telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)
    mongo_client = pymongo.MongoClient(f"mongodb://localhost:27017")
    db = mongo_client.ransomware
    dataDB = db['data']

    query = {'notified': False}
    documents = dataDB.find(query)

    for document in documents:
        if document:
            title = document.get('title', '')
            link = document.get('link', '')
            published_date = document.get('published_date', '')
            #summary = document.get('summary', '')
            message = f"Titolo: {title}\n" \
              f"Link: {link}\n" \
              f"Data di pubblicazione: {published_date}\n" 
            
            # Aggiornare stato di notifica
            dataDB.update_one({'title': title}, {'$set': {'notified': True}})

            await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


    #message_text = document
    

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
    loop.close()

if __name__ == '__main__':
    main()
