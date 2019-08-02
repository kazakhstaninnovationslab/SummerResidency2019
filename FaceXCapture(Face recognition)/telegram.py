import telebot
import numpy as np
import pandas as pd
import csv
from telebot import types



print("Bot started...")


bot = telebot.TeleBot("969097386:AAHcd-8LI0uHU6nlRuTdBwvTCFgZgVT9MDk")

user_dict = {}





class User:

     def __init__(self, age):
          self.age = age

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
     if message.text.lower() == 'hello':
         bot.send_message(message.chat.id, 'For start using ParentAndChild bot please enter: "/start" or "/help"')
     else:
          bot.send_message(message.chat.id, 'Hello, to know status of your child , please enter the command "/mychild" and then enter your Telegram_id')




@bot.message_handler(commands = ['mychild'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hello Parent! Enter your Telegram_ID:
""")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
# pid

    chat_id = message.chat.id
    pid = message.text
    user = User(pid)
    if not pid.isdigit():
        msg = bot.reply_to(message, 'Please enter the correct Telegram_ID(only numbers)')
        bot.register_next_step_handler(msg, process_name_step)
        return
    user_dict[chat_id] = user
    bot.send_message(chat_id,'\n Your Telegram_ID is :' + str(user.age) + '\n Please wait...')


    while True:
        df_data = pd.read_csv('schooldata.csv')
        #print(df_data)
        pidint = int(pid)
        df_data = df_data[df_data["parent_id"] == pidint]
        #print(df_data)
        if not df_data.empty:
                bot.send_message(chat_id, 'Authorization success. Loading')
                #print(df_data)
                #df_data.loc[:, ['child_name']]
                if pd.isna(df_data['time']).all():
                    bot.send_message(chat_id, "Your child " + df_data['child_name'].iloc[0] + " currently is NOT in the school. ")

                else:
                    bot.send_message(chat_id, "Your child " + df_data['child_name'].iloc[0] + " currently is IN the school. Authorization time:" + df_data['time'].iloc[0])

                break
        else:
            bot.send_message(chat_id, "Your Telegram_ID is not matched in base. Try again or contact with your school administration for information. Error: 'Unmatched_ID '")
            break


bot.polling()



