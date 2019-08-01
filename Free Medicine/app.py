from flask import Flask, request
import telebot
from telebot import types
import os
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


TOKEN = '832334217:AAEEcz7EiP-3j2NxqeiCf-gNAkB5YPE9TTs'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
server.config.from_object(os.environ['APP_SETTINGS'])
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

from models import *

buttons = {"category": "Выбрать по категории",
           "code": "Выбрать по коду мкб-10"}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(buttons["category"], callback_data=buttons["category"]))
    #markup.add(types.InlineKeyboardButton(buttons["code"], callback_data=buttons["code"]))
    bot.send_message(message.chat.id, "Доступны следующие методы поиска.", reply_markup=markup)

#
# @bot.callback_query_handler(func=lambda call: call.data == buttons["code"])
# def find_by_code(call):
#     markup = types.ForceReply(selective=False)
#     code = bot.send_message(call.message.chat.id, "Введите код.", reply_markup=markup)
#     diseases = (db.session.query(Disease.name.distinct()).filter(code.in_(Disease.code))).all()
#     dis_markup = types.ReplyKeyboardMarkup()
#     for c in diseases:
#         button = types.KeyboardButton(text=c.name)
#         dis_markup.add(button)
#     msg = bot.send_message(call.message.chat.id, "Выберите заболевание", reply_markup=markup)
#     #bot.register_next_step_handler(msg, choose_category)


@bot.callback_query_handler(func=lambda call: call.data == buttons["category"])
def choose_people_category(call):
    markup = types.ReplyKeyboardMarkup()
    categories = db.session.query(PeopleCategory).all()
    for c in categories:
        button = types.KeyboardButton(text=c.name)
        markup.add(button)
    msg = bot.send_message(call.message.chat.id, "Выберите категорию людей к которой относитесь:", reply_markup=markup)
    bot.register_next_step_handler(msg, choose_category)


def choose_category(message):
    markup = types.ReplyKeyboardMarkup()
    people_category = PeopleCategory.query.filter_by(name=message.text).first()
    categories = db.session.query(Category).all()
    for c in categories:
        button = types.KeyboardButton(text=c.name)
        markup.add(button)
    msg = bot.send_message(message.chat.id, "Выберите категорию заболевания:", reply_markup=markup)
    bot.register_next_step_handler(msg, choose_disease, people_category)


def choose_disease(message, people_category):
    markup = types.ReplyKeyboardMarkup()
    category = Category.query.filter_by(name=message.text).first()
    dis_people_id = DiseaseCategory.query.filter_by(category_id=people_category.id).all()
    names = (db.session.query(Disease.name.distinct())
             .filter((Disease.category_id == category.id)
                     & (Disease.id.in_([dis.disease_id for dis in dis_people_id])))).all()
    if len(names) > 1:
        for c in names:
            button = types.KeyboardButton(text=c[0])
            markup.add(button)
        msg = bot.send_message(message.chat.id, "Выберите заболевание:", reply_markup=markup)
        bot.register_next_step_handler(msg, choose_stage)
    else:
        bot.reply_to(message, 'К сожалению по данным параметрам ничего не найдено!')


def choose_stage(message):
    markup = types.ReplyKeyboardMarkup()
    dis = Disease.query.filter_by(name=message.text).first()
    dis_stages = DiseaseStage.query.filter_by(disease_id=dis.id).all()
    stages = db.session.query(Stage).filter(Stage.id.in_([d.stage_id for d in dis_stages])).all()
    stages_names = ''
    i = 0
    for s in stages:
        stages_names += str(i) + '. ' + s.name + '\n'
        i = i+1
    bot.send_message(message.chat.id, stages_names)
    markup.add(*[types.KeyboardButton(str(button)) for button in range(len(stages))])
    msg = bot.send_message(message.chat.id, "Выберите номер ваших показаний", reply_markup=markup)
    bot.register_next_step_handler(msg, show_medicine, dis, stages)


def show_medicine(message, disease, stages):
    stage = stages[int(message.text)]
    #stage = Stage.query.filter(Stage.name.startswith(message.text)).first()
    disease_stage = db.session.query(DiseaseStage)\
        .filter((DiseaseStage.stage_id == stage.id) & (DiseaseStage.disease_id == disease.id)).first()
    medicine = Medicine.query.filter_by(disease_stage_id=disease_stage.id).all()
    str = ''
    for i in medicine:
        str += i.name + '\t' + i.form + '\n'
    bot.send_message(message.chat.id, str)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://freemedicine.herokuapp.com/' + TOKEN)
    #bot.polling()
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))