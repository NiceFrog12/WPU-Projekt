import google.generativeai as genai # Google Gemini API
from google.generativeai import types
import telebot # Telegram bot API
from telebot import types as tele_type

BOT_TOKEN = "telegram_token"
GOOGLE_API = "gemini_token"
# Misc imports
import time

# Gemini API stuff
genai.configure(api_key=GOOGLE_API)
model = genai.GenerativeModel("gemini-1.5-flash")

# Telebot stuff
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")


welcome_msg = "*Hallo ich bin Nicebot12_*\n\nIch bin dafür da dein *Leben einfacher zu machen*. Zwar kann ich nicht kochen, *aber ich kann dir aber bei vielen anderen Sachen helfen*.\n\nMit `/help` siehst du alle meine Funktionen. Ich hoffe, dass ich dir helfen kann, ein umweltfreundliches und freundliches Leben zu führen."

lambda_message = "Du brauchst Hilfe? Kein Problem, mit `/start` schaltest du mich ein ^^.\n\nMit `/help` kannst du mich nach Hilfe bitten, welches Commands ich habe 🙂"

# In my opinion it's more readable this way

help_msg = """
`/alltag` Hier kannst du Informationen bekommen, die dir helfen können, deinen Alltag nachhaltiger zu machen.


`/fakt` erzähle ich dir einen lustigen Fakt über den aktuellen Stand der Dinge. Nartüllich hat es was mit umwellt zutun.

Mit `/rezept` gebe ich dir ein Rezept was du nachkochen kannst, aber vertrau nicht auf meine Tipps, denn ich esse ja nicht 😉

`/essen` kann ich dir helfen was man essen könnte, was gesund aber auch schmeckt und auch auf regionale basis ist

`/tonne`  Diese Command erzählt dir über verschiedene Mülltonnen, die es in Deutschland gibt. Es spricht etwa über jede Tonne und erklärt, welcher Müll da drin gehört.

`/item <Sache>`  hilft dir mit einer KI den Müll in einer der Mülltonnen einzuordnen, sodass du den Müll ohne Probleme sortieren kannst.  Das hilft dir, wenn du unsicher bist, wo dein Müll hingehört.

`/news` damit zeigt der Bot dir an, was in der Welt gerade so passiert. *Wichtig*: Die KI könnte *fehlerhaft* sein und nicht 100% richtige Information zeigen!!!

`/credits` ist eine kleine Command die ein bisschen über die Entwicklern dieser Bots spricht 😜
"""

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
    bot.send_message(message.chat.id, help_msg ,parse_mode="Markdown")


@bot.message_handler(commands=["fakt"])
def send_random_fact(message):
    global used_facts
    try:
        response = model.generate_content(sys_instruct + '\n' + f"Schreib mir ein zufälliger Fakt über Nachhaltigkeit. IF THE FACT IS ALREADY IN {used_facts} YOU CANNOT USE IT AGAIN!!")
        used_facts += [response.text]
    #response.text is the correct thing you need to pull out
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)
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

        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
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

        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)

@bot.message_handler(commands=["rezept"])
def recipe_advice_command(message):
    global recipes_used
    try:
        response = model.generate_content(sys_instruct + "\n" + f"Schreib mir ein kurzen und nachhaltiges Rezept, was ich zuhause kochen kann. IF THE FACT IS ALREADY IN {recipes_used} YOU CANNOT USE IT AGAIN!!")
        recipes_used += [response.text]
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)
        bot.send_message(message.chat.id, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "There has been an error while working through your request.")
        print(e)

@bot.message_handler(commands=["news"])
def nachhaltigkeit_news(message):
    global news_used
    try:
        response = model.generate_content(sys_instruct + "\n" + f"Schreib mir ein Neuigkeit der was mit Nachhaltigkeit zu tun hat aus moderne Zeit. Es muss irgendwas relevantes sein, die Sprache soll aber simple bleiben. IF THE NEWS ARE ALREADY IN {news_used} YOU CANNOT USE IT AGAIN!!")
        news_used += [response]

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


@bot.message_handler(commands=["tonne"])
def trashcan_info(message):
    markup = tele_type.InlineKeyboardMarkup(row_width=2)

    versch_tonnen = [tele_type.InlineKeyboardButton("Papiermüll", callback_data="cb_papier"), tele_type.InlineKeyboardButton("Restmüll", callback_data="cb_rest"), tele_type.InlineKeyboardButton("Biomüll", callback_data="cb_bio"), tele_type.InlineKeyboardButton("Gelber Sack", callback_data="cb_sack"), tele_type.InlineKeyboardButton("Andere", callback_data="cb_andere")]
    for item in versch_tonnen:
        markup.add(item)
    bot.send_message(message.chat.id, "Über welche Mülltonne willst du was herausfinden: ", reply_markup=markup)


@bot.callback_query_handler(func=lambda call : True)
def tonnen_query(call):
    bot.answer_callback_query(call.id , "Hier sind paar Informationen: ")
    if call.data == "cb_rest":
        ans = "Hier landet alles, was in keine anderen Tonnen passt:  Speisereste (gut verpackt!), Windeln,  Staubsaugerbeutel,  Hygiene-Artikel,  verunreinigte Verpackungen, die nicht recycelbar sind etc.  Wichtig: Vermeidung durch Kompostierung und Recycling ist wünschenswert!"
        bot.send_message(call.message.chat.id, ans)
    elif call.data == "cb_bio":
        ans = "Biomülltonne (braun/grün):  In die Biotonne gehören alle organischen Abfälle aus Küche und Garten.  Das sind zum Beispiel Obst- und Gemüsereste, Kaffeesatz, Teebeutel (ohne Metallklammern),  Rasenschnitt,  Blumen,  Laub etc.  Kein Plastik oder sonstiger Müll darf beigemischt werden."
        bot.send_message(call.message.chat.id, ans)
    elif call.data == "cb_sack":
        ans = "Gelbe Tonne/Gelber Sack (gelb):  Hier werden Verpackungen aus Plastik, Metall und Verbundstoffen gesammelt.  Beispiele sind Plastikflaschen,  Konservendosen,  Alufolien,  Plastiktüten (meistens),  Tetrapaks etc.  Bitte beachten Sie die jeweiligen regionalen Vorgaben, da diese variieren können.  Oftmals müssen die Verpackungen gespült und ggf. zerkleinert werden."
        bot.send_message(call.message.chat.id, ans)
    elif call.data == "cb_andere":
        ans = "Es gibt regional auch noch weitere Tonnenarten, z.B. für Glas (meistens separate Container),  Sperrmüll (auf Anfrage)  oder Sondermüll (z.B. Batterien,  Leuchtmittel).  Informieren Sie sich bitte bei Ihrer Gemeinde oder Stadt über die genauen Regelungen in Ihrer Region."
        bot.send_message(call.message.chat.id, ans)
    elif call.data == "cb_papier":
        ans = "Papiertonne/Blaue Tonne (blau):  Hier gehören Zeitungen, Zeitschriften, Prospekte, Bücher,  Kartons (flachgedrückt),  Papiertüten etc. hinein.  Verpackungen aus Pappe oder Karton sollten möglichst sauber sein.  Kein beschichtetes Papier oder stark verschmutztes Papier."
        bot.send_message(call.message.chat.id, ans)

@bot.message_handler(func=lambda message: True)
def sift_every_message(message):
    bot.reply_to(message, lambda_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
