from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import telebot
import time
from threading import Thread


app = Flask(__name__)
app.secret_key = '30secondstomars'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Adicione o caminho do seu banco de dados aqui
db = SQLAlchemy(app)
DB_DIR = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])
os.makedirs(DB_DIR, exist_ok=True)
bot = telebot.TeleBot('6151054063:AAFDJe8ZzBnNIG-b-CG6EUSYgX-YWt9p0CY')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(120), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'ricardo' and password == '0710': 
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            message = "Credenciais inválidas!"
    return render_template('login.html', message=message)

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    message = None

    if request.method == 'POST':
        image = request.files['image']
        caption = request.form['caption']
        date_str = request.form['date']
        date = datetime.fromisoformat(date_str.replace('T', ' '))

        image_path = f'tmp/{secure_filename(image.filename)}'
        image.save(image_path)

        post = Post(image_path=image_path, caption=caption, date=date)
        db.session.add(post)
        db.session.commit()

        message = "Postagem agendada!"

    if not session.get('thread_started', False):
        session['thread_started'] = True
        Thread(target=lambda: check_posts(app)).start()

    return render_template('index.html', message=message)

def check_posts(app):
    with app.app_context():
        while True:
            current_time = datetime.now()

            posts_to_send = Post.query.filter(Post.date <= current_time).all()

            for post in posts_to_send:
                with open(post.image_path, 'rb') as photo_file:
                    bot.send_photo('-1001980761038', photo_file, caption=post.caption)
                os.remove(post.image_path)
                db.session.delete(post)

            db.session.commit()

            time.sleep(60)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
