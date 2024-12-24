from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import token

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher()

MENU = {
    'эспрессо' : 150,
    "капучино" : 150,
    "Американо" : 150,
    "Латте" : 150 ,
    "3 в 1": 50
}

INFO = [
    "Контакты",
    "О нас"
]

orders = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()

    for info in INFO:
        builder.button(
            text=info,
            callback_data=f"info_{info.lower()}"
        )
    builder.adjust(1)

    await message.answer("Добро пожаловать.\nВыберите из меню: /menu", reply_markup=builder.as_markup())

@dp.message(F.text == "О нас")
async def about(message:types.Message):
    await message.answer("Инфо о нас")

@dp.message(Command("menu"))
async def menu(message:types.Message):
    builder = InlineKeyboardBuilder()

    for coffee, price in MENU.items():
        builder.button(
            text=f"{coffee} - {price}",
            callback_data=f"menu_{coffee}"
        )
    builder.adjust(2)
    await message.answer("Меню напитков: ", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("menu_"))
async def choose_coffee(callback: types.CallbackQuery):
    coffee = callback.data.split("_")[1]
    orders[callback.from_user.id] = {"coffee" : coffee, "quantity": 1}

    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.button(
            text=str(i),
            callback_data=f"quantity_{i}"
        )
    builder.adjust(3)
    await callback.message.answer(
        f"Вы выбрали {coffee}.Укажите ков-ло: ",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("quantity_"))
async def choose_quantity(callback:types.CallbackQuery):
    quantity = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if user_id in orders:
        orders[user_id]["quantity"] = quantity
        coffee = orders[user_id]["coffee"]
        price = MENU[coffee] * quantity

        builder = InlineKeyboardBuilder()
        builder.button(
            text="Подтвердить заказ",
            callback_data='comfirm_orders'
        )

        await callback.message.answer(
            f"Ваш заказ: {coffee} x {quantity} = {price} сомов.\nПодтвердить заказ",
            reply_markup=builder.as_markup()
        )

@dp.callback_query(F.data == 'comfirm_orders')
async def comfirm_orders(callback:types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in orders:
        coffee = orders[user_id]['coffee']
        quantity = orders[user_id]['quantity']
        total_price = MENU[coffee] * quantity

        del orders[user_id]

        await callback.message.answer(
            f"Спасибо за заказ!\nВы заказали: {coffee} x {quantity}.\nИтог к оплате: {total_price} сомов"
        )

async def main():
    await dp.start_polling(bot)

asyncio.run(main())