import sqlite3


def initialize():
    con = sqlite3.connect('reminder.db')
    c = con.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS reminder
                        (id INTEGER PRIMARY KEY, text TEXT)''')

    con.commit()
    con.close()

def get_reminders():
    con = sqlite3.connect('reminder.db')
    c = con.cursor()

    reminders = list(map(lambda row: (row[0], row[1]),
                         c.execute('SELECT * FROM reminder').fetchall()))

    con.commit()
    con.close()
    return reminders


def save_new_reminder(text):
    con = sqlite3.connect('reminder.db')
    c = con.cursor()

    c.execute('''INSERT INTO reminder (text) VALUES (?)''', (text,))

    con.commit()
    con.close()
