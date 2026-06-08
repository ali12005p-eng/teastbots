#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

import telebot
from telebot import types
import random
from PIL import Image, ImageDraw, ImageFont
import os
import logging
import arabic_reshaper
from bidi.algorithm import get_display
import sqlite3
import time
from datetime import datetime

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

TOKEN = '000000'
AbuHamza = [7598650992] 
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def init_db():
    conn = sqlite3.connect('abuHamza.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        join_date TEXT,
        usage_count INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel_id INTEGER PRIMARY KEY,
        channel_username TEXT,
        channel_title TEXT,
        add_date TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        maintenance_mode INTEGER DEFAULT 0
    )
    ''')
    
    cursor.execute('INSERT OR IGNORE INTO settings (id) VALUES (1)')
    
    conn.commit()
    conn.close()

init_db()

ARABIC_NAMES = [
    "Ⲁⲃⲇⲁⲗⲗⲁⲏ", "Ⲛⲟⲟⲣ", "Ⲙⲟⲏⲙⲉⲇ", "Ⲙⲟⲩⲛⲉⲉⲣ", "Ⲁⲏⲙⲉⲇ", 
    "Ⲥⲁⲣⲁ", "Ⲙⲁⲣⲩⲁⲙ", "Ⲇⲁⲗⲓⲁ", "Ⲙⲓ", "Ⲛⲟⲩⲣⲁⲗⲏⲕ",
    "Ⲥⲉⲙ", "Ⲙⲓⲇⲓ", "Ⲣⲁⲙⲟ", "Ⲙⲓⲭⲁⲉⲗ", "Ⲁⲙⲓⲣ",
    "Ⲙⲓⲥⲁ", "Ⲙⲓⲥⲧⲓ", "Ⲙⲓⲥⲧⲁ", "Ⲙⲓⲥⲧⲟ", "Ⲙⲓⲥⲧⲓ"
]

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

ENGLISH_NAMES = [
    "𝕁𝕠𝕙𝕟", "𝕄𝕒𝕣𝕪", "𝔻�𝕧𝕚𝕕", "𝕊𝕒𝕣𝕒𝕟", "𝔸𝕞𝕖𝕝𝕚𝕒", 
    "𝕄𝕚𝕔𝕙𝕒𝕖𝕝", "𝔼𝕞𝕞𝕒", "𝕁𝕒𝕗𝕒𝕣", "𝕃𝕚𝕝𝕪", "ℝ𝕠𝕓𝕖𝕣𝕥",
    "𝕆𝕝𝕚𝕧𝕚𝕒", "𝕎𝕚𝕝𝕝𝕚𝕒𝕞", "𝕊𝕠𝕙𝕒", "ℍ𝕖𝕟𝕣𝕪", "ℂ�𝕙𝕒𝕣𝕝𝕠𝕥𝕥𝕖",
    "𝔾𝕖𝕠𝕣𝕘𝕖", "𝔸𝕞𝕖𝕝𝕚𝕖", "𝕋𝕙𝕠𝕞𝕒𝕤", "ℂ𝕙𝕒𝕣𝕝𝕖𝕤", "𝔼𝕝𝕖𝕒𝕟𝕠𝕣"
]

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

ARABIC_DECORATIONS = [
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}")),
    lambda text: get_display(arabic_reshaper.reshape(f"{text}"))
]

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

ENGLISH_DECORATIONS = [
    lambda text: f"𝔽𝕒𝕟𝕔𝕪: {text}",
    lambda text: f"𝕋𝕖𝕩𝕥: {text}",
    lambda text: f"🅂🅃🄰🅁: {text}",
    lambda text: f"𝓢𝔀𝓲𝓼𝓱: {text}",
    lambda text: f"𝕊𝕡𝕖𝕔𝕚𝕒𝕝: {text}",
    lambda text: f"Ⓒⓞⓞⓛ: {text}",
    lambda text: f"Ｔｈｉｃｋ: {text}",
    lambda text: f"🅂🄽🄰🅉🅉🅈: {text}",
    lambda text: f"𝕊𝕥𝕪𝕝𝕚𝕤𝕙: {text}",
    lambda text: f"🄵🄰🄽🄲🅈: {text}",
    lambda text: f"𝕲𝖑𝖆𝖒𝖔𝖗: {text}",
    lambda text: f"𝔻𝕖𝕝𝕦𝕩𝕖: {text}",
    lambda text: f"✧⋄⋆⋅⋆⋄✧: {text}",
    lambda text: f"✞𝓓𝓪𝓻𝓴✞: {text}",
    lambda text: f"★彡{text}彡★",
    lambda text: f"『{text}』",
    lambda text: f"≪{text}≫",
    lambda text: f"〖{text}〗",
    lambda text: f"⧼{text}⧽",
    lambda text: f"『☆』{text}『☆』",
    lambda text: f"✾ {text} ✾",
    lambda text: f"✧･ﾟ: *✧･ﾟ:* {text} *:･ﾟ✧*:･ﾟ✧",
    lambda text: f"☽ {text} ☾",
    lambda text: f"♡ {text} ♡"
]

user_states = {}
current_page = {}

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def is_admin(user_id):
    return user_id in AbuHamza

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def get_user_info(user_id):
    conn = sqlite3.connect('abuHamza.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def update_user_usage(user_id):
    conn = sqlite3.connect('abuHamza.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        user_info = bot.get_chat(user_id)
        username = user_info.username if user_info.username else ""
        first_name = user_info.first_name if user_info.first_name else ""
        last_name = user_info.last_name if user_info.last_name else ""
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
        INSERT INTO users (user_id, username, first_name, last_name, join_date, usage_count)
        VALUES (?, ?, ?, ?, ?, 1)
        ''', (user_id, username, first_name, last_name, join_date))
    else:
        cursor.execute('UPDATE users SET usage_count = usage_count + 1 WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def check_subscription(user_id):
    conn = sqlite3.connect('abuHamza.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM channels')
    channels = cursor.fetchall()
    conn.close()
    
    if not channels:
        return True 
    
    for channel in channels:
        try:
            chat_member = bot.get_chat_member(channel[0], user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            logger.error(f"Error checking subscription: {e}")
            continue
    
    return True

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def is_maintenance_mode():
    conn = sqlite3.connect('abuHamza.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT maintenance_mode FROM settings WHERE id = 1')
    mode = cursor.fetchone()[0]
    conn.close()
    return mode == 1

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def create_logo(name):
    try:
        width, height = 800, 400
        bg_color = (random.randint(50, 200), (random.randint(50, 200)), (random.randint(50, 200))
        gradient = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(gradient)
        
        for i in range(width):
            r = bg_color[0] + int((255 - bg_color[0]) * i / width)
            g = bg_color[1] + int((255 - bg_color[1]) * i / width)
            b = bg_color[2] + int((255 - bg_color[2]) * i / width)
            draw.line((i, 0, i, height), fill=(r, g, b))
        
        try:
            font = ImageFont.truetype("ffjff5.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text_width, text_height = draw.textsize(name, font=font)
        
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        
        text_color = (255, 255, 255)
        
        draw.text((x+2, y+2), name, fill=(0, 0, 0), font=font)
        draw.text((x, y), name, fill=text_color, font=font)
        
        draw.rectangle([x-10, y-10, x+text_width+10, y+text_height+10], outline=(255, 255, 255), width=3)
        
        logo_path = f"logo_{name}.png"
        gradient.save(logo_path)
        
        return logo_path
    except Exception as e:
        logger.error(f"Error creating logo: {e}")
        return None

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        
        if is_maintenance_mode() and not is_admin(user_id):
            bot.send_message(message.chat.id, "⛔ البوت في وضع الصيانة حالياً. الرجاء المحاولة لاحقاً.")
            return
        
        if not check_subscription(user_id):
            channels = get_mandatory_channels()
            if channels:
                markup = types.InlineKeyboardMarkup()
                for channel in channels:
                    markup.add(types.InlineKeyboardButton(f"{channel[2]}", url=f"https://t.me/{channel[1]}"))
                markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))
                bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات التالية لاستخدام البوت:", reply_markup=markup)
                return
        
        update_user_usage(user_id)
        user_states[user_id] = None
        current_page[user_id] = {'arabic': 0, 'english': 0}
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_names = types.InlineKeyboardButton("🎭 أسماء جاهزة", callback_data="ready_names")
        btn_decorate = types.InlineKeyboardButton("✨ زخرفة نص", callback_data="decorate_text")
        btn_logo = types.InlineKeyboardButton("🖼 تصميم لوجو", callback_data="design_logo")
        
        dev = types.InlineKeyboardButton("Abu Hamza", url="t.me/ffjff5")
            channel = types.InlineKeyboardButton("EgyCodes", url="t.me/EgyCodes")
        
        markup.add(btn_names, btn_decorate)
        markup.add(btn_logo)
        markup.add(dev, channel)
        welcome_msg = """
🎉 *مرحباً بك في بوت زخرفة ابو حمزه*

_المميزات_ :

• زخرفة عربي
• زخرفة انجليزي
• 42 ~ 10 اشكال زخرفة
• تصميم لوجو بإسم
• اسماء جاهزه
---------------------------------------------------------
اختر أحد الخيارات من الأسفل للبدء
        """
        
        bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in send_welcome: {e}")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    try:
        user_id = message.from_user.id
        if not is_admin(user_id):
            return
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        btn_ban = types.InlineKeyboardButton("حظر مستخدم", callback_data="admin_ban")
        btn_unban = types.InlineKeyboardButton("إلغاء حظر", callback_data="admin_unban")
        markup.add(btn_ban, btn_unban)
        
        btn_stats = types.InlineKeyboardButton("الإحصائيات", callback_data="admin_stats")
        btn_broadcast = types.InlineKeyboardButton("اذاعة", callback_data="admin_broadcast")
        markup.add(btn_stats, btn_broadcast)
        
        btn_top_users = types.InlineKeyboardButton("تريند المستخدمين", callback_data="admin_top_users")
        btn_add_channel = types.InlineKeyboardButton("إضافة قناة", callback_data="admin_add_channel")
        markup.add(btn_top_users, btn_add_channel)
        
        btn_remove_channel = types.InlineKeyboardButton("حذف قناة", callback_data="admin_remove_channel")
        btn_list_channels = types.InlineKeyboardButton("قنوات الاشتراك الاجباري", callback_data="admin_list_channels")
        markup.add(btn_remove_channel, btn_list_channels)
        
        btn_maintenance_on = types.InlineKeyboardButton("تفعيل الصيانة", callback_data="admin_maintenance_on")
        btn_maintenance_off = types.InlineKeyboardButton("تعطيل الصيانة", callback_data="admin_maintenance_off")
        markup.add(btn_maintenance_on, btn_maintenance_off)
        
        admin_msg = """
⚙️ *لوحة التحكم الإدارية*

اختر أحد الخيارات لإدارة البوت
        """
        
        bot.send_message(message.chat.id, admin_msg, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in admin_panel: {e}")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        
        if call.data == "check_subscription":
            if check_subscription(user_id):
                bot.delete_message(chat_id, call.message.message_id)
                send_welcome(call.message)
            else:
                bot.answer_callback_query(call.id, "⛔ لم تشترك في جميع القنوات المطلوبة بعد", show_alert=True)
            return
        
        if not call.data.startswith("admin_") and not is_admin(user_id):
            if is_maintenance_mode():
                bot.answer_callback_query(call.id, "⛔ البوت في وضع الصيانة حالياً.", show_alert=True)
                return
            
            if not check_subscription(user_id):
                channels = get_mandatory_channels()
                if channels:
                    markup = types.InlineKeyboardMarkup()
                    for channel in channels:
                        markup.add(types.InlineKeyboardButton(f"{channel[2]}", url=f"https://t.me/{channel[1]}"))
                    markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))
                    bot.edit_message_text("⚠️ يجب الاشتراك في القنوات التالية لاستخدام البوت:", chat_id, call.message.message_id, reply_markup=markup)
                    return
        
        if call.data == "ready_names":
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_arabic = types.InlineKeyboardButton("🇸🇦 عربية", callback_data="arabic_names")
            btn_english = types.InlineKeyboardButton("🇬🇧 إنجليزية", callback_data="english_names")
            btn_back = types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")
            
            markup.add(btn_arabic, btn_english, btn_back)
            
            bot.edit_message_text("📜 *اختر نوع الأسماء المزخرفة*", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
        elif call.data == "arabic_names":
            show_names_page(user_id, chat_id, call.message.message_id, 'arabic')
        
        elif call.data == "english_names":
            show_names_page(user_id, chat_id, call.message.message_id, 'english')
        
        elif call.data == "back_to_start":
            user_states[user_id] = None
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_names = types.InlineKeyboardButton("🎭 أسماء جاهزة", callback_data="ready_names")
            btn_decorate = types.InlineKeyboardButton("✨ زخرفة نص", callback_data="decorate_text")
            btn_logo = types.InlineKeyboardButton("🖼 تصميم لوجو", callback_data="design_logo")
            
            dev = types.InlineKeyboardButton("Abu Hamza", url="t.me/ffjff5")
            channel = types.InlineKeyboardButton("EgyCodes", url="t.me/EgyCodes")
            
            markup.add(btn_names, btn_decorate)
            markup.add(btn_logo)
            markup.add(dev, channel)
            
            welcome_msg = """
🎉 *مرحباً بك في بوت زخرفة ابو حمزه*

_المميزات_ :

• زخرفة عربي
• زخرفة انجليزي
• 42 ~ 10 اشكال زخرفة
• تصميم لوجو بإسم
• اسماء جاهزه
---------------------------------------------------------
اختر أحد الخيارات من الأسفل للبدء
            """
            
            bot.edit_message_text(welcome_msg, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
        elif call.data == "next_page_arabic":
            current_page[user_id]['arabic'] += 1
            show_names_page(user_id, chat_id, call.message.message_id, 'arabic')
        
        elif call.data == "prev_page_arabic":
            if current_page[user_id]['arabic'] > 0:
                current_page[user_id]['arabic'] -= 1
                show_names_page(user_id, chat_id, call.message.message_id, 'arabic')
        
        elif call.data == "next_page_english":
            current_page[user_id]['english'] += 1
            show_names_page(user_id, chat_id, call.message.message_id, 'english')
        
        elif call.data == "prev_page_english":
            if current_page[user_id]['english'] > 0:
                current_page[user_id]['english'] -= 1
                show_names_page(user_id, chat_id, call.message.message_id, 'english')
        
        elif call.data == "decorate_text":
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_arabic = types.InlineKeyboardButton("🇸🇦 عربية", callback_data="decorate_arabic")
            btn_english = types.InlineKeyboardButton("🇬🇧 إنجليزية", callback_data="decorate_english")
            btn_back = types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")
            
            markup.add(btn_arabic, btn_english)
            markup.add(btn_back)
            
            bot.edit_message_text("🎨 *اختر نوع الزخرفة الذي تريده*", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
        elif call.data == "decorate_arabic":
            user_states[user_id] = 'waiting_for_text_arabic'
            msg = bot.send_message(chat_id, "📝 *أرسل النص العربي الذي تريد زخرفته*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_text_for_decoration, 'arabic')
        
        elif call.data == "decorate_english":
            user_states[user_id] = 'waiting_for_text_english'
            msg = bot.send_message(chat_id, "📝 *أرسل النص الإنجليزي الذي تريد زخرفته*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_text_for_decoration, 'english')
        
        elif call.data == "design_logo":
            user_states[user_id] = 'waiting_for_logo_text'
            msg = bot.send_message(chat_id, "🎨 *أرسل النص الذي تريد تصميم لوجو به:*\n(يمكنك استخدام العربية أو الإنجليزية)", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_logo_text)
        
        # الأوامر الإدارية
        elif call.data == "admin_ban":
            msg = bot.send_message(chat_id, "⛔ *أرسل آيدي المستخدم لحظره*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_ban_user)
        
        elif call.data == "admin_unban":
            msg = bot.send_message(chat_id, "🔓 *أرسل آيدي المستخدم لإلغاء حظره*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_unban_user)
        
        elif call.data == "admin_stats":
            show_bot_stats(chat_id)
        
        elif call.data == "admin_broadcast":
            msg = bot.send_message(chat_id, "📢 *أرسل الرسالة التي تريد إرسالها لجميع المستخدمين*\n(يمكنك استخدام الصور والنصوص)", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_broadcast_message)
        
        elif call.data == "admin_top_users":
            show_top_users(chat_id)
        
        elif call.data == "admin_add_channel":
            msg = bot.send_message(chat_id, "*أرسل يوزر القناة لإضافتها للاشتراك الإجباري*\n(يجب أن يكون البوت مشرفاً في القناة)", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_add_channel)
        
        elif call.data == "admin_remove_channel":
            show_channels_for_removal(chat_id)
        
        elif call.data == "admin_list_channels":
            list_mandatory_channels(chat_id)
        
        elif call.data == "admin_maintenance_on":
            set_maintenance_mode(True, chat_id, call.message.message_id)
        
        elif call.data == "admin_maintenance_off":
            set_maintenance_mode(False, chat_id, call.message.message_id)
        
        elif call.data.startswith("remove_channel_"):
            channel_id = int(call.data.split("_")[2])
            remove_mandatory_channel(channel_id, chat_id, call.message.message_id)
    
    except Exception as e:
        logger.error(f"Error in callback_query: {e}")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def show_names_page(user_id, chat_id, message_id, lang):
    try:
        names = ARABIC_NAMES if lang == 'arabic' else ENGLISH_NAMES
        page = current_page[user_id][lang]
        items_per_page = 5
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        
        if start_idx >= len(names):
            current_page[user_id][lang] = 0
            start_idx = 0
            end_idx = items_per_page
        
        current_names = names[start_idx:end_idx]
        
        markup = types.InlineKeyboardMarkup()
        
        for name in current_names:
            markup.add(types.InlineKeyboardButton(name, callback_data=f"name_{name}"))
        
        btn_row = []
        if page > 0:
            btn_row.append(types.InlineKeyboardButton("◀ السابق", callback_data=f"prev_page_{lang}"))
        
        if len(names) > end_idx:
            btn_row.append(types.InlineKeyboardButton("التالي ▶", callback_data=f"next_page_{lang}"))
        
        if btn_row:
            markup.add(*btn_row)
        
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="ready_names"))
        
        bot.edit_message_text(f"Channel @EgyCodes", 
                             chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in show_names_page: {e}")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def process_text_for_decoration(message, lang):
    try:
        user_id = message.from_user.id
        
        if is_maintenance_mode() and not is_admin(user_id):
            bot.send_message(message.chat.id, "⛔ البوت في وضع الصيانة حالياً. الرجاء المحاولة لاحقاً.")
            return
        
        if not check_subscription(user_id):
            channels = get_mandatory_channels()
            if channels:
                markup = types.InlineKeyboardMarkup()
                for channel in channels:
                    markup.add(types.InlineKeyboardButton(f"{channel[2]}", url=f"https://t.me/{channel[1]}"))
                markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))
                bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات التالية لاستخدام البوت:", reply_markup=markup)
                return
        
        update_user_usage(user_id)
        text = message.text
        
        if lang == 'arabic':
            decorations = ARABIC_DECORATIONS
            bot.send_message(message.chat.id, "⏳ *جاري زخرفة النص العربي...*", parse_mode="Markdown")
        else:
            decorations = ENGLISH_DECORATIONS
            bot.send_message(message.chat.id, "⏳ *جاري زخرفة النص الإنجليزي...*", parse_mode="Markdown")
        
        time.sleep(1)
        
        for i, decorate_func in enumerate(decorations[:14 if lang == 'arabic' else 24]):
            decorated_text = decorate_func(text)
            bot.send_message(message.chat.id, f"`{decorated_text}`", parse_mode="Markdown")
        
        user_states[user_id] = None
    except Exception as e:
        logger.error(f"Error in process_text_for_decoration: {e}")
        bot.send_message(message.chat.id, "⚠️ *حدث خطأ أثناء زخرفة النص. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def process_logo_text(message):
    try:
        user_id = message.from_user.id
        
        if is_maintenance_mode() and not is_admin(user_id):
            bot.send_message(message.chat.id, "⛔ البوت في وضع الصيانة حالياً. الرجاء المحاولة لاحقاً.")
            return
        
        if not check_subscription(user_id):
            channels = get_mandatory_channels()
            if channels:
                markup = types.InlineKeyboardMarkup()
                for channel in channels:
                    markup.add(types.InlineKeyboardButton(f"{channel[2]}", url=f"https://t.me/{channel[1]}"))
                markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))
                bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات التالية لاستخدام البوت:", reply_markup=markup)
                return
        
        update_user_usage(user_id)
        text = message.text
        
        bot.send_message(message.chat.id, "⏳ *جاري تصميم اللوجو...*", parse_mode="Markdown")
        logo_path = create_logo(text)
        
        if logo_path:
            with open(logo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=f"Channel *@EgyCodes*", parse_mode="Markdown")
            os.remove(logo_path)
        else:
            bot.send_message(message.chat.id, "⚠️ *عذراً، حدث خطأ أثناء إنشاء اللوجو. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")
        
        user_states[user_id] = None
    except Exception as e:
        logger.error(f"Error in process_logo_text: {e}")
        bot.send_message(message.chat.id, "⚠️ *حدث خطأ أثناء إنشاء اللوجو. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def process_ban_user(message):
    try:
        if not is_admin(message.from_user.id):
            return
        
        try:
            user_id = int(message.text)
            conn = sqlite3.connect('abuHamza.sqlite')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            
            bot.send_message(message.chat.id, f"✅ *تم حظر المستخدم* `{user_id}` *بنجاح.*", parse_mode="Markdown")
        except ValueError:
            bot.send_message(message.chat.id, "⚠️ *الرجاء إدخال آيدي مستخدم صحيح.*", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in process_ban_user: {e}")
        bot.send_message(message.chat.id, "⚠️ *حدث خطأ أثناء عملية الحظر. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def process_unban_user(message):
    try:
        if not is_admin(message.from_user.id):
            return
        
        try:
            user_id = int(message.text)
            conn = sqlite3.connect('abuHamza.sqlite')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            
            bot.send_message(message.chat.id, f"✅ *تم إلغاء حظر المستخدم* `{user_id}` *بنجاح.*", parse_mode="Markdown")
        except ValueError:
            bot.send_message(message.chat.id, "⚠️ *الرجاء إدخال آيدي مستخدم صحيح.*", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in process_unban_user: {e}")
        bot.send_message(message.chat.id, "⚠️ *حدث خطأ أثناء عملية إلغاء الحظر. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def show_bot_stats(chat_id):
    try:
        conn = sqlite3.connect('abuHamza.sqlite')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE usage_count > 2')
        active_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
        banned_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(usage_count) FROM users')
        total_usage = cursor.fetchone()[0] or 0
        
        conn.close()
        
        stats_msg = f"""
📊 *إحصائيات البوت:*

👥 *إجمالي المستخدمين:* `{total_users}`
🚀 *المستخدمون النشطون:* `{active_users}`
⛔ *المستخدمون المحظورون:* `{banned_users}`
🔢 *إجمالي استخدامات البوت:* `{total_usage}`
        """
        
        bot.send_message(chat_id, stats_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in show_bot_stats: {e}")
        bot.send_message(chat_id, "⚠️ *حدث خطأ أثناء جلب الإحصائيات. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def process_broadcast_message(message):
    try:
        if not is_admin(message.from_user.id):
            return
        
        bot.send_message(message.chat.id, "⏳ *جاري إرسال الاذاعة لجميع المستخدمين...*", parse_mode="Markdown")
        
        conn = sqlite3.connect('abuHamza.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE is_banned = 0')
        users = cursor.fetchall()
        conn.close()
        
        success = 0
        failed = 0
        
        for user in users:
            try:
                if message.content_type == 'text':
                    bot.send_message(user[0], message.text, parse_mode="Markdown")
                elif message.content_type == 'photo':
                    bot.send_photo(user[0], message.photo[-1].file_id, caption=message.caption, parse_mode="Markdown")
                success += 1
            except Exception as e:
                logger.error(f"Error sending to user {user[0]}: {e}")
                failed += 1
            time.sleep(0.1) 
        
        bot.send_message(message.chat.id, f"""
✅ *تم إرسال الاذاعة بنجاح:*
✔ *تم الإرسال بنجاح لـ:* `{success}` مستخدم
✖ *فشل الإرسال لـ:* `{failed}` مستخدم
        """, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in process_broadcast_message: {e}")
        bot.send_message(message.chat.id, "⚠️ *حدث خطأ أثناء إرسال الإشعار. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def show_top_users(chat_id):
    try:
        conn = sqlite3.connect('abuHamza.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username, first_name, usage_count FROM users WHERE is_banned = 0 ORDER BY usage_count DESC LIMIT 5')
        top_users = cursor.fetchall()
        conn.close()
        
        if not top_users:
            bot.send_message(chat_id, "⚠️ *لا توجد بيانات عن المستخدمين بعد.*", parse_mode="Markdown")
            return
        
        top_msg = "🏆 *أكثر 5 مستخدمين نشاطاً*\n\n"
        for i, user in enumerate(top_users):
            username = f"@{user[1]}" if user[1] else f" {user[0]}"
            name = user[2] if user[2] else "بدون يوزر"
            top_msg += f"{i+1}. {name} ({username}) - {user[3]} استخدام\n"
        
        bot.send_message(chat_id, top_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in show_top_users: {e}")
        bot.send_message(chat_id, "⚠️ *حدث خطأ أثناء جلب قائمة المستخدمين. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def process_add_channel(message):
    try:
        if not is_admin(message.from_user.id):
            return
        
        channel_input = message.text.strip()
        
        try:
            channel_id = int(channel_input)
            try:
                chat = bot.get_chat(channel_id)
            except Exception as e:
                bot.send_message(message.chat.id, "⚠️ *لم يتم العثور على القناة. تأكد من أن البوت مشرف فيها.*", parse_mode="Markdown")
                return
        except ValueError:
            if channel_input.startswith("@"):
                channel_input = channel_input[1:]
            try:
                chat = bot.get_chat(f"@{channel_input}")
            except Exception as e:
                bot.send_message(message.chat.id, "⚠️ *لم يتم العثور على القناة. تأكد من أن البوت مشرف فيها.*", parse_mode="Markdown")
                return
        
        try:
            bot.get_chat_member(chat.id, bot.get_me().id)
        except Exception as e:
            bot.send_message(message.chat.id, "⚠️ *البوت ليس مشرف في هذه القناة. يرجى ترقيته أولاً.*", parse_mode="Markdown")
            return
        
        conn = sqlite3.connect('abuHamza.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO channels (channel_id, channel_username, channel_title, add_date) VALUES (?, ?, ?, ?)',
                      (chat.id, chat.username, chat.title, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, f"✅ *تمت إضافة قناة* `{chat.title}` *للاشتراك الإجباري بنجاح.*", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in process_add_channel: {e}")
        bot.send_message(message.chat.id, "⚠️ *حدث خطأ أثناء إضافة القناة. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def show_channels_for_removal(chat_id):
    try:
        channels = get_mandatory_channels()
        if not channels:
            bot.send_message(chat_id, "⚠️ *لا توجد قنوات للاشتراك الإجباري.*", parse_mode="Markdown")
            return
        
        markup = types.InlineKeyboardMarkup()
        for channel in channels:
            markup.add(types.InlineKeyboardButton(f"حذف {channel[2]}", callback_data=f"remove_channel_{channel[0]}"))
        
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin"))
        
        bot.send_message(chat_id, "*اختر القناة التي تريد حذفها من الاشتراك الاجباري*", reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in show_channels_for_removal: {e}")
        bot.send_message(chat_id, "⚠️ *حدث خطأ أثناء جلب القنوات. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def remove_mandatory_channel(channel_id, chat_id, message_id):
    try:
        conn = sqlite3.connect('abuHamza.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT channel_title FROM channels WHERE channel_id = ?', (channel_id,))
        channel_title = cursor.fetchone()[0]
        cursor.execute('DELETE FROM channels WHERE channel_id = ?', (channel_id,))
        conn.commit()
        conn.close()
        
        bot.edit_message_text(f"✅ *تم حذف قناة* `{channel_title}` *من الاشتراك الإجباري بنجاح.*", 
                            chat_id, message_id, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in remove_mandatory_channel: {e}")
        bot.edit_message_text("⚠️ *حدث خطأ أثناء حذف القناة. يرجى المحاولة مرة أخرى.*", 
                            chat_id, message_id, parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def list_mandatory_channels(chat_id):
    try:
        channels = get_mandatory_channels()
        if not channels:
            bot.send_message(chat_id, "⚠️ *لا توجد قنوات للاشتراك الإجباري.*", parse_mode="Markdown")
            return
        
        channels_msg = "📋 *قنوات الاشتراك الإجباري المضافة الى البوت*\n\n"
        for channel in channels:
            channels_msg += f"- {channel[2]} (@{channel[1]})\n"
        
        bot.send_message(chat_id, channels_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in list_mandatory_channels: {e}")
        bot.send_message(chat_id, "⚠️ *حدث خطأ أثناء جلب القنوات. يرجى المحاولة مرة أخرى.*", parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def get_mandatory_channels():
    conn = sqlite3.connect('abuHamza.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id, channel_username, channel_title FROM channels')
    channels = cursor.fetchall()
    conn.close()
    return channels

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

def set_maintenance_mode(enable, chat_id, message_id):
    try:
        conn = sqlite3.connect('abuHamza.sqlite')
        cursor = conn.cursor()
        cursor.execute('UPDATE settings SET maintenance_mode = ? WHERE id = 1', (1 if enable else 0,))
        conn.commit()
        conn.close()
        
        status = "✅ *تم تفعيل وضع الصيانة*" if enable else "✅ *تم تعطيل وضع الصيانة*"
        bot.edit_message_text(status, chat_id, message_id, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in set_maintenance_mode: {e}")
        bot.edit_message_text("⚠️ *حدث خطأ أثناء تعديل وضع الصيانة. يرجى المحاولة مرة أخرى.*", 
                            chat_id, message_id, parse_mode="Markdown")

#البوت كتابة المبرمج ابو حمزه

#يوزر المبرمج @FFJFF5

#قناة المبرمج @FileeCode

if __name__ == '__main__':
    try:
        logger.info("Starting bot...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error in main: {e}")