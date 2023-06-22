from flask import Flask, render_template, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from threading import Thread

app = Flask(__name__)

TOKEN = '6249631383:AAGN7i8eoqh-QOZyq5aFYmhYdPcE_f6UDN0'
updater = None
bot_thread = None

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🚀Com certeza", callback_data='1'),
            InlineKeyboardButton("❌Não", callback_data='2'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('👋  Olá, bem vindo! O canal TipsMaster e a Suprabets estão promovendo um Mega Sorteio! O Ganhador receberá uma Banca em seu nome, recheada com R💲4.000,00\n\nQuer participar?', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == '1':
        context.user_data['step'] = 'name'
        query.edit_message_text(text="♥️ Ótimo, vamos lá!\n\n Irei precisar de alguns dados:\n\n1️⃣  Digite seu nome completo:")
    elif query.data == 'email_correct':
        context.bot.send_message(chat_id=1820571821, text=context.user_data.get('email'))
        query.edit_message_text(text="3️⃣  Agora, envie um Print de um comprovante de depósito de qualquer valor efetuado na SupraBets (Caso ainda não tenha uma conta na Suprabets poderá criar através do link https://bit.ly/3Lxa6p2).\n\n🗒️Envie seu comprovante agora...")
        context.user_data['step'] = 'receipt'
    elif query.data == 'email_incorrect':
        context.user_data['step'] = 'email'
        query.edit_message_text(text="Por favor, digite seu email novamente.")
    elif query.data == 'finish':
        query.edit_message_text(text="👋")

def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('step') == 'name':
        context.bot.send_message(chat_id=1820571821, text=update.message.text)
        context.user_data['email'] = None
        context.user_data['step'] = 'email'
        update.message.reply_text('2️⃣  Seu melhor E-mail: ( será através dele que entraremos em contato caso você ganhe. )')
    elif context.user_data.get('step') == 'email':
        context.user_data['email'] = update.message.text
        keyboard = [
            [
                InlineKeyboardButton("✔️Está correto", callback_data='email_correct'),
                InlineKeyboardButton("❌Corrigir", callback_data='email_incorrect'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f'Confirme seu email: {update.message.text}', reply_markup=reply_markup)

def handle_receipt(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('step') == 'receipt':
        if update.message.document:
            file_id = update.message.document.file_id
            context.bot.send_document(chat_id=1820571821, document=file_id, 
                                      caption=f'User ID: {update.message.from_user.id}\nUsername: {update.message.from_user.username}')
        elif update.message.photo:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.get_file(file_id)
            newFile.download('receipt_photo.jpg')
            context.bot.send_document(chat_id=1820571821, document=open('receipt_photo.jpg', 'rb'), 
                                      caption=f'User ID: {update.message.from_user.id}\nUsername: {update.message.from_user.username}')
        else:
            return

        keyboard = [
            [
                InlineKeyboardButton("🔚Finalizar", callback_data='finish'),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('✅ Muito bom, seus dados foram recebidos!\n\nVocê já está concorrendo, o sorteio será realizado no dia 25/07/2023, caso você seja o ganhador, entraremos em contato através do e-mail cadastrado para entregar a premiação.\n\nBoa Sorte🍀', reply_markup=reply_markup)
        context.user_data['receipt_sent'] = True


@app.route('/')
def home():
    global updater
    return render_template('index.html', bot_status=updater is not None)

@app.route('/toggle', methods=['POST'])
def toggle_bot():
    global updater, bot_thread
    if updater is None:
        updater = Updater(token=TOKEN, use_context=True)
        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        updater.dispatcher.add_handler(MessageHandler(Filters.document | Filters.photo, handle_receipt))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        bot_thread = Thread(target=updater.start_polling)
        bot_thread.start()
    else:
        updater.stop()
        updater = None
        bot_thread.join()
        bot_thread = None
    return '', 204
if __name__ == '__main__':
    app.run(port=3000)