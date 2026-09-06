import telebot
import re
import time
from flask import Flask
from threading import Thread

BOT_TOKEN = "8973023915:AAF-oHw-Tl-3wn8JPfZxJjk2CVS3GJLGgKQ"
CHANNEL_ID = "@Mesho_99_deal_"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive and Running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        photo_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ""
        links = re.findall(r'(https?://\S+)', caption)
        link_text = links[0] if links else caption

        post = f"""
🔥 **UNDER ₹99 LOOT DEAL** 🔥

🛒 **Buy Now:**
👉 {link_text}

━━━━━━━━━━━━━━━━━━━━
📢 Join: {CHANNEL_ID}
"""
        bot.send_photo(CHANNEL_ID, photo=photo_id, caption=post, parse_mode="Markdown")
        bot.reply_to(message, "✅ Photo post ho gayi!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    links = re.findall(r'(https?://\S+)', message.text)
    if not links:
        bot.reply_to(message, "⚠️ Link bhejo!")
        return

    bot.reply_to(message, f"⏳ {len(links)} deals post ho rahi hain...")
    for link in links:
        post = f"""
🔥 **NEW LOOT DEAL** 🔥

🛒 **Link:** {link}

━━━━━━━━━━━━━━━━━━━━
📢 Join: {CHANNEL_ID}
"""
        bot.send_message(CHANNEL_ID, post, parse_mode="Markdown")
        time.sleep(1)
    bot.reply_to(message, f"✅ {len(links)} deals post ho gayi!")

# Bot start
keep_alive()
print("Bot starting...")
bot.polling(non_stop=True)
