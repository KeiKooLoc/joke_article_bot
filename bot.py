import logging
from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
from random import randint
import os


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


keyboard = [['/joke'],['/article']]
reply_markup = ReplyKeyboardMarkup(keyboard)

# get random url for request to api with articles
def get_url():
    api_key = os.environ.get('API_KEY')
    # tags to find articles
    tags = ['Galaxy', 'Apple', 'Sun', 'Moon', 'Nasa', 'Music',
            'Science', 'Python', 'Education']
    countries = ['gb', 'us', 'au', 'ca', 'ie', 'nz']
    endpoints = ['https://newsapi.org/v2/top-headlines?'
                 'sources=bbc-news&'
                 'pageSize=100&'
                 'language=en&'
                 'apiKey={}'.format(api_key),

                 'https://newsapi.org/v2/everything?'
                 'q={}&'
                 'pageSize=100&'
                 'language=en&'
                 'from=2019-02-06&'
                 'sortBy=popularity&'
                 'apiKey={}'.
                     format(tags[randint(0, len(tags) - 1)], api_key),

                 'https://newsapi.org/v2/top-headlines?'
                 'country={}&'
                 'pageSize=100&'
                 'language=en&'
                 'apiKey={}'.
                     format(countries[randint(0, len(countries) - 1)], api_key)
                 ]
    return endpoints[randint(0, len(endpoints) -1)]

# get random article from response
def get_article():
    endpoint = get_url()
    res = requests.get(endpoint).json()
    total = len(res['articles'])
    data = {'img_url': '', 'url': ''}
    while not data['img_url'] and not data['url']:
        article = res['articles'][randint(0, total-1)]
        data['title'] = article['title']
        data['text'] = article['content']
        data['img_url'] = article['urlToImage']
        data['url'] = article['url']
    return data


def start(bot, update):
    update.message.reply_text('I can make you laugh or tell you'
                              'something interesting, choose what you want',
                              reply_markup=reply_markup)

def joke(bot, update):
    res = requests.get('https://icanhazdadjoke.com/',
                       headers={"Accept": "application/json"})
    text = res.json()['joke']
    bot.send_message(chat_id=update.message.chat_id, text=text)


def article(bot, update):
    article = get_article()
    bot.send_message(chat_id=update.message.chat_id, text=article['title'])
    bot.send_photo(chat_id=update.message.chat_id, photo=article['img_url'])
    bot.send_message(chat_id=update.message.chat_id, text=article['text'])
    bot.send_message(chat_id=update.message.chat_id, text=article['url'])

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(token=os.environ.get('BOT_TOKEN'))
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('joke', joke))
    dp.add_handler(CommandHandler('article', article))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
