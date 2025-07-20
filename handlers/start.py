from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton
import utils
from typing import List

start_router = Router()


async def get_week_data(day) -> List:
    try:
        data = await utils.filter_data(week=22, day=day, group=2, sub=1)
        return data
    except ConnectionError as e:
        return []



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
    dates_list = utils.get_days_of_this_week()
    kb = list()

    for date in dates_list:
        button = InlineKeyboardButton(text=date[1], callback_data=f"date#{date[0]}")
        kb.append([button])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text="For which day of week?", reply_markup=reply_markup)


@start_router.callback_query(F.data.startswith("date#"))
async def show_schedule(callback: CallbackQuery):
    global filtered_data
    filtered_data = await get_week_data(callback.data.split('#')[1])
    buttons_list = []

    if len(filtered_data) == 0:
        await callback.message.answer(text=f"I am sorry, the server is currently unavailable, please, try later")

    else:
        for subject in filtered_data:
            type_ = subject.get("type")
            name = subject.get("content").get("lesson_from_reference")
            lesson_id = subject.get("_id")

            buttons_list.append([InlineKeyboardButton(text=f"{type_}:{name}", callback_data=f"id#{lesson_id}")])

        kb = InlineKeyboardMarkup(inline_keyboard=buttons_list)
        await callback.message.answer(text=f"The schedule for today", reply_markup=kb)
        await callback.answer(text="Click on a lesson to show the details")
        await callback.answer(reply_markup=ReplyKeyboardRemove())


@start_router.message(F.text.lower() == "print your homework")
async def show_homework(message: Message):
    builder = ReplyKeyboardBuilder()
    for obj in range(1, 13):
        builder.add(KeyboardButton(text=f"R1:{obj}"))
    builder.adjust(3)
    await message.answer(text="Chose the object", reply_markup=builder.as_markup(resize_keyboard=True))


@start_router.callback_query(F.data.startswith("id#"))
async def show_button_data(callback: CallbackQuery) -> None:
    id_ = callback.data.split('#')[1]

    corresponding_lesson = list(filter(lambda subject: subject.get("_id") == id_, filtered_data))

    await callback.answer(text=f"""prof: {corresponding_lesson[0].get('content').get('teacher')}\n\ntype: {corresponding_lesson[0].get('content').get('type')}\n\nroom: {corresponding_lesson[0].get('content').get('room')}\n\nstart: {corresponding_lesson[0].get("start_date")}\n\nend: {corresponding_lesson[0].get("end_date")}""", show_alert=True)
