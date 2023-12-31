# import asyncio
# import logging

# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# from telegram.ext.jobqueue import JobQueue

import os
import logging
import time
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
 
from contract import generate_report

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.WARNING,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

logger.info('Starting a bot....')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Always happy to provide you with Reward Distribution Report! \nUse /start to turn on the service, and /stop to shut it down!")


async def report(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.chat_id, text=generate_report())


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(report,3600*4, chat_id=chat_id, name=str(chat_id))

        text = "Thanks, Always happy to provide you with Reward Distribution Report! I will keep you updated every 4 hours!"
        if job_removed:
            text += "The service is shut down!!."
        await update.effective_message.reply_text(text)

    except (IndexError):
        await update.effective_message.reply_text("Oops, an unexpected error occured!")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Stopped the service successfully!" if job_removed else "You have no active service running."
    await update.message.reply_text(text)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()