import sqlite3

class Db(object):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()

        # Create table
        self.c.execute('''CREATE TABLE titles
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title TEXT,
             created_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def select_all(self):
        self.c.fetchall()

    def insert(self, t):
        self.c.execute('''INSERT INTO titles (title) VALUES (?)''', t)