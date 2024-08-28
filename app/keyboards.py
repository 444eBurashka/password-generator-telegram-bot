from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сгенерировать пароль')],
    [KeyboardButton(text='Настройки')]
],
                           resize_keyboard=True)

async def getInlineSettings(data: dict):
    keyboard = InlineKeyboardBuilder()
    buttons = {'Прописные буквы': 'uppercase',
               'Строчные буквы': 'lowercase',
               'Цифры': 'number',
               'Спец. символы': 'specialchar',
               'Пробел': 'whitespace',
               'Кол-во символов': 'numamount'}
    for button in buttons:
        if button != 'Кол-во символов':
            __btn = button + ' ✅' if data[buttons[button]] else button + ' ❌'
        else:
            __btn = button + ' ' + str(data[buttons[button]])
        keyboard.add(InlineKeyboardButton(text=__btn, callback_data=buttons[button]))
    return keyboard.adjust(2).as_markup()
