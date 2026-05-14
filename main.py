import telebot
import sqlite3

from config import TOKEN, chanel, numbers, men_arcane, women_arcane, admin_id, directions, women_aromat, man_aromat
from keyboard import start, gender, delete_markup, subscripe, next_step, aromas, finish, end, admin, remind_text

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def bot_start(message):
    conn = sqlite3.connect('astro_users.db')
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE user_id = ?', (message.chat.id,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO users (user_id) VALUES ('%s')" % (message.chat.id,))
        conn.commit()
    cur.close()
    conn.close()
    with open('welcome.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo,
                              caption='Привет ✨\n'
                                      'Я — Парфюмик.\n\n'
                                      'Каждый человек приходит в этот мир со своей энергией.\n'
                                      'Она влияет на характер, выборы, притяжение людей\n'
                                      'и даже на то, какие ароматы раскрывают нас лучше всего.\n\n'
                                      'Я помогу тебе:\n'
                                      '• узнать свою базовую энергию\n'
                                      '• понять сильные стороны\n'
                                      '• подобрать 2–3 аромата, которые усиливают именно тебя\n\n'
                                      'Готов(а) познакомиться со своей энергией?', reply_markup=start)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, 'Панель администратора', reply_markup=admin)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == '👉 Узнать свою энергию':
        msg = bot.send_message(message.chat.id, 'Чтобы описание и рекомендации были максимально точными✨\n'
                                          'подскажи, пожалуйста\n'
                                          'твой пол:', reply_markup=gender)

        bot.register_next_step_handler(msg, take_gender)

def take_gender(message):
    if message.text == '🔹Женский' or message.text == '🔹Мужской':
        select_gender = message.text[1:4]
        msg = bot.send_message(message.chat.id, 'Напиши свою дату рождения\n'
                                          'в формате ДД.ММ.ГГГГ\n\n'
                                          'Например: 07.11.1994\n\n'
                                          '(Я аккуратно проверю формат —\n'
                                          'если что, попрошу ввести ещё раз ✨)', reply_markup=delete_markup)
        bot.register_next_step_handler(msg, take_birthdate, select_gender)

    elif 'зачем' in message.text:
        msg = bot.send_message(message.chat.id, 'Я говорю с тобой языком,\n'
                                          'который будет звучать точнее для тебя ✨\n'
                                          'Суть энергии не меняется —\n'
                                          'меняются нюансы и акценты. ')
        bot.register_next_step_handler(msg, take_gender)

    else:
        msg = bot.send_message(message.chat.id, 'Я пока не смог определить ответ 🙈\n'
                                          'Выбери, пожалуйста, вариант кнопкой: ')
        bot.register_next_step_handler(msg, take_gender)

def take_birthdate(message, select_gender):
    try:
        data = list(map(int, message.text.split('.')))
        if (len(data) == 3) and (data[0] < 32) and (data[0] > 0) and (data[1] < 13) and (data[1] > 0) and (len(str(data[2])) == 4):
            bot.send_message(message.chat.id, 'Считываю твою дату…\n\n'
                                              'В системе 22 архетипа —\n'
                                              'каждый отражает путь, характер и тип энергии.\n\n'
                                              'Сейчас посмотрю,\n'
                                              'какая энергия проявлена именно у тебя ✨')
            if data[0] <= 22:
                number = data[0]
            else:
                number = data[0] - 22

            conn = sqlite3.connect('astro_users.db')
            cur = conn.cursor()
            cur.execute("UPDATE users SET gender = ?, arcane = ? WHERE user_id = ?", (select_gender,number, message.chat.id))
            conn.commit()
            cur.close()
            conn.close()

            if select_gender == 'Муж':
                msg = bot.send_message(message.chat.id, f'🔮Твоя энергия - {number}: Аркан {numbers[number-1]}\n'
                                              f'Коротко о тебе:\n\n'
                                              f'{men_arcane[number-1].split('\n\n')[0]}\n\n'
                                              f'Это та энергия,\n'
                                              f'которую ты транслируешь миру\n'
                                              f'даже тогда, когда молчишь.', reply_markup=next_step)
            else:
                msg = bot.send_message(message.chat.id, f'🔮Твоя энергия - {number}: Аркан {numbers[number - 1]}\n'
                                                  f'Коротко о тебе:\n'
                                                  f'{women_arcane[number-1].split('\n\n')[0]}\n\n'
                                                  f'Это та энергия,\n'
                                                  f'которую ты транслируешь миру\n'
                                                  f'даже тогда, когда молчишь.', reply_markup=next_step)
            bot.register_next_step_handler(msg, step_4_5)

        else:
            msg = bot.send_message(message.chat.id, 'Кажется, формат немного сбился 🙈\n'
                                                    'Попробуй ещё раз: ДД.ММ.ГГГГ ')
            bot.register_next_step_handler(msg, take_birthdate, select_gender)
    except Exception as e:
        print(e)
        msg = bot.send_message(message.chat.id, 'Кажется, формат немного сбился 🙈\n'
                                          'Попробуй ещё раз: ДД.ММ.ГГГГ ')
        bot.register_next_step_handler(msg, take_birthdate, select_gender)

