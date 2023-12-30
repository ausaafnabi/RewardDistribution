import os
import logging
import time
from dotenv import load_dotenv

import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import *
 

load_dotenv()

TOKEN = os.environ['BOT_TOKEN']

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info('Starting a bot....')
     
async def start_commmand(update, context):
    await update.message.reply_text('Hello! Always happy to provide you with Reward Distribution Report')

async def notify_stats(update, context):
    message = "Your Daily Report\n\n..." 
    # to call report generation function and format results appropriately.
    await update.message.reply_text(message)

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler('start', start_commmand))
    application.add_handler(CommandHandler('report', notify_stats))

    # Run bot
    application.run_polling(1.0)