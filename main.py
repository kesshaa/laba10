import telebot;
from telebot import types;
from functools import partial;
import sqlite3;
import csv;

bot = telebot.TeleBot('6707987964:AAFbEm1PDEwevyFgkG6SU9e7a02VGNF0NyI')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Здравствуйте!")
    btn2 = types.KeyboardButton("Старт")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот, который сохраняет твои данные".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, handle_start)

def handle_start(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, text="Привет удачного дня")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/start')
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Начнём", reply_markup=markup)
        bot.register_next_step_handler(message, get_lastname)
    else:
        bot.register_next_step_handler(message, get_lastname)

def get_lastname(message):
    bot.send_message(message.chat.id, "Фамилия: ")
    bot.register_next_step_handler(message, get_firstname)

def get_firstname(message):
    lastname = message.text
    bot.send_message(message.chat.id, "Имя:")
    bot.register_next_step_handler(message, partial(get_middlename, lastname=lastname))

def get_middlename(message, lastname):
    firstname = message.text
    bot.send_message(message.chat.id, "Отчество:")
    bot.register_next_step_handler(message, partial(get_birthday, lastname=lastname, firstname=firstname))

def get_birthday(message, lastname, firstname):
    middlename = message.text
    bot.send_message(message.chat.id, "Дата ГГГГ-ММ-ДД: ")
    bot.register_next_step_handler(message, save_data, lastname, firstname, middlename)

def save_data(message, lastname, firstname, middlename):
    birthday = message.text
    userid = message.chat.id
    username = message.chat.first_name

    con = sqlite3.connect('tgbase2.db')
    cur = con.cursor()
    cur.execute(
        '''create table if not exists botsave(
        id integer primary key autoincrement,
        userid integer,
        username text,
        f text,
        i text,
        o text,
        birthday text
        )
        '''
    )
    cur.execute('''insert into botsave (userid, username, f, i , o, birthday) values (?,?,?,?,?,?)''',
                (userid, username, lastname, firstname, middlename, birthday))

    cur.execute('''select * from botsave''')
    rows = cur.fetchall()

    with open('choet.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id', 'userid', 'username', 'f', 'i', 'o', 'birthday'])
        csv_writer.writerows(rows)

    con.commit()
    con.close()
    bot.reply_to(message, "Сохранил")

if __name__ == '__main__':
    bot.polling()
