# -*- coding: utf-8 -*-
import requests
import datetime
import pandas as pd
import telebot


class abs_bot():

    def __init__(self, token):
        self.api_url = "https://api.telegram.org/bot" + token + "/"
        self.token = token

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        # print (result_json)
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def forward_message(self, chat_id, from_id, mess_id):
        params = {'chat_id': chat_id, 'from_chat_id': from_id, 'message_id': mess_id}
        method = 'forward_message'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
            return last_update


token = ""
bot = abs_bot(token)
data = pd.read_excel("greetings.xlsx")
now = datetime.datetime.now()
admission_id = ''
bot2 = telebot.TeleBot(token)


# print((data[data['Greetings'] == 'привет']).count()[0])

def main():
    new_offset = None
    hour = now.hour

    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        if (type(last_update) == type({}) and ('message' in last_update or 'callback_query' in last_update)):
            last_update_id = last_update['update_id']

            if ('callback_query' in last_update):
                callback_query = last_update['callback_query']
                from_id = last_update['callback_query']['from']['id']

                # print(callback_query)

                callback_data = callback_query['data']

                if (callback_data == 'поступление'):
                    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                    button = telebot.types.InlineKeyboardButton(text='Как поступить на грант',
                                                                callback_data='как поступить на грант')
                    button2 = telebot.types.InlineKeyboardButton(text='Cписок обязательных документов',
                                                                 callback_data='список обязательных документов')
                    markup.add(button)
                    markup.add(button2)

                    bot2.send_message(chat_id=from_id,
                                      text='Вопросы о поступении', reply_markup=markup)
                elif (callback_data == 'студентам'):
                    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                    button3 = telebot.types.InlineKeyboardButton(text='Учебный процесс',
                                                                 callback_data='как поступить на грант')
                    button4 = telebot.types.InlineKeyboardButton(text='Дом студентов',
                                                                 callback_data='список обязательных документов')
                    markup.add(button3)
                    markup.add(button4)

                    bot2.send_message(chat_id=from_id,
                                      text='Часто задаваемые вопросы', reply_markup=markup)
                else:
                    questions = pd.read_excel("questions.xlsx")
                    questions = questions[questions['Questions'] == callback_data]
                    if (questions.count()[0] >= 1):
                        answer = questions.iloc[0]['Answers']
                        bot.send_message(from_id, answer)


            else:
                las


t_chat_id = last_update['message']['chat']['id']
last_mess_id = last_update['message']['message_id']
if ('text' in last_update['message']):
    last_chat_text = last_update['message']['text']
    last_chat_name = last_update['message']['chat']['first_name']
    mess = last_chat_text.lower()
    questions = pd.read_excel("questions.xlsx")
    questions = questions[questions['Questions'] == mess]
    gr = data[data['Greetings'] == mess].count()[0] >= 1

    if (gr and 6 <= hour < 12):
        bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))


    elif (gr and 12 <= hour < 17):
        bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))

    elif (gr and 17 <= hour <= 23):
        bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))

    elif (gr and hour < 6):
        bot.send_message(last_chat_id, 'Доброй ночи, {}'.format(last_chat_name))

    elif (questions.count()[0] >= 1):
        answer = questions.iloc[0]['Answers']
        bot.send_message(last_chat_id, answer)

    elif (mess == 'data'):
        bot.send_message(last_chat_id, 'Доброй ночи, {}'.format(last_chat_name))


    elif (mess == '/help' or mess == '/start'):

        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        button = telebot.types.InlineKeyboardButton(text='Поступающим',
                                                    callback_data='поступление')

        button1 = telebot.types.InlineKeyboardButton(text='Студентам',
                                                     callback_data='студентам')
        markup.add(button)
        markup.add(button1)

        bot2.send_message(chat_id=last_chat_id,
                          text='Отправьте боту вопрос и он ответит на него', reply_markup=markup)

    else:

        bot2.forward_message(admission_id, last_chat_id, last_mess_id)

else:

    bot2.forward_message(admission_id, last_chat_id, last_mess_id)

new_offset = last_update_id + 1

if name == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

