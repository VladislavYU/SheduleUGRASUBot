import sqlite3

base = sqlite3.connect('database.db', check_same_thread=False)

def write(message):
    chat = message['chat']
    login = chat['username']
    first_name = chat['first_name']
    last_name = chat['last_name']
    chat_id = chat['id']
    cursor = base.cursor()
    sql = f"""insert into User(chat_id, first_name, last_name, login) values{chat_id, first_name, last_name, login}"""
    cursor.execute(sql)
    base.commit()
    base.close()


def write_message(message):
    chat = message['chat']
    chat_id = chat['chat_id']
    cursor = base.cursor()
    sql = f"""select * from User where chat_id = {chat_id}"""

    cursor = base.cursor()
    cursor.execute(sql)

    sql = f"""insert into Message(text, chat_id) values{text, chat_id}"""
    cursor.execute(sql)
    base.commit()
    base.close()

