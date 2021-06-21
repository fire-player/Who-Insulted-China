import requests
from bs4 import BeautifulSoup
import logging
from random import randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
}

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

page = requests.get('https://duckduckgo.com/html/?q=%E8%BE%B1%E8%8F%AF&t=ffab&df=d', headers=headers).text
soup = BeautifulSoup(page, 'html.parser').find_all("a", class_="result__snippet", text=True)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Type /who to check who insulted China today!')


def updateData():
    global today
    global tomorrow
    global page
    global soup
    if today >= tomorrow:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        page = requests.get('https://duckduckgo.com/html/?q=%E8%BE%B1%E8%8F%AF&t=ffab&df=d', headers=headers).text
        soup = BeautifulSoup(page, 'html.parser').find_all("a", class_="result__snippet", text=True)
    return


def who(update, context):
    '''Return a random result from the page.'''
    updateData()

    update.message.reply_text(soup[randint(0, len(soup))].text)
    print("Someone called this bot.")
    print(today)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    TOKEN = "Your token here!"
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("who", who))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
