from telebot import types

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
start.add(types.KeyboardButton('👉 Узнать свою энергию'))

gender = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
gender.add(types.KeyboardButton('🔹Женский'), types.KeyboardButton('🔹Мужской'))

delete_markup = types.ReplyKeyboardRemove()

subscripe = types.InlineKeyboardMarkup(row_width=1)
subscripe.add(types.InlineKeyboardButton('🔔Подписаться на канал', url='https://t.me/aroma_muse'),
              types.InlineKeyboardButton('✨Продолжить', callback_data='check_subscribe'))

next_step = types.ReplyKeyboardMarkup(resize_keyboard=True)
next_step.add(types.KeyboardButton('➡️Далее'))

aromas = types.ReplyKeyboardMarkup(resize_keyboard=True)
aromas.add(types.KeyboardButton('🔑Мои ароматы'))

finish = types.ReplyKeyboardMarkup(resize_keyboard=True)
finish.add(types.KeyboardButton('🟡Получить ароматы'))

end = types.InlineKeyboardMarkup(row_width=1)
end.add(types.InlineKeyboardButton('🔸Приобрести аромат под меня', url='https://t.me/aroma_muse?direct'),
        types.InlineKeyboardButton(text='🔸Посмотреть каталог',url='https://t.me/katalog_aromamuse'),
        types.InlineKeyboardButton(text='🔸Пройти ещё раз', callback_data='again'))

admin = types.InlineKeyboardMarkup(row_width=1)
admin.add(types.InlineKeyboardButton('💬Рассылка', callback_data='messages'),
            types.InlineKeyboardButton('📢Напомнить о боте', callback_data='remind'),
            types.InlineKeyboardButton('📲Скачать базу данных', callback_data='download'),
            types.InlineKeyboardButton('❎Закрыть меню', callback_data='close'))

remind_text = types.InlineKeyboardMarkup(row_width=1)
remind_text.add(types.InlineKeyboardButton('Текст №1', callback_data='text1'),
                types.InlineKeyboardButton('Текст №2', callback_data='text2'))