import json
from flask import Blueprint, redirect, render_template, url_for, request, flash
from werkzeug.utils import secure_filename
from .functions import *

home = Blueprint('home',__name__)
home.template_folder = 'templates'
home.static_folder = 'static'

PAGE = 'home.html'
TITLE = 'home'

@home.route('/', methods=['GET'])
def index():
    username = is_session()
    if username:
        return render_template(PAGE,
                                title=TITLE,
                                content='profile.html',
                                user=get_session(),
                                profile_img=get_profile_img(username))

    return redirect(url_for('signin.index'))

@home.route('/chat', methods=['GET'])
def chat():
    username = get_session()
    if username:
        chatpartner = request.args.get('user')
        if chatpartner:
            if exist_user(chatpartner):
                set_chatpartner(username, chatpartner)
                return render_template(PAGE,
                                        title=TITLE,
                                        content='chat.html',
                                        user=chatpartner,
                                        profile_img=get_profile_img(username))

    return redirect(url_for('home.index'))

@home.route('/profile', methods=['GET'])
def profile():
    username = is_session()
    if username:
        user = request.args.get('user')
        if exist_user(user):
            return render_template(PAGE,
                                    title=TITLE,
                                    content='profile.html',
                                    user=request.args.get('user'),
                                    profile_img=get_profile_img(username),
                                    user_img = get_profile_img(user))

    return redirect(url_for('home.index'))
    
@home.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']

    if message:
        message = is_link_in_msg(message)
        username = get_session()

        if username:
            chatpartner = get_chatpartner(username)
            if chatpartner:
                if exist_user(chatpartner):
                    add_message(username, chatpartner, message)
    return ''

@home.route('/get_data', methods=['GET'])
def get_data():
    username = get_session()
    if username:
        active_sessions(username)
        set_user_online(username)
        chatpartner = get_chatpartner(username)
        sidebar_data = get_all_users()
        chat_data = get_chat(username, chatpartner)
        return json.dumps([sidebar_data, chat_data])

    return ''

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
        set_profile_img(username ,f'profile_images/{filename}')
    else:
        flash('Der Dateityp ist nicht Erlaubt')

    return redirect(url_for('home.index'))
