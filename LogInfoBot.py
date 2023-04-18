import os
import telebot
import pprint

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


API_KEY = os.environ.get("telegrambotAPI_key")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(API_KEY)



def read_last_lines(file_path, num_lines=20):
    with open(file_path, "r") as file:
        lines = file.readlines()
        print("Sent Lines")
        return "\n".join(lines[-num_lines:])
    
@bot.message_handler(commands=['get_lines'])
def send_log_text(message):
    log_file_path = "log.txt"
    if os.path.exists(log_file_path):
        last_lines = read_last_lines(log_file_path, 20)
        bot.reply_to(message, last_lines)
        print("Sent File")
    else:
        print("File nout found")
        bot.reply_to(message, "log.txt file not found")

@bot.message_handler(commands=['get_file'])
def send_log_file(message):
    log_file_path = "log.txt"
    if os.path.exists(log_file_path):
        with open(log_file_path, "rb") as log_file:
            bot.send_document(chat_id=message.chat.id, document=log_file, caption="log.txt")
    else:
        bot.reply_to(message, "log.txt file not found")



# Start the bot
bot.polling()