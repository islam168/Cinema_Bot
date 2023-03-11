import telebot
from telebot import types
from cinematica import *


bot_token = '6091274091:AAEvPf0O0969PrgOrmokzvPouVXBgWPmpe4'

bot = telebot.TeleBot(token=bot_token)


cinemas = {
    'list': 'Вывести список кинотеатров',
    'url': 'https://kg.kinoafisha.info/bishkek/cinema/'
}

cinema = []
cinema_ids = []
movie_date = []
day_ids = []
movie_data = []
movie_ids = []


@bot.message_handler(commands=['start'])
def get_shops(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*[cinemas.get('list')])
    bot.send_message(message.chat.id, 'Здравствуйте', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_cinema(message):
    get_cinema_from_site(cinema, cinemas['url'])
    markup = types.InlineKeyboardMarkup()
    for cin in cinema:
        cinema_ids.append(cin.get('id'))
        button = types.InlineKeyboardButton(cin.get('name'),
                                            callback_data=cin.get('id'))
        markup.add(button)

    bot.send_message(message.chat.id, 'Здравствуйте, выберите кинотеатр', reply_markup=markup)


@bot.callback_query_handler(lambda query: query.data in cinema_ids)
def callback_movie_date_handler(query):
    for date in cinema:
        if date.get('id') == query.data:
            markup = types.InlineKeyboardMarkup()
            url = date.get('url')
            get_movie_date(movie_date, url)

            if not movie_date:
                text = f'Извините, в данный момент на сайте нет ближайших сеансов в кинотеатре {date.get("name")}'
                bot.send_message(query.from_user.id, text)
            else:
                text = f'Выберите дату на сеанс в кинотетре {date.get("name")}'
                for day in movie_date:
                    day_ids.append(day.get('id'))
                    button = types.InlineKeyboardButton(day.get('name'),
                                                        callback_data=day.get('id'))
                    markup.add(button)
                bot.send_message(query.from_user.id, text, reply_markup=markup)


@bot.callback_query_handler(lambda query: query.data in day_ids)
def callback_movie_date_handler(query):
    for data in movie_date:
        if data.get('id') == query.data:
            markup = types.InlineKeyboardMarkup()
            url = data.get('url')
            get_movie_data(movie_data, url)
            for movie in movie_data:
                movie_ids.append(movie.get('id'))
                button = types.InlineKeyboardButton(movie.get('name'),
                                                    callback_data=movie.get('id'))
                markup.add(button)
            bot.send_message(query.from_user.id, 'Выберите фильм', reply_markup=markup)


@bot.callback_query_handler(lambda query: query.data in movie_ids)
def callback_movie_date_handler(query):
    for movie in movie_data:
        if movie.get('id') == query.data:
            movie_name = f'*Название фильма: {movie.get("name")}*'
            movie_format = f'Форматы: {movie.get("format")}'
            bot.send_message(query.from_user.id, movie_name, parse_mode='Markdown')
            bot.send_message(query.from_user.id, movie_format)
            for time_price in movie.get('time_and_price_list'):
                time = f'Время: {time_price.get("time")}'
                price = f'Цена: {time_price.get("price")}'
                time_and_price = f'{time}   {price}'
                bot.send_message(query.from_user.id, time_and_price)


bot.infinity_polling()
