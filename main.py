from aiogram import types, Dispatcher, F, filters, Bot
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


bot = Bot(token="6459329359:AAHoJ2ZO8E4-oRXP47zwGHDGLtXJKHI_85c")
dp = Dispatcher(bot=bot)


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    number = State()


contact_button = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Kontakt jo'natish", request_contact=True)]
])


@dp.message(filters.Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Registration.first_name)
    await message.answer("Xush kelibsiz\nIsmingizni kiriting: ")


@dp.message(Registration.first_name)
async def first_name_function(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(Registration.last_name)
    await message.answer("Yaxshi endi familya kiriting: ")


@dp.message(Registration.last_name)
async def last_name_function(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Registration.number)
    await message.answer("Yaxshi endi number kiriting: ", reply_markup=contact_button)


@dp.message(Registration.number)
async def phone_function(message: types.Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"Gap yo'q!\nSizning ismingiz: {data['first_name']}\nSizning familyangiz: {data['last_name']}\nSizning nomeringiz: +{data['number']}", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
