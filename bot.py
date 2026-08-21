import telebot
from telebot import types
import os
from flask import Flask

bot = telebot.TeleBot('8745020834:AAHlDdroqkuhDJkbG4Qqtu72pnGmgVHWcvg')
ADMIN_ID = '8549327132'
CHANNEL_USERNAME = "@tehnoprofiLipetsk"

user_data = {}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status != 'left' and member.status != 'kicked'
    except:
        return False

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📝 Оставить заявку", callback_data="zayavka")
    btn2 = types.InlineKeyboardButton("💰 Прайс", callback_data="price")
    btn3 = types.InlineKeyboardButton("💬 Отзывы", callback_data="reviews")
    btn4 = types.InlineKeyboardButton("📋 Как мы работаем", callback_data="how_it_works")
    btn5 = types.InlineKeyboardButton("☎️ Контакты", callback_data="kontakty")
    markup.add(btn1, btn2, btn3, btn4, btn5)
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
        "🔨 Мы подбираем лучших строителей и мастеров по ремонту.\n"
        "💯 Работаем быстро, качественно и с гарантией.\n\n"
        "👇 <b>Выберите действие:</b>"
    )
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu(), parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "Спасибо за подписку! ✅")
        bot.edit_message_text("👋 <b>Добро пожаловать в «ТехноПрофи»!</b>\n\n🔨 Мы подбираем лучших строителей и мастеров по ремонту.\n💯 Работаем быстро, качественно и с гарантией.\n\n👇 <b>Выберите действие:</b>", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_main_menu(), parse_mode='HTML')
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
        btn6 = types.InlineKeyboardButton("⬅️ В меню", callback_data="menu")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "price":
        text = "💰 <b>Наши цены:</b>\n\n🛠 Разнорабочие — от 500 ₽/час\n🔨 Демонтаж — от 800 ₽/м²\n🚛 Вывоз мусора — от 3000 ₽/рейс\n🌿 Покос травы — от 1000 ₽/сотка\n\n📞 Точная стоимость зависит от объема работ. Свяжитесь с нами!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ В меню", callback_data="menu"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "reviews":
        text = "💬 <b>Отзывы наших клиентов:</b>\n\n⭐️⭐️⭐️⭐️⭐️ «Сделали ремонт за 2 дня, всё супер!» — Анна\n⭐️⭐️⭐️⭐️⭐️ «Быстро вывезли мусор, цена честная» — Дмитрий\n⭐️⭐️⭐️⭐️⭐️ «Рабочие приехали вовремя, работают качественно» — Ольга\n\n📝 Хотите так же? Оставьте заявку!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ В меню", callback_data="menu"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "how_it_works":
        text = "📋 <b>Как мы работаем:</b>\n\n1️⃣ Вы оставляете заявку\n2️⃣ Мы звоним и уточняем детали\n3️⃣ Мастер приезжает и рассчитывает точную ��тоимость\n4️⃣ Выполняем работу\n5️⃣ Вы оплачиваете результат\n\n💯 Всё просто и с гарантией!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ В меню", callback_data="menu"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "kontakty":
        text = "☎️ <b>Наши контакты:</b>\n\n📞 +7 (950) 807-57-88\n🕘 Мы на связи с 9:00 до 21:00!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ В меню", callback_data="menu"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode='HTML')

    elif call.data == "menu":
        bot.edit_message_text("👋 <b>Главное меню</b>\n\n👇 Выберите действие:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_main_menu(), parse_mode='HTML')

    elif call.data.startswith("usluga_"):
        service_map = {
            "usluga_raznorab": "🛠 Разнорабочие",
            "usluga_demontazh": "🔨 Демонтаж",
            "usluga_musor": "🚛 Вывоз мусора",
            "usluga_pokos": "🌿 Покос травы",
            "usluga_svoy": "📝 Свой вариант"
        }
        service = service_map.get(call.data, "Выбранная услуга")
        user_data[call.from_user.id] = service
        bot.edit_message_text(f"✅ Отлично! Вы выбрали: <b>{service}</b>\n\n✍️ Теперь напишите ваше <b>Имя</b>:", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML')
        bot.register_next_step_handler(call.message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_data[f'{user_id}_name'] = message.text
    bot.send_message(message.chat.id, "📱 Отлично! Теперь напишите ваш <b>Номер телефона</b>:", parse_mode='HTML')
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_id = message.from_user.id
    phone = message.text
    user_data[f'{user_id}_phone'] = phone
    bot.send_message(message.chat.id, "📍 <b>Отлично! Теперь напишите ваш Адрес</b> (или населенный пункт, где нужна работа):", parse_mode='HTML')
    bot.register_next_step_handler(message, get_address)

def get_address(message):
    user_id = message.from_user.id
    address = message.text
    user_data[f'{user_id}_address'] = address
    bot.send_message(message.chat.id, "⏰ <b>Когда вам удобно?</b> (Напишите дату и время, например: завтра с 10:00):", parse_mode='HTML')
    bot.register_next_step_handler(message, get_time)

def get_time(message):
    user_id = message.from_user.id
    time = message.text
    user_data[f'{user_id}_time'] = time

    name = user_data.get(f'{user_id}_name', "Не указано")
    phone = user_data.get(f'{user_id}_phone', "Не указано")
    service = user_data.get(user_id, "Не указано")
    address = user_data.get(f'{user_id}_address', "Не указано")

    admin_text = (
        f"🔥 <b>НОВАЯ ЗАЯВКА!</b>\n\n"
        f"🛠 <b>Услуга:</b> {service}\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📱 <b>Телефон:</b> {phone}\n"
        f"📍 <b>Адрес:</b> {address}\n"
        f"⏰ <b>Время:</b> {time}"
    )

    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка при отправке админу: {e}")

    try:
        markup = types.InlineKeyboardMarkup()
        try:
            markup.add(types.InlineKeyboardButton("📞 Позвонить", url=f"tel:{phone}"))
        except:
            pass
        try:
            markup.add(types.InlineKeyboardButton("💬 Написать в WhatsApp", url="https://wa.me/79508075788"))
        except:
            pass
        markup.add(types.InlineKeyboardButton("🏠 В меню", callback_data="menu"))

        bot.send_message(
            message.chat.id,
            f"🎉 Спасибо, {name}!\n\n"
            f"✅ Ваша заявка по услуге «{service}» принята!\n"
            f"📞 Мы свяжемся с вами в ближайшее время.\n\n"
            f"Хорошего дня! 😊",
            reply_markup=markup
        )
    except Exception as e:
        print(f"Ошибка при отправке клиенту: {e}")
        try:
            bot.send_message(message.chat.id, f"🎉 Спасибо, {name}!\n\n✅ Ваша заявка по услуге «{service}» принята!\n📞 Мы свяжемся с вами в ближайшее время.")
        except:
            pass

bot.polling(none_stop=True)

import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
