import sqlite3

class Model:
    def __init__(self):
        self.conn = sqlite3.connect('database/service.db')