from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

menu = [
    [
        InlineKeyboardButton(
            text="📝 Генерировать текст", callback_data="generate_text"
        ),
        InlineKeyboardButton(
            text="🖼 Генерировать изображение", callback_data="generate_image"
        ),
<<<<<<< HEAD
        InlineKeyboardButton(
            text="Edit image", callback_data="edit_image"
        )
    ],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")],
=======
    ]
>>>>>>> 9ab576072f2fcf8e754521476b2e041d74817d0d
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
    ]
)
