from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config
import logging
import shedule as sh
from emoji import emojize
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

types = {
    1: '📢',
    2: '📝',
    3: '🔬',
    4: '☎️',
    5: '🤞',
    6: '👍',
    7: '📝',
    8: '📑',
    9: '💻',
    10: '📑'
}


command_list = {
    'start': 'start bot',
    'help': 'help',
    'номер группы': 'получение расписаия группы на сегодня'
}




def parseShedule(shedule_list):
    date = sh.get_current_date()
    group = shedule_list[0]['group']['group_name']
    text = emojize(":calendar:", use_aliases=True) + date + '\n' + group

    for i in shedule_list:
        time_begin = i['time_begin']
        time_end = i['time_end']
        subject_name = i['subject_name']
        lesson_type = i['lesson_type']['name']
        lesson_type_id = i['lesson_type']['id']
        lector = i['lector']['lector_name']
        location = i['location']
        subgroup = i['group']['subgroup']
        text = text + '\n\n' + \
               '⏰' + time_begin + ' - ' + \
               time_end + '\n' + \
               types[lesson_type_id] + subject_name + ' (' + lesson_type + ')' + '\n' + \
               '🎓' + lector + '\n' + \
               '📍' + location

        if subgroup != None:
            text = text + '\n' + '🔸️Подгруппа ' + subgroup

    return text


def start_command(bot, update):
    # database.write(update.message)
    bot.send_message(chat_id=update.message.chat_id, text='Введите номер группы')


def help_command(bot, update):
    text = ''
    for key, value in command_list.items():
        text = text + '/' + key + ' – ' + value + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=text)


def text_message(bot, update):
    try:
        id = sh.getIdGroup(update.message.text)
        shedule_group = parseShedule(sh.get_shedule_group_current_day(id))

        bot.send_message(chat_id=update.message.chat_id, text=shedule_group)
    except:
        bot.send_message(chat_id=update.message.chat_id, text='Группа не найдена или нет занятий на сегодня')



def start(bot, update):
    print(update.message)
    chat = update.message['chat']
    print(chat)
    print(chat['username'])
    print(chat['first_name'])
    keyboard = []
    keyboard.append([InlineKeyboardButton(u'11', callback_data='1')])
    keyboard.append([InlineKeyboardButton(u'22', callback_data='2')])
    keyboard.append([InlineKeyboardButton(u'33', callback_data='3')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)



def button(bot, update):
    query = update.callback_query
    keyboard = [[KeyboardButton('button1'), KeyboardButton('button2')]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    handlerDataCallback(bot, query)

    # bot.send_message(query.message.chat_id, 'Some text', reply_markup=reply_markup)


def handlerDataCallback(bot, query):
    if query.data == '1':
        keyboard = [[KeyboardButton('button1'), KeyboardButton('button2')]]
        bot.send_message(query.message.chat_id, 'text', reply_markup=ReplyKeyboardMarkup(keyboard, 10))
    if query.data == '2':
        keyboard = [[KeyboardButton('button3'), KeyboardButton('button4')]]
        bot.send_message(query.message.chat_id, 'text', reply_markup=ReplyKeyboardMarkup(keyboard, 10))
    if query.data == '3':
        keyboard = [[KeyboardButton('button6')]]
        bot.send_message(query.message.chat_id, 'text', reply_markup=ReplyKeyboardMarkup(keyboard, 10))


def main():
    updater = Updater(token=config.TOKEN)
    dispatcher = updater.dispatcher

    # Хендлеры
    start_command_handler = CommandHandler('start', start_command)
    text_message_handler = MessageHandler(Filters.text, text_message)
    help_command_handler = CommandHandler('help', help_command)

    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    dispatcher.add_handler(help_command_handler)
    # dispatcher.add_handler(CallbackQueryHandler(button))
    # dispatcher.add_handler(CommandHandler('start_new', start))

    # Начинаем поиск обновлений
    updater.start_polling(clean=True)

    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()
