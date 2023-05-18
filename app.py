from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import threading
import time
import os
from werkzeug.utils import secure_filename
import telebot

app = Flask(__name__)
app.secret_key = '30secondstomars'  # Substitua 'sua_chave_secreta_aqui' por uma chave secreta de sua escolha
bot = telebot.TeleBot('6151054063:AAFDJe8ZzBnNIG-b-CG6EUSYgX-YWt9p0CY')  # Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'ricardo' and password == '0710':  # Substitua 'admin' e 'password' pelas credenciais desejadas
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            message = "Credenciais inválidas!"
    return render_template('login.html', message=message)

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    message = None  # Inicializa a variável da mensagem como None

    if request.method == 'POST':
        image = request.files['image']
        caption = request.form['caption']
        date_str = request.form['date']
        date = datetime.fromisoformat(date_str.replace('T', ' '))

        # Salve a imagem em um arquivo temporário
        image_path = f'tmp/{secure_filename(image.filename)}'
        image.save(image_path)

        # Crie uma nova thread para enviar a postagem no horário agendado
        thread = threading.Thread(target=send_post, args=(image_path, caption, date))
        thread.start()

        message = "Postagem agendada!"  # Define a mensagem de sucesso

    return render_template('index.html', message=message)  # Passa a mensagem para o template

def send_post(image_path, caption, date):
    # Calcule o tempo restante até o horário agendado
    current_time = datetime.now()
    time_delta = date - current_time
    time_to_sleep = time_delta.total_seconds()

    # Aguarde até o tempo restante expirar
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)

    # Envie a postagem para o Telegram
    chat_id = '-1001980761038'  # Substitua 'YOUR_CHANNEL_ID' pelo ID do seu canal
    with open(image_path, 'rb') as photo_file:
        bot.send_photo(chat_id, photo_file, caption=caption)
    os.remove(image_path)

if __name__ == "__main__":
    app.run(debug=True)
