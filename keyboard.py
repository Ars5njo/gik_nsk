from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Канал "ГИК"', url="tg://resolve?domain=www_quizz_mixer"),
         InlineKeyboardButton(text='Беседа "ГИК"', url="https://t.me/+IQpQb8WAoN4wNjQy")
         ],
        [
            InlineKeyboardButton(text='Канал "Ноябрьск Интеллектуальный"', url="tg://resolve?domain=intellektnsk")
        ]
    ]
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='включить таймер'),
            KeyboardButton(text='список команд')
        ],
        [
            KeyboardButton(text='начать игру')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Choose action',
    selective=True,
)
info_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Инструкция для бота и информация о нас')
         ],
        [   
            KeyboardButton(text='Зарегистрировать команду')
         ],
        ],
    resize_keyboard=True,
    one_time_keyboard=False,
    selective=True,
)
