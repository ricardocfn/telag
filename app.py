from flask import Flask, request
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


app = Flask(__name__)
TOKEN = '6249631383:AAGN7i8eoqh-QOZyq5aFYmhYdPcE_f6UDN0'


def start(update, context):
    keyboard = [
        [InlineKeyboardButton('✅🔥 Entrar para o Vip 🔥✅', callback_data='entrar_vip')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Bem-vindo! Clique no botão "Entrar para o Vip" para saber como garantir seu acesso GRÁTIS ao canal.', reply_markup=reply_markup)


def entrar_vip(update, context):
    keyboard = [
        [InlineKeyboardButton('Enviar comprovante', callback_data='enviar_comprovante')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('⭐️ No TipsMaster vip você tem acesso a bilhetes prontos com ODDS turbinadas diariamente!\n\n✅ Você pode fazer parte do canal gratuitamente! Isso mesmo, 0800!\n\nℹ️ Para isso basta nos enviar aqui, um comprovante de depósito na sua conta da SupraBets. Nossa equipe irá analisar rapidinho e se estiver tudo de acordo, você será automaticamente adicionado ao Vip Tipmasters 🚀', reply_markup=reply_markup)


def receber_foto(update, context):
    photo = update.message.photo[-1]
    photo_file_id = photo.file_id

    user = update.message.from_user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    chat_id = update.message.chat_id
    outras_informacoes = ""

    caption = f"Foto enviada por {first_name} {last_name} (@{username})\n\nChat ID: {chat_id}\n\n{outras_informacoes}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Finalizar', callback_data='finalizar')]])
    update.message.reply_text('😀 Obrigado pelo envio! Aguarde um instante enquanto nossa equipe verifica o comprovante e logo você será adicionado ao TipsMasters Vip.', reply_markup=reply_markup)
    context.bot.send_photo(chat_id=1820571821, photo=photo_file_id, caption=caption)


def button(update, context):
    query = update.callback_query
    if query.data == 'entrar_vip':
        entrar_vip(update, context)
    elif query.data == 'enviar_comprovante':
        query.message.reply_text('Por favor, envie o comprovante de depósito...')
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    elif query.data == 'finalizar':
        query.message.reply_text('👋')


@app.route('/<token>', methods=['POST'])
def webhook(token):
    if token == TOKEN:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


def main():
    global updater, bot, dispatcher
    bot = telegram.Bot(TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, receber_foto))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=3000)

