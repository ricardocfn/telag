from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Função para lidar com o comando /start
def start(update, context):
    keyboard = [
        [InlineKeyboardButton('Entrar para o Vip', callback_data='entrar_vip')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Bem-vindo! Clique no botão "Entrar para o Vip" para saber mais sobre o Vip TipsMaster.', reply_markup=reply_markup)

# Função para lidar com a opção "Entrar para o Vip"
def entrar_vip(update, context):
    keyboard = [
        [InlineKeyboardButton('Enviar comprovante', callback_data='enviar_comprovante')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('[🗒] ⭐️ No TipsMaster vip você tem acesso a bilhetes prontos com ODDS turbinadas diariamente!\n\n✅ Você pode fazer parte do canal gratuitamente! Isso mesmo, 0800!\n\nℹ️ Para isso basta nos enviar aqui, um comprovante de depósito na sua conta da SupraBets. Nossa equipe irá analisar rapidinho e se estiver tudo de acordo, você será automaticamente adicionado ao Vip Tipmasters 🚀', reply_markup=reply_markup)

# Função para lidar com o envio de foto
def receber_foto(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('foto_usuario.jpg')
    update.message.reply_text('😀Obrigado pelo envio! Aguarde um instante enquanto nossa equipe verifica o comprovante e logo você será adicionado ao TipsMasters Vip.')

# Função para lidar com os botões inline
def button(update, context):
    query = update.callback_query
    if query.data == 'entrar_vip':
        entrar_vip(update, context)
    elif query.data == 'enviar_comprovante':
        query.message.reply_text('Por favor, envie o comprovante de depósito...')

def main():
    # Crie um objeto Updater e passe o token do seu bot
    updater = Updater(token='6249631383:AAGN7i8eoqh-QOZyq5aFYmhYdPcE_f6UDN0', use_context=True)

    # Obtenha o despachante para registrar os manipuladores de comando, mensagens e botões inline
    dispatcher = updater.dispatcher

    # Registre um manipulador de comando para o comando /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Registre um manipulador de mensagens para receber fotos
    dispatcher.add_handler(MessageHandler(Filters.photo, receber_foto))

    # Registre um manipulador de botões inline
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Inicie o bot
    updater.start_polling()

    # Mantenha o bot em execução até que Ctrl + C seja pressionado
    updater.idle()

if __name__ == '__main__':
    main()
