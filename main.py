import google.generativeai as genai # Google Gemini API
from google.generativeai import types
import telebot # Telegram bot API

from config import BOT_TOKEN, GOOGLE_API # Misc imports
import time

# Gemini API stuff
genai.configure(api_key=GOOGLE_API)
model = genai.GenerativeModel("gemini-1.5-flash")

# Telebot stuff
bot = telebot.TeleBot(BOT_TOKEN)


welcome_msg = "Ich bin der Bot der dir mit Nachhaltigkeit helfen soll! Falls du fragen hast, wie du mich nutzen kannst, schick einfach /help in chat rein!" # Message for /start
# In my opinion it's more readable this way

help_msg = "this is a WIP"

# Instructions for the Gemini API
sys_instruct="Du sprichst nur Deutsch und über das Thema Nachhaltigkeit. Alle deine Antworten sollen auf Deutsch sein." 
client = genai.configure(api_key=GOOGLE_API)
used_facts = []


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

@bot.message_handler(commands=["fact"])
def send_random_fact(message):
    global used_facts
    response = model.generate_content(sys_instruct + '\n' + f"Schreib mir ein zufälliger Fakt über Nachhaltigkeit. IF THE FACT IS ALREADY IN {used_facts} YOU CANNOT USE IT AGAIN!!")
    used_facts += response
    #response.text is the correct thing you need to pull out
    try:
        bot.send_message(message.chat.id, response.text)
    except Exception:
        bot.send_animation(message.chat.id, "There has been an error while working through your request.")
        print(Exception)


if __name__ == "__main__":
    bot.polling(none_stop=True)