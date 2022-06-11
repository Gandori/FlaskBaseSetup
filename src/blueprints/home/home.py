import json
import re
from flask import Blueprint, redirect, render_template, url_for, request, flash
from werkzeug.utils import secure_filename
from src.modules.session import get_session
from src.database.database import database

home = Blueprint('home',__name__)
home.template_folder = 'templates'
home.static_folder = 'static'

#routes
@home.route('/', methods=['GET'])
def index():
    username = get_session()
    page = 'home.html'
    content = 'profile.html'
    title = 'home'
    profile_img = database.get_profile_img(username)

    if not username: return redirect(url_for('signin.index'))
    return render_template(page,
                        title=title,
                        user=username,
                        content=content,
                        profile_img=profile_img)

@home.route('/profile', methods=['GET'])
def profile():
    username = get_session()
    user = request.args.get('user')
    page = 'home.html'
    content = 'profile.html'
    title = 'home'
    profile_img = database.get_profile_img(username)
    user_img = database.get_profile_img(user)

    if not username: return redirect(url_for('home.index'))
    if not database.is_user_in_database(user): return redirect(url_for('home.index'))

    return render_template(page,
                        title=title,
                        user=user,
                        content=content,
                        profile_img=profile_img,
                        user_img = user_img)

@home.route('/chat', methods=['GET'])
def chat():
    username = get_session()
    chatpartner = request.args.get('user')
    page = 'home.html'
    title = 'home'
    content = 'chat.html'
    profile_img = database.get_profile_img(username)
    
    if not username:return redirect(url_for('home.index'))
    if not chatpartner:return redirect(url_for('home.index'))
    if not database.is_user_in_database(chatpartner):return redirect(url_for('home.index'))

    database.set_chatpartner(username, chatpartner)
    return render_template(page,
                            title=title,
                            content=content,
                            user=chatpartner,
                            profile_img=profile_img)
    
@home.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']

    if not message: return ''

    #ist link in message
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    if url:
        if url[0] in message:
            message = message.replace(url[0] ,f"<a href={url[0]} target=_blank>{url[0]}</a>")

    username = get_session()
    if not username: return redirect(url_for('home.index'))

    chatpartner = database.get_chatpartner(username)
    if not chatpartner: return redirect(url_for('home.index'))

    database.add_message(username, chatpartner, message)
    
    return ''

@home.route('/get_data', methods=['GET'])
def get_data():
    username = get_session()
    chatpartner = database.get_chatpartner(username)

    if not username: return ''

    active_sessions(username)
    database.set_user_online(username)
    sidebar_data = database.get_all_users(username)
    chat_data = database.get_chat(username, chatpartner)

    return json.dumps([sidebar_data, chat_data])

@home.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        flash('Das Bild konnte nicht hochgeladen werden')
        return redirect(url_for('home.index'))

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f'{get_session()}.jpg'
        file.save(f'src/static/profile_images/{filename}')
        username = get_session()
        database.set_profile_img(username ,f'profile_images/{filename}')
    else:
        flash('Der Dateityp ist nicht Erlaubt')

    return redirect(url_for('home.index'))

#methods

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
            database.set_all_user_offline()
            index = all_active_sessions.index(i)
            all_active_sessions.pop(index)#wird aus den active_sessions entfernt

def allowed_file(filename):
    allowed = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed
