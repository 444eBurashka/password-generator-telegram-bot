from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from random import choice

import app.keyboards as kb


router = Router()


class Sts(StatesGroup):
    default = default_state
    getNumAmonut = State()


async def generatePassword(data: dict):
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    number = '0123456789'
    specialchar = "-_!#$%&()*+./:;<=>?@[]^`{|}~'\\"
    whitespace = ' '

    chars = (
        list(uppercase) * int(data['uppercase']) +
        list(lowercase) * int(data['lowercase']) +
        list(number) * int(data['number']) +
        list(specialchar) * int(data['specialchar']) +
        list(whitespace) * int(data['whitespace'])
        )
    
    password = ''
    for i in range(data['numamount']):
        password += choice(chars)
    
    return password


@router.message(default_state, CommandStart())
async def cmdStart(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data:
        startDict = {
            'uppercase': True,
            'lowercase': True,
            'number': True,
            'specialchar': False,
            'whitespace': False,
            'numamount': 8
        }
        await state.update_data(startDict)

    await message.answer('Привет!\nДля генерации пароля нажми на кнопку "Сгенерировать пароль" или /generate\n\nДля настройки - на кнопку "Настройки" или /settings', reply_markup=kb.main)


@router.message(default_state, Command('settings'))
async def settingsFromCommand(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.message(default_state, F.text == 'Настройки')
async def settingsFromText(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.message(default_state, F.text == 'Сгенерировать пароль')
async def generatePasswordFromText(message: Message, state: FSMContext):
    data = await state.get_data()
    if any([data[i] for i in data if i != 'numamount']):
        password = await generatePassword(data)
    else:
        password = 'Настройки не позволяют сгенерировать пароль'
    await message.answer(password)


@router.message(default_state, Command('generate'))
async def generatePasswordFromText(message: Message, state: FSMContext):
    data = await state.get_data()
    if any([data[i] for i in data if i != 'numamount']):
        password = await generatePassword(data)
    else:
        password = 'Настройки не позволяют сгенерировать пароль'
    await message.answer(password)


@router.callback_query(F.data == 'uppercase')
async def setUppercase(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Настройка изменена')
    data = await state.get_data()
    await state.update_data(uppercase=bool(int(data['uppercase'] + 1) % 2))
    data['uppercase'] = bool(int(data['uppercase'] + 1) % 2)
    await callback.message.edit_text('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.callback_query(F.data == 'lowercase')
async def setLowercase(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Настройка изменена')
    data = await state.get_data()
    await state.update_data(lowercase=bool(int(data['lowercase'] + 1) % 2))
    data['lowercase'] = bool(int(data['lowercase'] + 1) % 2)
    await callback.message.edit_text('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.callback_query(F.data == 'number')
async def setNumber(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Настройка изменена')
    data = await state.get_data()
    await state.update_data(number=bool(int(data['number'] + 1) % 2))
    data['number'] = bool(int(data['number'] + 1) % 2)
    await callback.message.edit_text('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.callback_query(F.data == 'specialchar')
async def setSpecialchar(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Настройка изменена')
    data = await state.get_data()
    await state.update_data(specialchar=bool(int(data['specialchar'] + 1) % 2))
    data['specialchar'] = bool(int(data['specialchar'] + 1) % 2)
    await callback.message.edit_text('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.callback_query(F.data == 'whitespace')
async def setWhitespace(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Настройка изменена')
    data = await state.get_data()
    await state.update_data(whitespace=bool(int(data['whitespace'] + 1) % 2))
    data['whitespace'] = bool(int(data['whitespace'] + 1) % 2)
    await callback.message.edit_text('Настройки', reply_markup=await kb.getInlineSettings(data))


@router.callback_query(F.data == 'numamount')
async def setNumamount(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите количество символов в пароле')
    await state.set_state(Sts.getNumAmonut)
    await callback.answer()

@router.message(Sts.getNumAmonut)
async def getNumamount(message: Message, state: FSMContext):
    num = message.text
    if num.isdigit():
        if int(num) > 0:
            await state.set_state(Sts.default)
            await state.update_data(numamount=int(num))
            data = await state.get_data()
            await message.answer('Настройка применена')
            await message.answer('HEEEELP', reply_markup=await kb.getInlineSettings(data))
        else:
            await message.answer('Количество символов не может быть меньше или равно нулю')
    else:
        await message.answer('Введите корректные данные (число)')