def step_4_5(message):
    if message.text == '➡️Далее':
        msg = bot.send_message(message.chat.id, '.', reply_markup=delete_markup)
        bot.delete_message(msg.chat.id, msg.message_id)
        bot.send_message(message.chat.id, '✨ Я уже вижу твою энергию глубже.\n\n'
                                          'Следующий шаг —\n'
                                          'узнать:\n'
                                          '• твою сильную сторону\n'
                                          '• где важно сохранять баланс\n'
                                          '• какие ароматы усиливают именно тебя\n\n'
                                          'Эта часть доступна только тем,\n'
                                          'кто находится внутри нашего ароматного пространства 🌿',reply_markup=subscripe)

def step_6(message, number, genderr):
    if message.text == '➡️Далее':
        msg = bot.send_message(message.chat.id, 'Ароматы — это не просто запах.\n\n'
                                          'Они усиливают одни состояния\n'
                                          'и мягко выравнивают другие.\n\n'
                                          'Поэтому один и тот же аромат\n'
                                          'на разных людях звучит по-разному.\n\n'
                                          'Для твоей энергии\n'
                                          'есть свои ароматы-ключи 🔑', reply_markup=aromas)
        bot.register_next_step_handler(msg, step_78, number, genderr)

def step_78(message, number, genderr):
    if message.text == '🔑Мои ароматы':
        if genderr == 'Жен':
            bot.send_message(message.chat.id, f'💫 Ароматы, которые работают с твоей энергией ({numbers[number-1]}):\n\n'
                                          f'{directions[number-1]}\n\n'
                                          f'{women_aromat[number-1]}')
        else:
            bot.send_message(message.chat.id,
                             f'💫 Ароматы, которые работают с твоей энергией ({numbers[number - 1]}):\n\n'
                             f'{directions[number - 1]}\n\n'
                             f'{man_aromat[number - 1]}')

        msg = bot.send_message(message.chat.id, 'Когда ты выбираешь аромат\n'
                                          'в своей энергии —\n'
                                          'мир начинает откликаться иначе.\n\n'
                                          'Ты не меняешься.\n'
                                          'Ты просто звучишь собой ✨', reply_markup=finish)
        bot.register_next_step_handler(msg, finish_step)

def finish_step(message):
    if message.text == '🟡Получить ароматы':
        msg = bot.send_message(message.chat.id, '.', reply_markup=delete_markup)
        bot.delete_message(msg.chat.id, msg.message_id)
        bot.send_message(message.chat.id, 'Хочешь попробовать ароматы,\n'
                                          'которые я подобрал для тебя?\n\n'
                                          'Я помогу выбрать формат:\n'
                                          'тестеры, миниатюры или флакон —\n'
                                          'так, чтобы тебе было комфортно ✨', reply_markup=end)

