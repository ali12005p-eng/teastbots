import telebot
import requests
import os
import time
from telebot import types

BOT_TOKEN = "8994170717:AAF0F9VV4UITSuryt43vYya0AqCqHT0uLTY"
bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://vcdfg.darksidehost.com/so/api.php?url="

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("DEV", url="https://t.me/IMSWAD"))
    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك في بوت تحميل من يوتيوب فقط",
        reply_markup=markup
    )

@bot.message_handler(func=lambda msg: msg.text is not None and ("youtube.com" in msg.text or "youtu.be" in msg.text))
def download_youtube(message):
    url = message.text.strip()
    loading_msg = bot.reply_to(message, "⏳ جاري التحميل...")

    try:
        response = requests.get(API_URL + url)
        if response.status_code == 200:
            data = response.json()
            links = data.get("links", [])

            if not links:
                bot.reply_to(message, "❌ لم يتم العثور على روابط تحميل.")
                return

            video_link = None
            for link in links:
                if link["type"] == "video" and link["ext"] == "mp4":
                    video_link = link["url"]
                    break

            if not video_link:
                bot.reply_to(message, "❌ لم يتم العثور على فيديو مناسب.")
                return

            video_data = requests.get(video_link, stream=True)
            local_filename = "video.mp4"
            with open(local_filename, "wb") as f:
                for chunk in video_data.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)

            time.sleep(2)
            try:
                bot.delete_message(message.chat.id, loading_msg.message_id)
            except:
                pass

            with open(local_filename, "rb") as f:
                bot.send_video(message.chat.id, f, caption="BY: @IMSWAD")

            os.remove(local_filename)
        else:
            bot.reply_to(message, f"❌ حصل خطأ من السيرفر. (Status {response.status_code})")
    except Exception as e:
        bot.reply_to(message, f"⚠️ حصل خطأ: {e}")

print("🤖 البوت شغال...")
bot.infinity_polling()
