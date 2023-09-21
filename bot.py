import telegram
import asyncio
import logging
import os

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def send_message():
    telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)
    message_text = 'TEST'
    await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message_text)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
    loop.close()

if __name__ == '__main__':
    main()