def send_messages(message):
    conn = sqlite3.connect('astro_users.db')
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()

    for i in users:
        try:
            bot.send_message(i[0], message.text)
        except telebot.apihelper.ApiTelegramException:
            bot.send_message(admin_id, f'❌Ошибка отправки\n\n'
                                       f'Пользователь: @{bot.get_chat(i[0]).username}\n'
                                       f'Айди: <code>{i[0]}</code>', parse_mode='HTML')
    bot.send_message(admin_id, '✅Рассылка завершена.')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'check_subscribe':
            chat_member = bot.get_chat_member(chanel, call.message.chat.id)
            if chat_member.status in ['member', 'creator']:
                conn = sqlite3.connect('astro_users.db')
                cur = conn.cursor()
                cur.execute('SELECT arcane, gender FROM users WHERE user_id = ?', (call.message.chat.id,))
                f = cur.fetchone()
                number, genderr = int(f[0]), f[1]
                cur.close()
                conn.close()
                if genderr == 'Жен':
                    points = women_arcane[number-1].split('\n\n')[1].split('\n')
                else:
                    points = men_arcane[number - 1].split('\n\n')[1].split('\n')
                for i in range(len(points)):
                    points[i] = points[i].split(':')[1][1:]
                bot.delete_message(call.message.chat.id, call.message.message_id)
                msg = bot.send_message(call.message.chat.id,'✨Твоя сильная сторона:\n'
                                           f'{points[0]}\n\n'
                                           f'⚖️Зона баланса:\n'
                                           f'{points[1]}\n\n'
                                           f'💡Как энергия проявляется в жизни:\n'
                                           f'{points[2]}', reply_markup=next_step)
                bot.register_next_step_handler(msg, step_6, number, genderr)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text='Я пока не вижу подписку 🙈\n'
                                           'Подпишись на канал, пожалуйста,\n'
                                           'и я сразу продолжу ✨', reply_markup=subscripe)

        elif call.data == 'again':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id, 'Чтобы описание и рекомендации были максимально точными✨\n'
                                                    'подскажи, пожалуйста\n'
                                                    'твой пол:', reply_markup=gender)
            bot.register_next_step_handler(msg, take_gender)

        elif call.data == 'messages':
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Введите сообщение:')
            bot.register_next_step_handler(msg, send_messages)

        elif call.data == 'remind':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Выберите текст', reply_markup=remind_text)

        elif call.data == 'download':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='⬇️База данных')
            with open("astro_users.db", "rb") as f:
                bot.send_document(call.message.chat.id, f)

        elif call.data == 'text1':
            conn = sqlite3.connect('astro_users.db')
            cur = conn.cursor()
            cur.execute('SELECT user_id, arcane FROM users')
            users = cur.fetchall()
            cur.close()
            conn.close()
            for i in users:
                if i[1] == None:
                    try:
                        bot.send_message(i[0], 'Привет! Чтобы я смог подобрать твой идеальный аромат, мне нужна твоя дата рождения. Давай начнём? 😏')
                    except telebot.apihelper.ApiTelegramException:
                        bot.send_message(admin_id, f'❌Ошибка отправки\n\n'
                                                   f'Пользователь: @{bot.get_chat(i[0]).username}\n'
                                                   f'Айди: <code>{i[0]}</code>', parse_mode='HTML')
            bot.send_message(admin_id, '✅Рассылка завершена.')

        elif call.data == 'text2':
            conn = sqlite3.connect('astro_users.db')
            cur = conn.cursor()
            cur.execute('SELECT user_id, arcane FROM users')
            users = cur.fetchall()
            cur.close()
            conn.close()
            for i in users:
                if i[1] == None:
                    try:
                        bot.send_message(i[0], '🎁 У тебя уникальный аромат, и я готов его найти! Просто введи дату рождения.')
                    except telebot.apihelper.ApiTelegramException:
                        bot.send_message(admin_id, f'❌Ошибка отправки\n\n'
                                                   f'Пользователь: @{bot.get_chat(i[0]).username}\n'
                                                   f'Айди: <code>{i[0]}</code>', parse_mode='HTML')
            bot.send_message(admin_id, '✅Рассылка завершена.')

bot.infinity_polling(timeout=10, long_polling_timeout=5)