from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config, re
import logging
import datetime
import schedule as sh
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




def parseschedule(schedule_list):
    date = sh.get_current_date()
    group = schedule_list[0]['group']['group_name']
    text = emojize(":calendar:", use_aliases=True) + date + '\n' + group

    for i in schedule_list:
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


def get_schedule_week_after(schedule):
    week = []
    today = datetime.date.today()
    week.append(today)
    timetable = {}
    for i in range(1,6):
        week.append(today + datetime.timedelta(days=i))

    for day in week:
        for key, value in schedule.items():
            if key == str(day):
                timetable[key] = value
                break

    text = ''

    for day, schedule in timetable.items():
        text = text + '\n' + emojize(":calendar:", use_aliases=True) + day + '\n'
        for i in schedule:
            time_begin = i['time_begin']
            time_end = i['time_end']
            subject_name = i['subject_name']
            lesson_type = i['lesson_type']['name']
            lesson_type_id = i['lesson_type']['id']
            lector = i['lector']['lector_name']
            location = i['location']
            subgroup = i['group']['subgroup']
            text = text + '\n' + \
                   '⏰' + time_begin + ' - ' + \
                   time_end + '\n' + \
                   types[lesson_type_id] + subject_name + ' (' + lesson_type + ')' + '\n' + \
                   '🎓' + lector + '\n' + \
                   '📍' + location

            if subgroup != None:
                text = text + '\n' + '🔸️Подгруппа ' + subgroup

            text = text + '\n'

    return text


def get_schedule_week_before(schedule):
    week = []
    today = datetime.date.today()
    week.append(today)
    timetable = {}
    for i in range(1,6):
        week.append(today + datetime.timedelta(days=-i))

    for day in week:
        for key, value in schedule.items():
            if key == str(day):
                timetable[key] = value
                break

    text = ''

    for day, schedule in timetable.items():
        text = text + '\n' + emojize(":calendar:", use_aliases=True) + day + '\n'
        for i in schedule:
            time_begin = i['time_begin']
            time_end = i['time_end']
            subject_name = i['subject_name']
            lesson_type = i['lesson_type']['name']
            lesson_type_id = i['lesson_type']['id']
            lector = i['lector']['lector_name']
            location = i['location']
            subgroup = i['group']['subgroup']
            text = text + '\n' + \
                   '⏰' + time_begin + ' - ' + \
                   time_end + '\n' + \
                   types[lesson_type_id] + subject_name + ' (' + lesson_type + ')' + '\n' + \
                   '🎓' + lector + '\n' + \
                   '📍' + location

            if subgroup != None:
                text = text + '\n' + '🔸️Подгруппа ' + subgroup + '\n'
            text = text + '\n'

    return text

def text_message(bot, update):
    try:
        id = sh.getIdGroup(update.message.text)

        keyboard = []
        keyboard.append([InlineKeyboardButton(u'Расписание на неделю вперед', callback_data=f'week_after {id}')])
        keyboard.append([InlineKeyboardButton(u'Расписание на неделю назад', callback_data=f'week_before {id}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        # schedule_group = sh.get_schedule_group(id)

        shed = sh.get_schedule_group(id)
        date = datetime.date.today()
        scheduleCurrentDay = shed.get(str(date))

        if scheduleCurrentDay == None:
            update.message.reply_text('Занятий на сегодня нет', reply_markup=reply_markup)
        else:
            schedule_group = parseschedule(scheduleCurrentDay)
            update.message.reply_text(schedule_group, reply_markup=reply_markup)

    except:
        bot.send_message(chat_id=update.message.chat_id, text='Группа не найдена')



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
    start = re.split(r' ', query.data)

    if start[0] == 'week_after':
        msg = get_schedule_week_after(sh.get_schedule_group(start[1]))
        bot.send_message(chat_id=query.message.chat.id, text=msg)

    if start[0] == 'week_before':
        msg = get_schedule_week_before(sh.get_schedule_group(start[1]))
        bot.send_message(chat_id=query.message.chat_id, text=msg)

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
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('start_new', start))

    # Начинаем поиск обновлений
    updater.start_polling(clean=True)

    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()
