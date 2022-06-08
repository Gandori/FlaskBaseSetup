import sqlite3
import cryptocode
from os import path
from src.modules.session import delete_session

class crypt:
    def encrypt(str:str):
        return cryptocode.encrypt(str,'test')

    def decoded(str:str):
        return cryptocode.decrypt(str, 'test')

class database():
    def __init__(self) -> None:
        self.dir = path.dirname(path.abspath(__file__))
        self.file = f'{self.dir}/database.db'
        self.connect = None
        self.cursor = None
        self.crypt = crypt

    def __enter__(self):
        self.connect = sqlite3.connect(self.file)
        self.cursor = self.connect.cursor()
        return self

    def __exit__(self, *args):
        self.connect.commit()
        self.connect.close()

    def create_tables(self):
        with open(f'{self.dir}/data.sql') as f:
            self.cursor.executescript(f.read())

    def is_user_in_database(username):
        with database() as db:
            db.cursor.execute(f"select name from users where name = '{username}'")
            data = db.cursor.fetchone()
            if not data:delete_session()
            return data