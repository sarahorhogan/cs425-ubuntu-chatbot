import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

api_endpoint = os.getenv('API_ENDPOINT')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    chat_id = update.message.chat.id

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome to the reminder bot!")

    response = requests.post(api_endpoint,
                             json={'telegramHandle': username,
                                   'chatId': chat_id})
    if response.status_code == 200:
        print('User saved successfully')
    else:
        print(f'Failed to save user: {response.content}')


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv(
        'TELE_BOT_TOKEN')).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
