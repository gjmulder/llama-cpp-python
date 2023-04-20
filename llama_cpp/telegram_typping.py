import logging
import asyncio
import aiohttp
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def start(update, context):
    update.message.reply_text("Hi! Type /simulate to simulate the bot typing.")
    logging.info("User %s started the bot", update.message.from_user.id)

async def simulate(update, context):
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    logging.info("Bot is typing a response...")

    url = 'https://httpbin.org/get'
    logging.info("Fetching API response from %s", url)

    loop = asyncio.get_event_loop()
    response_text = await fetch(url)

    update.message.reply_text("API response received: " + response_text)
    logging.info("Sent response to user %s", update.message.from_user.id)

def stop(update, context):
    update.message.reply_text("Stopping the bot...")
    logging.info("User %s stopped the bot", update.message.from_user.id)
    context.bot.stop()

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("simulate", simulate))
    dp.add_handler(CommandHandler("stop", stop))

    updater.start_polling()
    logging.info("Bot started polling for updates...")
    updater.bot.send_message(chat_id="@YOUR_CHANNEL_ID", text="Bot started.")
    updater.idle()
    updater.bot.send_message(chat_id="@YOUR_CHANNEL_ID", text="Bot stopped.")
    logging.info("Bot stopped polling for updates.")

if __name__ == "__main__":
    asyncio.run(main())
