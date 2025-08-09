import os
from flask import Flask, request
import telebot
from datetime import datetime

API_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)
user_data = {}

def get_streak(user_id):
    if user_id not in user_data:
        return 0
    return (datetime.now().date() - user_data[user_id]['start']).days

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    user_data[user_id] = {'start': datetime.now().date()}
    bot.reply_to(message, "Welcome! Apka streak shuru ho gaya.")

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    streak = get_streak(user_id)
    bot.reply_to(message, f"Aapka current streak: {streak} din.")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.from_user.id
    user_data[user_id] = {'start': datetime.now().date()}
    bot.reply_to(message, "Streak reset kar diya gaya. Shubhkamnaayein dobara shuru karne ke liye!")

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + API_TOKEN)
    return "Webhook set!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
