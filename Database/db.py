import sqlite3

class Db(object):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()

        # Create table
        self.c.execute('''CREATE TABLE drawings
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             content TEXT,
             created_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def select_all(self):
        self.c.execute("SELECT * FROM drawings")
        return self.c.fetchall()

    def insert(self, t):
        return self.c.execute('''INSERT INTO drawings (content) VALUES (?)''', t)

    def last(self):
        self.c.execute('''\
        SELECT id, content, created_date
        FROM drawings
        ORDER BY id DESC
        LIMIT 1''')
        return self.c.fetchone()