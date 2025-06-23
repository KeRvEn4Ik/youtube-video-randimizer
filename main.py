from flask import Flask, request, redirect, render_template, session
import os
import database
import random
import requests


app = Flask(__name__)
app.secret_key = os.urandom(24)

API_KEY = 'AIzaSyBQSvezVu8vLf-Lbv7M1RYmqoEe1QslcAc'
url_for_video = 'https://www.youtube.com/watch?v=N-_SHsOejKw'

def get_random_video_id():
    queries = [
    "film", "animation", "cars", "vehicles", "music", "pets", "animals",
    "sports", "short films", "travel", "events", "gaming", "vlog", "people", 
    "blogs", "comedy", "entertainment", "news", "politics", "how-to", 
    "style", "education", "science", "technology", "nonprofits", 
    "activism", "movies", "anime", "action", "adventure", "classics", 
    "documentary", "drama", "family", "foreign", "horror", "sci-fi", 
    "fantasy", "thriller", "shorts", "tv shows", "trailers"
    ]
    query = random.choice(queries)

    url = (
        'https://www.googleapis.com/youtube/v3/search'
        '?part=snippet'
        '&maxResults=10'
        '&type=video'
        f'&q={query}'
        f'&key={API_KEY}'
    )

    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video = random.choice(data['items'])
        return {
            'id': video['id']['videoId'],
            'title': video['snippet']['title']
            }
    
    else:
        return None
    
@app.route('/')
def main_page():
    video = get_random_video_id()
    username = session.get('username')
    user = database.get_one_user(username)
    if video:
        if username:
            url_video = f'https://www.youtube.com/watch?v={ video['id'] }'
            title = video['title']

            database.add_video(username, url_video, title)
        return render_template('main_page.html', user=user, video_id=video['id'])
    else:
        return render_template('main_page.html', user=user, error='Видео закончились')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register_page.html')
    if request.method == 'POST':
        name = request.form['user_name']
        password = request.form['user_password']

        if name == '':
            return render_template('register_page.html', error='Укажите логин')

        if password == '':
            return render_template('register_page.html', error='Укажите пароль')

        if database.check_user_login(name):
            return render_template('register_page.html', error='Этот логин уже существует')
        else:
            database.add_user(name, password)
            return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login_page.html')
    if request.method == 'POST':
        name = request.form['user_name']
        password = request.form['user_password']

        if database.check_user(name, password):
            session['username'] = name
            return redirect('/')
        else:
            return render_template('login_page.html', error='Неверное имя или пароль') 

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/settings', methods=['GET', 'POST'])
def settigs_page():
    if request.method == 'GET':
        history = database.get_history(session['username'])
        user = database.get_one_user(session['username'])
        return render_template('settigs_page.html', user=user, history=history)
    if request.method == 'POST':
        theme = request.form['theme']
        database.update_theme(theme, session['username'])
        return redirect('/settings')
database.init_database()
app.run(debug=True)