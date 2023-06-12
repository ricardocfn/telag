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
        text += "<b>ℹ️ Para isso basta nos enviar aqui, um comprovante de depósito de qualquer valor na sua conta da SupraBets, caso ainda nao tenha uma conta cadastre-se aqui ➡ https://bit.ly/3Lxa6p2</b>", parse_mode=ParseMode.HTML
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

