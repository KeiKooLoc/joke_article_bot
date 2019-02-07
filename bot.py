import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
from random import randint
import os


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
api_key = os.eniron.get('API_KEY')


# get random url for request to api with articles
def get_url():
    # tags to find random articles
    tags = ['Galaxy', 'Apple', 'Sun', 'Moon', 'Nasa', 'Music', 
            'Science', 'Python', 'Education', 'Sport', 'Medicine',
            'War']
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
                     format(tags[randint(0, len(tags) - 1)],
                            api_key),

                 'https://newsapi.org/v2/top-headlines?'
                 'country={}&'
                 'pageSize=100&'
                 'language=en&'
                 'apiKey={}'.
                     format(countries[randint(0, len(countries) - 1)],
                            api_key)
                 ]
    return endpoints[randint(0, len(endpoints) -1)]


# get random article from response
def get_article(tag=None):
    endpoint = get_url()
    if tag:
        endpoint = 'https://newsapi.org/v2/everything?' \
                   'q={}&' \
                   'pageSize=100&' \
                   'language=en&' \
                   'sortBy=relevancy&' \
                   'apiKey={}'.format(tag, api_key)
    res = requests.get(endpoint).json()
    total = len(res['articles'])
    if total == 0 or res['status'] == 'error':
        return "I can't find anything, try another tag"
    data = {'title': '',
            'text': '',
            'img_url': '',
            'url': ''}
    while not data['title'] and not data['text'] \
            and not data['img_url'] and not data['url']:
        article = res['articles'][randint(0, total-1)]
        data['title'] = article['title']
        data['text'] = article['description']
        data['img_url'] = article['urlToImage']
        data['url'] = article['url']
    return data


keyboard = [['/joke'],['/article']]
reply_markup = ReplyKeyboardMarkup(keyboard)


def start(bot, update):
    update.message.reply_text('I can make you laugh or tell you '
                              'something interesting, choose what you want. '
                              'You can also find an article by tag. '
                              'Just add your tag to /article command '
                              'For example: /article nasa news',
                              reply_markup=reply_markup)


def joke(bot, update):
    res = requests.get('https://icanhazdadjoke.com/',
                       headers={"Accept": "application/json"}).json()
    bot.send_message(chat_id=update.message.chat_id, text=res['joke'])


def article(bot, update, args):
    if len(args) == 0:
        article = get_article()
    else:
        article = get_article(' '.join(args))
    if type(article) == str:
        bot.send_message(chat_id=update.message.chat_id, text=article)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=article['title'])
        bot.send_photo(chat_id=update.message.chat_id, photo=article['img_url'])
        bot.send_message(chat_id=update.message.chat_id, text=article['text'])
        bot.send_message(chat_id=update.message.chat_id, text=article['url'])


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command."
                          "Send /article or /joke or /article "
                          "with your tag after.")


def main():
    updater = Updater(token=os.environ.get('BOT_TOKEN'))
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('joke', joke))
    dp.add_handler(CommandHandler('article', article, pass_args=True))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
