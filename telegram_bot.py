import configparser
import logging
import re

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from notion_client import CustomNotionClient
class FoodBot():
    def __init__(self) -> None:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        config = configparser.ConfigParser()
        config.read('credentials.ini')
        self.updater = Updater(token=config.get("telegram", "token"), use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.notion_client = CustomNotionClient()

        food_handler = MessageHandler(Filters.regex(re.compile('^food$|^essen$', re.IGNORECASE)), self.get_food)
        self.dispatcher.add_handler(food_handler)

        self.updater.start_polling()

        self.logger.info("Started bot")

    def get_food(self, update, context):
        self.logger.info("Getting food")
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.notion_client.get_names_of_available_products())

if __name__ == '__main__':
    food_bot = FoodBot()