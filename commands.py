import requests
import re
import datetime
import random
import logging
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

OMDB_API_KEY = "cfb513be"
NASA_API_KEY = "RG7fdE8let4UWinLzEHPhomXaVBTqToU1EInmwhi"

def getLogMessage(update: Update):
    logMessage = "text: %s, from: %s"%(update.message.text, update.message.chat.first_name)
    return logMessage

def start(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    update.message.reply_text(
        "Hello %s, Welcome to the Bot. Please write /help to see the commands available." % update.message.chat.first_name)


def help(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    update.message.reply_text("""Available Commands :-

	/help - To show this help again

	/woof - To get an amazing dog pic, woof woof!!

	/space - To get NASA's Astronomy Pic Of the Day

	/quote - To get a random quote

	/programming_quote - To get a random programming quote

	/onThisDay - To get an event that happened today in history
	
	You can search for a movie by typing \"Movie : <Movie name or a part of it's name>\" (without \"\")""")


def unknown(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    if update.message.text.lower().find("movie") != -1:
        getMovieDetails(update, context)
    else:
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
    logger.info(getLogMessage(update))
    url = get_image_url()
    update.message.bot.send_photo(chat_id=update.message.chat.id, photo=url)


def getProgrammingQuote(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    data = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['quote'])


def getQuote(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    data = requests.get('https://api.quotable.io/random').json()
    quote = data['content']
    author = data['author']
    message = "%s - %s" % (quote, author)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def getAPOD(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + NASA_API_KEY)
    data = response.json()
    title = data['title']
    explanation = data['explanation']
    imageUrl = data['hdurl']
    copyright = data['copyright']
    message = "Title : %s\n\nExplanation : %s\n\nCopyright : %s" % (title, explanation, copyright)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=imageUrl, caption=message)


def onThisDay(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    today = datetime.datetime.now()
    date = today.strftime('%m/%d')
    url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/' + date
    data = requests.get(url).json()
    selectedEventIndex = random.randint(0, len(data['events']))
    message = "On This Day in %s - %s" % (
    data['events'][selectedEventIndex]['year'], data['events'][selectedEventIndex]['text'])
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def getMovieDetails(update: Update, context: CallbackContext):
    logger.info(getLogMessage(update))
    searchTerm = " ".join(list(update.message.text.split())[2::])
    url = 'http://www.omdbapi.com/?apikey='+OMDB_API_KEY+'&t='+searchTerm
    data = requests.get(url).json()
    caption = "Title: %s\n\nYear: %s\n\nReleased: %s\n\nRuntime: %s\n\nGenre: %s\n\nActors: %s\n\nPlot: %s\n\nIMDB Rating: %s"%(
        data['Title'], data['Year'], data['Released'], data['Runtime'], data['Genre'], data['Actors'], data['Plot'], data['Ratings'][0]['Value']
    )
    posterUrl = data['Poster']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=posterUrl, caption=caption)

