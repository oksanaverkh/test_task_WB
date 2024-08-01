import telebot

# Инициализируем константу-словарь для периодов напоминаний
PERIODS = {'h': 'часов', 'd': 'дней', 'w': 'недель', 'm': 'месяцев'}

# имя бота: reminder_WB_bot
bot = telebot.TeleBot('7309683171:AAFKM-t0zbEmiRPYP8HnNP4Q-3Z-mHoWxtQ')

# Инициализируем переменные для срока напоминания и задачи
time = 0
period = ''
task = ''


@bot.message_handler(content_types=['text'])
def get_deadline(message):
    '''
    Определяем функцию, принимающую сообщение с информацией о сроке напоминания.
    Вводим опцию /help для разъяснения пользователю формата написания сообщения.
    Gthy
    '''
    deadline = message.text.split()[-1]
    if message.text.startswith('@reminder_WB_bot ctrl') and deadline[-1] in PERIODS.keys() and deadline[:-1].isdigit():
        global time
        global period
        time = int(deadline[:-1])
        period = deadline[-1]
        bot.send_message(message.from_user.id,
                         "Принято. Напиши задание, о котором нужно напомнить")
        bot.register_next_step_handler(message, get_task)

    elif message.text == "/help":
        bot.send_message(
            message.from_user.id, "Напиши в формате @reminder_WB_bot ctrl 5d, где 5d срок напоминания, 5 - интервал, d - продолжительность в часах, днях, неделях, месяцах (h, d, w, m)")
    else:
        bot.send_message(message.from_user.id,
                         "Я тебя не понимаю. Напиши /help.")


def get_task(message):
    '''
    Определяем функцию, принимающую сообщение с задачей, о которой нужно напомнить.
    Запрашиваем у пользователей подтверждение того, что все введено верно, с использованием клавиатуры.
    '''

    if not message.text:
        bot.send_message(message.from_user.id,
                         "Я тебя не понимаю. Напиши задание.")

    else:
        global task
        task = message.text
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(
            text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = telebot.types.InlineKeyboardButton(
            text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = f'Напомнить тебе о задаче {task} через {time} {PERIODS[period]}?'
        bot.send_message(message.from_user.id, text=question,
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    '''
    Определяем метод-обработчик значений на клавиатуре.
    Отправляем финальное сообщение с подтверждением.
    '''
    if call.data == "yes":
        bot.send_message(
            call.message.chat.id, f'Задача: "{task}" принята. Напомню о ней через {time} {PERIODS[period]}')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Начнем сначала. Напиши /help')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
