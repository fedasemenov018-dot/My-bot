import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

# Токен и ID админа
TOKEN = "8745020834:AAHlDdroqkuhDJkbG4Qqtu72pnGmgVHWcvg"
ADMIN_ID = 8549327132
CHANNEL_ID = "@tehnoprofiLipetsk"

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Инициализация Flask
app = Flask(__name__)

# Хранилище данных пользователей
user_data = {}

# Услуги
SERVICES = {
    "Разнорабочие": "raznorabochie",
    "Демонтаж": "demontazh",
    "Вывоз мусора": "vyvoz_musora",
    "Покос травы": "pokos_travy"
}

# ======================== КОМАНДЫ ЗАПУСКА ========================

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {
        "service": None,
        "name": None,
        "phone": None,
        "address": None,
        "time": None
    }
    
    # Проверка подписки на канал
    try:
        member = bot.get_chat_member(CHANNEL_ID, chat_id)
        if member.status == "left":
            send_subscribe_message(chat_id)
            return
    except:
        send_subscribe_message(chat_id)
        return
    
    send_main_menu(chat_id)

# ======================== ПРОВЕРКА ПОДПИСКИ ========================

def send_subscribe_message(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_ID[1:]}"))
    markup.add(InlineKeyboardButton("Я подписался ✓", callback_data="check_subscription"))
    
    bot.send_message(
        chat_id,
        f"👋 Добро пожаловать!\n\n"
        f"Для использования бота необходимо подписаться на канал {CHANNEL_ID}\n\n"
        f"После подписки нажмите кнопку ниже.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    chat_id = call.message.chat.id
    
    try:
        member = bot.get_chat_member(CHANNEL_ID, chat_id)
        if member.status != "left":
            bot.answer_callback_query(call.id, "✓ Спасибо за подписку!", show_alert=False)
            bot.delete_message(chat_id, call.message.message_id)
            send_main_menu(chat_id)
        else:
            bot.answer_callback_query(call.id, "❌ Вы ещё не подписались на канал", show_alert=True)
    except:
        bot.answer_callback_query(call.id, "❌ Ошибка проверки подписки", show_alert=True)

# ======================== ГЛАВНОЕ МЕНЮ ========================

def send_main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    
    for service, callback_data in SERVICES.items():
        markup.add(InlineKeyboardButton(service, callback_data=f"service_{callback_data}"))
    
    bot.send_message(
        chat_id,
        "🔧 Выберите услугу:",
        reply_markup=markup
    )

# ======================== ОБРАБОТКА ВЫБОРА УСЛУГИ ========================

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def choose_service(call):
    chat_id = call.message.chat.id
    service_key = call.data.replace("service_", "")
    
    # На��ти название услуги по ключу
    service_name = None
    for name, key in SERVICES.items():
        if key == service_key:
            service_name = name
            break
    
    if service_name:
        user_data[chat_id]["service"] = service_name
        bot.answer_callback_query(call.id)
        bot.delete_message(chat_id, call.message.message_id)
        
        ask_name(chat_id)

# ======================== СБОР ДАННЫХ ========================

def ask_name(chat_id):
    msg = bot.send_message(chat_id, "📝 Введите ваше имя:")
    bot.register_next_step_handler(msg, process_name, chat_id)

def process_name(message, chat_id):
    if message.chat.id != chat_id:
        return
    
    name = message.text.strip()
    if len(name) < 2:
        msg = bot.send_message(chat_id, "❌ Имя должно содержать хотя бы 2 символа. Попробуйте ещё раз:")
        bot.register_next_step_handler(msg, process_name, chat_id)
        return
    
    user_data[chat_id]["name"] = name
    ask_phone(chat_id)

def ask_phone(chat_id):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(KeyboardButton("📱 Отправить номер телефона", request_contact=True))
    
    msg = bot.send_message(chat_id, "📞 Поделитесь вашим номером телефона:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_phone, chat_id)

def process_phone(message, chat_id):
    if message.chat.id != chat_id:
        return
    
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text.strip()
    
    if not phone or len(phone) < 10:
        msg = bot.send_message(chat_id, "❌ Некорректный номер. Попробуйте ещё раз:")
        bot.register_next_step_handler(msg, process_phone, chat_id)
        return
    
    user_data[chat_id]["phone"] = phone
    ask_address(chat_id)

def ask_address(chat_id):
    msg = bot.send_message(chat_id, "📍 Введите адрес выполнения работ:")
    bot.register_next_step_handler(msg, process_address, chat_id)

def process_address(message, chat_id):
    if message.chat.id != chat_id:
        return
    
    address = message.text.strip()
    if len(address) < 5:
        msg = bot.send_message(chat_id, "❌ Адрес слишком короткий. Попробуйте ещё раз:")
        bot.register_next_step_handler(msg, process_address, chat_id)
        return
    
    user_data[chat_id]["address"] = address
    ask_time(chat_id)

def ask_time(chat_id):
    msg = bot.send_message(chat_id, "⏰ Введите удобное время (например: 10:00, 14:30 или завтра в 15:00):")
    bot.register_next_step_handler(msg, process_time, chat_id)

def process_time(message, chat_id):
    if message.chat.id != chat_id:
        return
    
    time_str = message.text.strip()
    if len(time_str) < 3:
        msg = bot.send_message(chat_id, "❌ Некорректное время. Попробуйте ещё раз:")
        bot.register_next_step_handler(msg, process_time, chat_id)
        return
    
    user_data[chat_id]["time"] = time_str
    send_confirmation(chat_id)

# ======================== ПОДТВЕРЖДЕНИЕ И ОТПРАВКА АДМИНУ ========================

def send_confirmation(chat_id):
    data = user_data[chat_id]
    
    confirmation_text = (
        f"✅ Спасибо! Вот ваши данные:\n\n"
        f"🔧 Услуга: {data['service']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📍 Адрес: {data['address']}\n"
        f"⏰ Время: {data['time']}\n\n"
        f"Спасибо за обращение! Мы свяжемся с вами в ближайшее время."
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Подать ещё одну заявку", callback_data="new_request"))
    
    bot.send_message(chat_id, confirmation_text, reply_markup=markup)
    
    # Отправка данных администратору
    admin_text = (
        f"📬 <b>Новая заявка:</b>\n\n"
        f"👤 Клиент: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"🔧 Услуга: {data['service']}\n"
        f"📍 Адрес: {data['address']}\n"
        f"⏰ Время: {data['time']}\n"
        f"📱 User ID: {chat_id}"
    )
    
    bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "new_request")
def new_request(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    send_main_menu(chat_id)

# ======================== ОБРАБОТЧИК ОШИБОК ========================

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Пожалуйста, используйте меню для выбора услуги. Нажмите /start")

# ======================== FLASK МАРШРУТЫ ========================

@app.route('/')
def index():
    return 'Bot is running!'

@app.route('/health')
def health():
    return 'OK', 200

# ======================== ЗАПУСК ========================

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

def run_bot():
    print("🤖 Бот запущен и готов к работе!")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Запуск бота
    run_bot()
