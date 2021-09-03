from telegram import update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import configparser
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('credentials.ini')
updater = Updater(token=config.get("telegram", "token"), use_context=True)
dispatcher = updater.dispatcher
logger.info("Started bot")

def start(update, context):
    logger.info(f"Recieved /start message")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    logger.info(f"Recieved message: {update.message.text}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def get_food(update, context):
    logger.info("Getting food")
    if len(context.args) > 0:
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No text passed!")

food_handler = CommandHandler('food', get_food)
dispatcher.add_handler(food_handler)

updater.start_polling()