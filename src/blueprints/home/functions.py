import re
from src.database.database import database
from src.modules.session import *

def is_session():
    username = get_session()
    if username:
        if exist_user(username):
            return username

def exist_user(username):
    if database.is_user_in_database(username):
        return True

def get_all_users():
    with database() as db:
        db.cursor.execute(f"select name, status, img from users where not name = '{get_session()}'")
        return db.cursor.fetchall()

def allowed_file(filename):
    allowed = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed

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

def is_link_in_msg(msg):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
    if url:
        if url[0] in msg:
            msg = msg.replace(url[0] ,f"<a href={url[0]} target=_blank>{url[0]}</a>")
    return msg

def add_message(username, chatpartner, message, ):
    with database() as db:
        db.cursor.execute(f"select * from chats")
        data = db.cursor.fetchall()
        message_id = len(data)
        db.cursor.execute(f"insert into chats values('{message_id}', '{username}', '{chatpartner}', '{message}')")

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

def set_user_online(username):
    with database() as db:
        db.cursor.execute(f"update users set status = 'online' where name = '{username}'")

def set_all_user_offline():
    with database() as db:
        db.cursor.execute("select name from users")
        for user in db.cursor.fetchall():
            db.cursor.execute(f"update users set status = 'offline' where name = '{user[0]}'")

#zum ausloggen wenn der tap einfach zu gemacht wird
max_time = 15
all_active_sessions = []
def active_sessions(name):
    if len(all_active_sessions) < 1:
        all_active_sessions.append([name, 0])

    if name not in [i[0] for i in all_active_sessions]:
        all_active_sessions.append([name, 0])
        
    for i in all_active_sessions:
        i[1]+=1#counter wenn bei max_time dann ausgeloggt
        if name == i[0]:#user noch da
            i[1] = 0

        if i[1] >= max_time:#wird ausgelogt
            set_all_user_offline()
            index = all_active_sessions.index(i)
            all_active_sessions.pop(index)#wird aus den active_sessions entfernt