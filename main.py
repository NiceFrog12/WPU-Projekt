import google.generativeai as genai # Google Gemini API
import telebot # Telegram bot API

from config import BOT_TOKEN, GOOGLE_API # Misc imports
import time

# Gemini API stuff
genai.configure(api_key=GOOGLE_API)
model = genai.GenerativeModel("gemini-1.5-flash")

# Telebot stuff
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")


welcome_msg = "*Hallo ich bin Nicebot12_*\nIch bin dafür da dein *Leben einfacher zu machen*. Zwar kann ich nicht kochen, *aber ich kann dir aber bei vielen anderen Sachen helfen*.\nMit `/help` siehst du alle meine Funktionen. Ich hoffe, dass ich dir helfen kann, ein umweltfreundliches und freundliches Leben zu führen."

# In my opinion it's more readable this way

help_msg = "/start\n/help\n/essen\n/alltag\n/fakt\n/rezept"

# Instructions for the Gemini API
sys_instruct="Du sprichst nur Deutsch und über das Thema Nachhaltigkeit. Alle deine Antworten sollen auf Deutsch sein. Du kannst simple Form von Markdown nutzen, aber nur in die Form was Telegram Markdown supportet. Als Beispiel, das ist *Bold* und das ist __italicized__"
client = genai.configure(api_key=GOOGLE_API)
used_facts = []
given_tips = []
food_advice = []
recipes_used = []
news_used = []


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown")

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, help_msg ,parse_mode="HTML")

@bot.message_handler(commands=["test"])
def testingcommand(message):
    bot.send_message(message.chat.id, "this is *bold* or *italicized.* another try of __bold__ or _italicized_",parse_mode="Markdown")
# ´JUST USE MARKDOWN: IT IS NOT WORTH FIGURING OUT MDV2

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

@bot.message_handler(commands=["rezept"])
def recipe_advice_command(message):
    global recipes_used
    try:
        response = model.generate_content(sys_instruct + "\n" + f"Schreib mir ein kurzen und nachhaltiges Rezept, was ich zuhause kochen kann. IF THE FACT IS ALREADY IN {recipes_used} YOU CANNOT USE IT AGAIN!!")
        recipes_used = [response.text]

        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)

@bot.message_handler(commands=["news"])
def nachhaltigkeit_news(message):
    global news_used
    try:
        response = model.generate_content(sys_instruct + "\n" + f"Schreib mir ein Neuigkeit der was mit Nachhaltigkeit zu tun hat aus moderne Zeit. Es muss irgendwas relevantes sein, die Sprache soll aber simple bleiben. IF THE NEWS ARE ALREADY IN {news_used} YOU CANNOT USE IT AGAIN!!")
        news_used = [response]

        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(3)
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)

@bot.message_handler(commands=["item"])
def pick_trashcan(message):
    try:
        response = model.generate_content(sys_instruct + "\n" + f"In welche Mülltone soll diese Sache rein gehen: " + message.text)

        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)


@bot.message_handler(commands=["credits"])
def credits_command(message):
    credits_message = "Dieser Bot war als ein WPU Projekt erstellt von Aleksandrs Litvins und Fynn Beneke"
    bot.send_message(message.chat.id, credits_message)



if __name__ == "__main__":
    bot.polling(none_stop=True)
