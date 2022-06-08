import time
from threading import Thread
from src.database.database import database
from src.modules.session import clear_all_session

START_SEVER = ['22', '00','00']
REBOOT = False
RESET_TIME   = [
    ['12', '00', '00'],
    ['24', '00', '00']
]
H = None
M = None
S = None

def get_time():
    global H
    global M
    global S
    H = time.strftime('%H')
    M = time.strftime('%M')
    S = time.strftime('%S')

def starts_on_time():
    global H
    global M
    global S
    global START_SEVER
    while True:
        get_time()
        print(f'{H}:{M}:{S}')
        if str([H, M, S]) == str(START_SEVER):
            #Thread(target=reset_sessions).start()
            print('server starts')
            logs('server starts')
            break
        time.sleep(1)

def reset_sessions():
    global H
    global M
    global S
    global REBOOT
    global RESET_TIME
    while True:

        for t in RESET_TIME:
            if  H == t[0] and M == t[1] and S == t[2]:
                REBOOT = True

        if REBOOT == True:
            REBOOT = False
            clear_all_session()
            
            with database() as db:
                db.cursor.execute("select name from users")
                for user in db.cursor.fetchall():
                    db.cursor.execute(f"update users set status = 'offline' where name = '{user[0]}'")
            print('reset all sessions')
            logs('reset all sessions')

        time.sleep(1)

def logs(msg):
    global H
    global M
    global S
    with open('.logs.txt','a')as f:
        get_time()
        f.write(f'\ntime:{H}:{M}:{S}-{msg}')