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
    
    def valid_password(username, pwd):
        with database() as db:
            db.cursor.execute(f"select password from users where name='{username}' and password='{pwd}'")
            return db.cursor.fetchone()

    def set_user_online(username):
        with database() as db:
            db.cursor.execute(f"update users set status = 'online' where name = '{username}'")

    def set_all_user_offline():
        with database() as db:
            db.cursor.execute("select name from users")
            for user in db.cursor.fetchall():
                db.cursor.execute(f"update users set status = 'offline' where name = '{user[0]}'")

    def set_chatpartner(username, chatpartner):
        with database() as db:
            db.cursor.execute(f"select user1 from currentchatpartner where user1 = '{username}'")
            if db.cursor.fetchone():
                db.cursor.execute(f"update currentchatpartner set user2 = '{chatpartner}' where user1 = '{username}'")
            else:
                db.cursor.execute(f"insert into currentchatpartner values('{username}', '{chatpartner}')")

    def get_chatpartner(username):
        with database() as db:
            db.cursor.execute(f"select user2 from currentchatpartner where user1 = '{username}'")
            data = db.cursor.fetchone()
            if data :
                return data[0]

    def set_profile_img(username, img):
        with database() as db:
            db.cursor.execute(f"select img from users where name = '{username}'")
            db.cursor.execute(f"update users set img = '{img}' where name = '{username}'")

    def get_profile_img(username):
        with database() as db:
            db.cursor.execute(f"select img from users where name = '{username}'")
            data = db.cursor.fetchone()
            if data:
                return data[0]

    def add_message(username, chatpartner, message, ):
        with database() as db:
            db.cursor.execute(f"select * from chats")
            data = db.cursor.fetchall()
            message_id = len(data)
            db.cursor.execute(f"insert into chats values('{message_id}', '{username}', '{chatpartner}', '{message}')")

    def get_all_users(username):
        with database() as db:
            db.cursor.execute(f"select name, status, img from users where not name = '{username}'")
            return db.cursor.fetchall()

    def get_chat(username, chatpartner):
        with database() as db:
            data = []
            db.cursor.execute(f"select id from chats where user1 in ('{username}','{chatpartner}') and user2 in ('{username}','{chatpartner}')")
            for i in db.cursor.fetchall():
                db.cursor.execute(f"select msg from chats where id = '{int(i[0])}'")
                msg = db.cursor.fetchone()
                db.cursor.execute(f"select user1 from chats where id = '{int(i[0])}'")
                written_by = db.cursor.fetchall()

                if written_by[0][0] == username:
                        written_by = "right"
                else:
                    written_by = "left"

                data.append([written_by, msg])
            return data