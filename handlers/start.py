from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton
import re
import main
from typing import List

start_router = Router()


async def get_week_data() -> List:
    data = await main.filter_data(6, 2, 1)
    return data


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')


@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()')


@start_router.message(F.text == '/call_buttons')
async def cmd_call_buttons(message: Message):
    kb = [
            [
                KeyboardButton(text="Print the schedule"),
                KeyboardButton(text='Print your homework')
            ]
          ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("What can i do for you?", reply_markup=keyboard)


@start_router.message(F.text.lower() == "print the schedule")
async def show_schedule(message: Message):
    filtered_data = await get_week_data()

    buttons_list = []

    for subject in filtered_data:
        type_ = subject.get("type")
        name = subject.get("content").get("lesson_from_reference")
        lesson_id = subject.get("_id")

        buttons_list.append([InlineKeyboardButton(text=f"{type_}:{name}", callback_data=f"id#{lesson_id}")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    await message.answer(text=f"The schedule for today", reply_markup=kb)
    await message.answer(text="Here you are )", reply_markup=ReplyKeyboardRemove())


@start_router.message(F.text.lower() == "print your homework")
async def show_homework(message: Message):
    builder = ReplyKeyboardBuilder()
    for obj in range(1, 13):
        builder.add(KeyboardButton(text=f"R1:{obj}"))
    builder.adjust(3)
    await message.answer(text="Chose the object", reply_markup=builder.as_markup(resize_keyboard=True))


@start_router.callback_query(F.data.startswith("id#"))
async def show_button_data(callback: CallbackQuery) -> None:
    filtered_data = await get_week_data()
    id_ = callback.data.split('#')[1]

    corresponding_lesson = list(filter(lambda subject: subject.get("_id") == id_, filtered_data))

    await callback.answer(text=f"""prof: {corresponding_lesson[0].get('content').get('teacher')}\n\ntype: {corresponding_lesson[0].get('content').get('type')}\n\nroom: {corresponding_lesson[0].get('content').get('room')}\n\nstart: {corresponding_lesson[0].get("start_date")}\n\nend: {corresponding_lesson[0].get("end_date")}""", show_alert=True)
