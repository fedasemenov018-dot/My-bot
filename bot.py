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
        bot.edit_message_text("🏗 <b>СтройБаза!</b>\n\nВыберите, что вас интересует:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_stroybaza_menu(), parse_mode='HTML')

    elif call.data == "stroy_poddony":
        text = "🪵 <b>Поддоны:</b>\n\nМы продаем деревянные поддоны по выгодным ценам!\n\n<b>Цена: от 380 ₽ за поддон</b>\n\n📞 Точная цена зависит от количества. Если есть вопросы, напишите нам!"
        markup = types.InlineKeyboardMarkup()
        btn_request = types.InlineKeyboardButton("📝 Оставить заявку", callback_data="stroy_request")
        btn_back = types.InlineKeyboardButton("⬅️ В СтройБазу", callback_data="stroybaza")
        markup.add(btn_request, btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "stroy_kirpich":
        text = "🧱 <b>Кирпич:</b>\n\nМы продаем кирпич по выгодным ценам!\n\n<b>Кирпич лицевой красный одинарный (Воротынский К.З.):</b> 15 руб/шт\n<b>Кирпич керамический одинарный лицевой красный (Керма):</b> 20 руб/шт\n<b>Кирпич лицевой пустотелый одинарный красный:</b> 23 руб/шт\n\n📞 Точная цена зависит от количества. Если есть вопросы, напишите нам!"
        markup = types.InlineKeyboardMarkup()
        btn_request = types.InlineKeyboardButton("📝 Оставить заявку", callback_data="stroy_request")
        btn_back = types.InlineKeyboardButton("⬅️ В СтройБазу", callback_data="stroybaza")
        markup.add(btn_request, btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "stroy_smesi":
        text = "💊 <b>Смеси:</b>\n\nМы продаем строительные смеси по выгодным ценам!\n\n<b>Шпаклевка гипсовая для заделки швов и стыков Волма Шов 20 кг:</b> 690 ₽\n\n📞 Точная цена зависит от количества. Если есть вопросы, напишите нам!"
        markup = types.InlineKeyboardMarkup()
        btn_request = types.InlineKeyboardButton("📝 Оставить заявку", callback_data="stroy_request")
        btn_back = types.InlineKeyboardButton("⬅️ В СтройБазу", callback_data="stroybaza")
        markup.add(btn_request, btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "stroy_request":
        bot.send_message(call.message.chat.id, "📦 <b>Оставить заявку на стройматериалы!</b>\n\n1️⃣ <b>Первый вопрос:</b> Какой товар и сколько штук вам нужен? (например, 5 поддонов или 100 кирпичей)")
        user_data[call.from_user.id] = "stroy"
        bot.register_next_step_handler(call.message, ask_stroy_quantity)

    elif call.data == "price":
        text = "💰 <b>Наши цены:</b>\n\n🛠 Разнорабочие — от 500 ₽/час\n🔨 Демонтаж — от 300 ₽/м²\n🚛 Вывоз мусора — от 3000 ₽/рейс\n🌿 Покос травы — от 500 ₽/сотка\n📦 Уборка территории от листвы — от 200 ₽/м²\n\n📞 Точная стоимость зависит от объема работ. Свяжитесь с нами!"
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
        markup.add(btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "how_it_works":
        text = "📋 <b>Как мы работаем:</b>\n\n1️⃣ Вы оставляете заявку\n2️⃣ Мы звоним и уточняем детали\n3️⃣ Мастер приезжает и рассчитывает точную стоимость\n4️⃣ Выполняем работу\n5️⃣ Вы оплачиваете результат\n\n💯 Всё просто и с гарантией!"
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
        markup.add(btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "kontakty":
        text = "☎️ <b>Наши контакты:</b>\n\n📞 +7 (950) 807-57-88\n🕘 Мы на связи с 9:00 до 21:00!\n\n💬 Наш Telegram: @Pankovvff"
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
        markup.add(btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "reviews":
        text = "💬 <b>Отзывы наших клиентов:</b>\n\n⭐️⭐️⭐️⭐️⭐️ «Сделали ремонт за 2 дня, всё супер!» — Анна\n⭐️⭐️⭐️⭐️⭐️ «Быстро вывезли мусор, цена честная» — Дмитрий\n⭐️⭐️⭐️⭐️⭐️ «Рабочие приехали вовремя, работают качественно» — Ольга\n\n📝 Хотите так же? Оставьте заявку!"
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
        markup.add(btn_back)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "menu":
        text = "👋 <b>Главное меню</b>\n\n👇 Выберите действие:"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_main_menu(), parse_mode='HTML')

    elif call.data.startswith("usluga_"):
        service_map = {
            "usluga_raznorab": "🛠 Разнорабочие",
            "usluga_demontazh": "🔨 Демонтаж",
            "usluga_musor": "🚛 Вывоз мусора",
            "usluga_pokos": "🌿 Покос травы",
            "usluga_svoy": "📝 Свой вариант",
            "usluga_uborka": "📦 Уборка территории"
        }
        service = service_map.get(call.data, "Выбранная услуга")
        user_data[call.from_user.id] = service
        bot.edit_message_text(f"✅ Отлично! Вы выбрали: <b>{service}</b>\n\n✍️ Теперь напишите ваше <b>Имя</b>:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler(call.message, get_name)

def ask_stroy_quantity(message):
    user_id = message.from_user.id
    user_data[f'{user_id}_stroy_quantity'] = message.text
    bot.send_message(message.chat.id, "2️⃣ <b>Нужна доставка или самовывоз?</b> (Напишите: Доставка или Самовывоз)")
    bot.register_next_step_handler(message, ask_stroy_delivery)

def ask_stroy_delivery(message):
    user_id = message.from_user.id
    user_data[f'{user_id}_stroy_delivery'] = message.text
    bot.send_message(message.chat.id, "3️⃣ <b>Когда нужен товар?</b> (Напишите дату и время, например: Завтра с 10:00)")
    bot.register_next_step_handler(message, ask_stroy_time)

def ask_stroy_time(message):
    user_id = message.from_user.id
    user_data[f'{user_id}_stroy_time'] = message.text
    bot.send_message(message.chat.id, "4️⃣ <b>Имя