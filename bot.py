import telebot
from telebot import types
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def health():
    return "Bot is running"

bot = telebot.TeleBot('8745020834:AAHOBXQIyVLT3TPKAKvVS2hJNNgtVyxoqJg')
ADMIN_ID = 8549327132
CHANNEL_USERNAME = "@tehnoprofiLipetsk"
USER_TG = "@Pankovvff"

user_data = {}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status != 'left' and member.status != 'kicked'
    except:
        return False

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📝 Оставить заявку", callback_data="zayavka")
    btn2 = types.InlineKeyboardButton("🏗 СтройБаза", callback_data="stroybaza")
    btn3 = types.InlineKeyboardButton("💰 Прайс", callback_data="price")
    btn4 = types.InlineKeyboardButton("📋 Как мы работаем", callback_data="how_it_works")
    btn5 = types.InlineKeyboardButton("☎️ Контакты", callback_data="kontakty")
    btn6 = types.InlineKeyboardButton("💬 Отзывы", callback_data="reviews")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def get_stroybaza_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🪵 Поддоны", callback_data="stroy_poddony")
    btn2 = types.InlineKeyboardButton("🧱 Кирпич", callback_data="stroy_kirpich")
    btn3 = types.InlineKeyboardButton("💊 Смеси", callback_data="stroy_smesi")
    btn4 = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("📢 Подписаться", url="https://t.me/tehnoprofiLipetsk")
        btn_check = types.InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")
        markup.add(btn_channel)
        markup.add(btn_check)
        bot.send_message(message.chat.id, "👋 Чтобы продолжить, пожалуйста, подпишитесь на наш новостной канал:", reply_markup=markup)
        return

    text = (
        "👋 <b>Добро пожаловать в «ТехноПрофи»!</b>\n\n"
        "🔨 Сервис подбора мастеров + наша <b>СтройБаза</b>!\n"
        "🏗 У нас вы можете купить стройматериалы: поддоны, кирпич, смеси и многое другое!\n\n"
        "💯 Работаем быстро, качественно и с гарантией.\n\n"
        "👇 <b>Выберите действие:</b>"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu(), parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "Спасибо за подписку! ✅")
        text = (
            "👋 <b>Добро пожаловать в «ТехноПрофи»!</b>\n\n"
            "🔨 Сервис подбора мастеров + наша <b>СтройБаза</b>!\n"
            "🏗 У нас вы можете купить стройматериалы: поддоны, кирпич, смеси и многое другое!\n\n"
            "💯 Работаем быстро, качественно и с гарантией.\n\n"
            "👇 <b>Выберите действие:</b>"
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_main_menu(), parse_mode='HTML')
    else:
        bot.answer_callback_query(call.id, "Вы еще не подписались на канал!", show_alert=True)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "zayavka":
        text = "🧰 <b>Какие услуги вам нужны?</b>\n\nВыберите вариант из списка:"
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("🛠 Разнорабочие", callback_data="usluga_raznorab")
        btn2 = types.InlineKeyboardButton("🔨 Демонтаж", callback_data="usluga_demontazh")
        btn3 = types.InlineKeyboardButton("🚛 Вывоз мусора", callback_data="usluga_musor")
        btn4 = types.InlineKeyboardButton("🌿 Покос травы", callback_data="usluga_pokos")
        btn5 = types.InlineKeyboardButton("📝 Свой вариант", callback_data="usluga_svoy")
        btn6 = types.InlineKeyboardButton("📦 Уборка территории", callback_data="usluga_uborka")
        btn7 = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "stroybaza":
        bot.edit_message_text("🏗 <b>СтройБаза!</b>\n\nВыберите, что вас интересует:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_m