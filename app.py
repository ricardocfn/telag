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
            InlineKeyboardButton("🚀Com certeza!", callback_data='1'),
            InlineKeyboardButton("❌Não", callback_data='2'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('👋  Olá, bem vindo! O canal TipsMaster e a Suprabets estão promovendo um Mega Sorteio! O Ganhador receberá uma Banca em seu nome, recheada com R💲3.000,00\n\nQuer participar?', reply_markup=reply_markup)

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

=======
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
            InlineKeyboardButton("✅🔥 Entrar para o TipsMaster Vip 🔥✅", callback_data='join_vip'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Bem-vindo! Clique no botão abaixo para saber como garantir seu acesso GRÁTIS ao canal.', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == "join_vip":
        keyboard = [
            [
                InlineKeyboardButton("Enviar comprovante", callback_data='send_proof'),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "⭐️ No TipsMaster Vip você tem acesso a bilhetes prontos com ODDS turbinadas diariamente!\n\n"
        text += "✅ Você pode fazer parte do canal gratuitamente! Isso mesmo, 0800!\n\n"
        text += "ℹ️ Para isso basta nos enviar aqui, um comprovante de depósito de qualquer valor na sua conta da SupraBets, caso ainda nao tenha uma conta cadastre-se aqui ➡️ https://bit.ly/3Lxa6p2 \n\n"
        text += "Nossa equipe irá analisar rapidinho e se estiver tudo de acordo, você receberá o link para fazer parte do nosso canal 🚀"

        context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=reply_markup)

    elif query.data == "send_proof":
        query.edit_message_reply_markup(reply_markup=None)
        context.bot.send_message(chat_id=query.message.chat_id, text="Por favor, envie seu comprovante . . .")

    elif query.data.startswith("add_to_vip:"):
        chat_id = int(query.data.split(':')[1])
        link = context.bot.export_chat_invite_link(chat_id=-1001581344401)
        context.bot.send_message(chat_id=chat_id, text="✅ Está tudo certo! Aqui está o seu link exclusivo: " + link)
        
        keyboard = [
            [
                InlineKeyboardButton("Finalizar", callback_data='finalize'),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text="🤝 Aproveite o Vip e bons lucros!", reply_markup=reply_markup)

    elif query.data == "finalize":
        context.bot.send_message(chat_id=query.message.chat_id, text="👋")

def handle_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.photo[-1].file_id if update.message.photo else update.message.document.file_id
    is_photo = True if update.message.photo else False
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    if username:
        username = '@' + username

    user_info = f"Usuário: {username}\nNome: {first_name} {last_name}\nChat ID: {chat_id}"

    context.bot.send_message(chat_id=1820571821, text=user_info)
    if is_photo:
        context.bot.send_photo(chat_id=1820571821, photo=file_id)
    else:
        context.bot.send_document(chat_id=1820571821, document=file_id)

    update.message.reply_text("😀Obrigado pelo envio! Aguarde um instante enquanto nossa equipe verifica o comprovante e logo você será adicionado ao TipsMasters Vip.")
    
    keyboard = [
        [
            InlineKeyboardButton("Adicionar ao VIP", callback_data=f'add_to_vip:{chat_id}'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=1820571821, text="Adicione este usuário ao VIP:", reply_markup=reply_markup)


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
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        updater.dispatcher.add_handler(MessageHandler(Filters.photo | Filters.document, handle_file))
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
