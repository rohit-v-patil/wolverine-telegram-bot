
import logging
from telegram.ext.updater import Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import commands

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_API_KEY = "884669112:AAGbOUDAiTOXyqkeJVOD29ZWc2zpNcTrMgA"


def main():
    updater = Updater(TELEGRAM_BOT_API_KEY, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', commands.start))
    updater.dispatcher.add_handler(CommandHandler('help', commands.help))
    updater.dispatcher.add_handler(CommandHandler('woof', commands.bop))
    updater.dispatcher.add_handler(CommandHandler('programming_quote', commands.getProgrammingQuote))
    updater.dispatcher.add_handler(CommandHandler('quote', commands.getQuote))
    updater.dispatcher.add_handler(CommandHandler('space', commands.getAPOD))
    updater.dispatcher.add_handler(CommandHandler('onThisDay', commands.onThisDay))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, commands.unknown))  # Filters out unknown commands

    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, commands.unknown_text))

    updater.start_polling()
    logger.info('Started....')
    updater.idle()


if __name__ == '__main__':
    main()
