import sqlite3

base = sqlite3.connect('database.db')

def write(chat_id):
    cursor = base.cursor()
    sql = f"""insert into User(chat_id) values({chat_id})"""
    cursor.execute(sql)
    base.commit()
    base.close()


def write_group(chat_id, text):
    cursor = base.cursor()
    sql = f"""insert into Message(text, chat_id) values({text}, {chat_id})"""
    cursor.execute(sql)
    base.commit()
    base.close()


write_group(12323, '3552')