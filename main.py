import telebot
from time import sleep
import threading
from telebot import types

token='TOKEN'
bot=telebot.TeleBot(token)
user_data={}
languages=['RU','EN']
messages={
    "greeting":
        {
            'RU':'Здравствуй Я твой бот для поддержания баланса воды\nЧтобы сменить язык\nиспользуй - /language,\nЧтобы увидеть списко доступных комманд используй - /help',
            'EN':'Hello I am your water balance bot.\nTo change language use - /language,\nto see available commands use /help'
        },
    "help":
        {
            'RU':'Список доступных комманд:\n/start - комманда приветствия,\n/help - показывает все команды,\n/language - смена языка,\n/manual - обьясняет как использовать бота',
            'EN':'List of available commands:\n/start - greetings command,\n/help - shows all available commands,\n/language - changes language,\n/manual - explains how to use bot'
        },

    "manual":
        {
            'RU':'Чтобы посмотреть сколько воды\nнужно выпить сегодня используйте - /status,\nЧтобы поставить напоминанаие\nвыпить воду используйте -/set_reminder [часы],\nЧтобы поставить цель\nпотребления воды используйте -/set_goal [обЪем(мл)],\nЧтобы отметить выпитую вами\nводу используйте - /drink [обЪем(мл)]',
            'EN':'To see how much water\nyou need to drink today use - /status,\nTo set reminder\nto drink water use - /set_reminder [hours],\nTo mark you\ndrank water - /drink [volume(ml)],\nTo set required amount\nof water per day - /set_goal [volume(ml)]'
        },
    "language":
        {
            'EN':'Choose language',
            'RU':'Выберете язык'
        },
    "status":
        {
            'EN':'You need to drink:',
            'RU':'Тебе надо выпить:'
        },
    "null":
        {
            'EN':'You completed goal for today uwu',
            'RU':'Ты выполнил цель на сегодня uwu'
        },
    "goal":
        {
            'EN':'\u2705Done now your goal is:',
            'RU':'\u2705Готово ваша цель теперь:'

        },
    "goal_error":
        {
            'EN':'\u274COopsie you forgot to input valid number',
            'RU':'\u274CОшибочка вы забыли ввести число'
        },
    "reminder":
        {
            'EN':f'\u2705Done now you will get notification in',
            'RU':f'\u2705Готово вы получите напоминание через'
        },
    "reminder_hours":
        {
            'EN':'h.',
            'RU':'ч.'
        },
    "reminder_error":
        {
            'EN':'\u274COopsie you forgot to input valid time',
            'RU':'\u274CОшибочка вы забыли ввести время'
        },
    "drink":
        {
            'EN':'\u2764\ufe0fWell Done\u2764\ufe0f',
            'RU':'\u2764\ufe0fМолодчик\u2764\ufe0f'
        },
    "drink_error":
        {
            'EN':'\u274COopsie you forgot to input amount of water you drank',
            'RU':'\u274CОшибочка вы забыли ввести количество воды которые вы выпили'
        },
    "notification":
        {
            'EN':'Please drink some water',
            'RU':'Пожалуйста выпейте немного воды'
        }
          }

def notification(message):
    while True:
        try:
            sleep(user_data[message.chat.id]['time']*3600)
            try:
                l = user_data[message.chat.id]['language']
                text=messages['notification'][l]
                bot.send_message(message.chat.id, text)
            except KeyError:
                l = 'EN'
                text = messages['notification'][l]
                bot.send_message(message.chat.id, text)
        except KeyError:
            sleep(3600)
            try:
                l = user_data[message.chat.id]['language']
                text = messages['notification'][l]
                bot.send_message(message.chat.id, text)
            except KeyError:
                l = 'EN'
                text = messages['notification'][l]
                bot.send_message(message.chat.id, text)
        print(user_data)

@bot.message_handler(commands=['start'])
def start_msg(message):
    try:
        l = user_data[message.chat.id]['language']
        text = messages["greeting"][l]
        bot.send_message(message.chat.id, text)
    except KeyError:
        text = messages["greeting"]['EN']
        bot.send_message(message.chat.id, text)
    threading.Thread(target=notification,args=(message,), daemon=True).start()

