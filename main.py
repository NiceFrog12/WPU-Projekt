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
given_tips = []
food_advice = []

#                   IDEAS FOR THE BOT
# 1. Make the bot discuss foods (e.g. what foods should you buy and why.) // DONE
# 2. Let the bot give you ideas how to better your day-to-day life (make it more sustainable) // DONE
# 3. 



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

@bot.message_handler(commands=["fakt"])
def send_random_fact(message):
    global used_facts
    try:
        response = model.generate_content(sys_instruct + '\n' + f"Schreib mir ein zufälliger Fakt über Nachhaltigkeit. IF THE FACT IS ALREADY IN {used_facts} YOU CANNOT USE IT AGAIN!!")
        used_facts += [response.text]
    #response.text is the correct thing you need to pull out
    
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)


@bot.message_handler(commands=["alltag"])
def daily_life_tip(message):
    global given_tips
    try:
        response = model.generate_content(sys_instruct + "\n" + f"Schreib mir ein Weg/Tipp, wie ich mein Alltag nachhaltiger machen kann. IF THE FACT IS ALREADY IN {given_tips} YOU CANNOT USE IT AGAIN!!")
        given_tips += [response.text]
    
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)


@bot.message_handler(commands=["essen"])
def food_advice_command(message):
    global food_advice
    try:
        response = model.generate_content(sys_instruct + '\n' + f"Schreib mir eine Rekommendation, über was ich essen soll und warum. Begründe deine Meinung mit einfache Sprache. IF THE ADVICE IS ALREADY IN {food_advice} YOU CANNOT USE IT AGAIN!!")
        food_advice += [response.text]
    
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)



if __name__ == "__main__":
    bot.polling(none_stop=True)