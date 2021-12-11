# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
import re

TELEGRAM_BOT_API_KEY = "884669112:AAGbOUDAiTOXyqkeJVOD29ZWc2zpNcTrMgA"
NASA_API_KEY = "RG7fdE8let4UWinLzEHPhomXaVBTqToU1EInmwhi"

def start(update: Update, context: CallbackContext):
    print(update)
    update.message.reply_text(
        "Hello %s, Welcome to the Bot.Please write\
        /help to see the commands available."%update.message.chat.first_name)


def help(update: Update, context: CallbackContext):
    print(update)
    update.message.reply_text("""Available Commands :-
	/help - To show this help again
	/woof - To get an amazing dog pic, woof woof!!
	/space - To get NASA's Astronomy Pic Of the Day
	/quote - To get a random programming quote""")


def unknown(update: Update, context: CallbackContext):
    print(update)

    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    print(update)

    update.message.reply_text("You said '%s', but I am not sure what that means, sorry :(" % update.message.text)


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def bop(update: Update, context: CallbackContext):
    print(update)

    url = get_image_url()
    update.message.bot.send_photo(chat_id=update.message.chat.id, photo=url)

def getQuote(update: Update, context: CallbackContext):
    print(update)

    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    data = response.json()
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['quote'])

def getAPOD(update: Update, context: CallbackContext):
    print(update)

    response = requests.get('https://api.nasa.gov/planetary/apod?api_key='+NASA_API_KEY)
    data = response.json()
    title = data['title']
    explanation = data['explanation']
    imageUrl = data['hdurl']
    copyright = data['copyright']
    message = "Title : %s\n\nExplanation : %s\n\nCopyright : %s"%(title, explanation, copyright)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=imageUrl, caption=message)

def main():
    updater = Updater(TELEGRAM_BOT_API_KEY, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('woof', bop))
    updater.dispatcher.add_handler(CommandHandler('quote', getQuote))
    updater.dispatcher.add_handler(CommandHandler('space', getAPOD))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands

    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.start_polling()
    updater.idle()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