@bot.message_handler(commands=['language'])
def language_msg(message):

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(languages)):
        markup.add(languages[i])
    try:
        l = user_data[message.chat.id]['language']
        text = messages["language"][l]
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except KeyError:
        text = messages["language"]['EN']
        bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_msg(message):
    try:
        l = user_data[message.chat.id]['language']
        text = messages["help"][l]
        bot.send_message(message.chat.id, text)
    except KeyError:
        text = messages["help"]['EN']
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['manual'])
def manual_msg(message):
    try:
        l = user_data[message.chat.id]['language']
        text = messages["manual"][l]
        bot.send_message(message.chat.id, text)
    except KeyError:
        text = messages["manual"]['EN']
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['status'])
def status_msg(message):
    try:
        l = user_data[message.chat.id]['language']

        try:
            water = user_data[message.chat.id]['goal']
        except KeyError:
            user_data[message.chat.id] = {}
            user_data[message.chat.id]['goal']=2000
            water = 2000
        try:
            drank=user_data[message.chat.id]['drank']
        except KeyError:
            user_data[message.chat.id] = {}
            user_data[message.chat.id]['drank']=0
            drank=0
        status=int(water)-int(drank)
        if status<=0:
            text = messages["null"][l]
            bot.send_message(message.chat.id, f'{text}')
        else:
            text= messages["status"][l]
            bot.send_message(message.chat.id, f'{text} {status} ml')
    except KeyError:
        try:
            water = user_data[message.chat.id]['goal']
        except KeyError:
            user_data[message.chat.id]={}
            user_data[message.chat.id]['goal'] = 2000
            water = 2000
        try:
            drank=user_data[message.chat.id]['drank']
        except KeyError:
            user_data[message.chat.id] = {}
            user_data[message.chat.id]['drank'] = 0
            drank=0
        status=int(water)-int(drank)
        if status<=0:
            text = messages["null"]['EN']
            bot.send_message(message.chat.id, f'{text}')
        else:
            text= messages["status"]['EN']
            bot.send_message(message.chat.id, f'{text} {status} ml')

@bot.message_handler(commands=['set_goal'])
def set_goal_msg(message):
    try:
        l = user_data[message.chat.id]['language']
        try:
            x,water=message.text.split()
            user_data[message.chat.id]['goal']=int(water)
            text=messages['goal'][l]
            bot.send_message(message.chat.id,f'{text} {water} ml')
        except ValueError:

            text=messages['goal_error'][l]
            bot.send_message(message.chat.id,text)
    except KeyError:
        try:

            x,water=message.text.split()
            try:
                user_data[message.chat.id]['goal']=int(water)
            except KeyError:
                user_data[message.chat.id] = {}
                user_data[message.chat.id]['goal'] = int(water)
            text=messages['goal']['EN']
            bot.send_message(message.chat.id,f'{text} {water} ml')
        except ValueError:
            text=messages['goal_error']['EN']
            bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['set_reminder'])
def set_reminder_msg(message):
    try:
        l = user_data[message.chat.id]['language']
        try:
            x,reminder=message.text.split()
            user_data[message.chat.id]['time']=int(reminder)
            text = messages['reminder'][l]
            after_text=messages['reminder_hours'][l]
            bot.send_message(message.chat.id, f'{text} {reminder} {after_text}')

        except ValueError:
            text = messages['reminder_error'][l]
            bot.send_message(message.chat.id, text)
    except KeyError:
        try:

            x,reminder=message.text.split()
            try:
                user_data[message.chat.id]['time']=int(reminder)
            except KeyError:
                user_data[message.chat.id] = {}
                user_data[message.chat.id]['time'] = int(reminder)
            text = messages['reminder']["EN"]
            after_text = messages['reminder_hours']["EN"]
            bot.send_message(message.chat.id, f'{text} {reminder} {after_text}')
        except ValueError:
            text = messages['reminder_error']['EN']
            bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['drink'])
def drink_msg(message):
    try:
        l = user_data[message.chat.id]['language']
        try:
            x,drink=message.text.split()
            try:
                user_data[message.chat.id]['drank']+= int(drink)
            except KeyError:
                user_data[message.chat.id]['drank']=0
            text=messages['drank'][l]
            bot.send_message(message.chat.id,f'{text} {drink} ml')
        except ValueError:
            text = messages['drink_error'][l]
            bot.send_message(message.chat.id,text)
    except KeyError:
        l='EN'
        try:
            x,drink=message.text.split()
            try:
                user_data[message.chat.id]['drank']+= int(drink)
            except KeyError:
                try:
                    user_data[message.chat.id]['drank']=0
                except KeyError:
                    user_data[message.chat.id]={}
                    user_data[message.chat.id]['drank'] = 0

            text=messages['drink'][l]
            bot.send_message(message.chat.id,f'{text} {drink} ml')
        except ValueError:
            text = messages['drink_error'][l]
            bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=["text"])
def text_msg(message):
    if message.text in languages:

        language = message.text
        bot.send_message(message.chat.id, "\u2705")

        try:
            user_data[message.chat.id]['language'] = language
        except KeyError:
            user_data[message.chat.id]={}
            user_data[message.chat.id]['language'] = language
    if message.text not in languages:
        bot.send_message(message.chat.id, "\u274C")

bot.polling()
