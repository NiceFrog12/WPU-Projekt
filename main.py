from google import genai # Google Gemini API
import telebot # Telegram bot API

from config import BOT_TOKEN, GOOGLE_API # Misc imports
import time

client = genai.Client(api_key=GOOGLE_API)

bot = telebot.TeleBot(BOT_TOKEN)


welcome_msg = "Ich bin der Bot der dir mit Nachhaltigkeit helfen soll! Falls du fragen hast, wie du mich nutzen kannst, schick einfach /help in chat rein!" # Message for /start
# In my opinion it's more readable this way

help_msg = "this is a WIP"

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, welcome_msg)

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, help_msg)

if __name__ == "__main__":
    bot.polling(none_stop=True)