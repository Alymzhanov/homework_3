from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
os.environ.get("token")

bot = Bot(token = '7619899113:AAGlZM3r-XI58HJkZwR6iKcChyVkLFB9knc')
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        username TEXT,
                        address TEXT,
                        description TEXT,
                        status TEXT DEFAULT 'Заказ принят.'
                    )''')
    conn.commit()
    conn.close()

init_db()

# Inline keyboards
def get_category_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Еда", callback_data="category:Еда")],
        [InlineKeyboardButton(text="Запчасти", callback_data="category:Запчасти")],
        [InlineKeyboardButton(text="Мебель", callback_data="category:Мебель")],
    ])
    return keyboard

# State storage
temp_data = {}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите категорию заказа:",
        reply_markup=get_category_keyboard()
    )

@dp.callback_query(lambda c: c.data.startswith("category:"))
async def select_category(callback_query: types.CallbackQuery):
    category = callback_query.data.split(":")[1]
    temp_data[callback_query.from_user.id] = {"category": category}
    await bot.send_message(callback_query.from_user.id, "Введите ваше имя:")

@dp.message(lambda message: message.from_user.id in temp_data and "username" not in temp_data[message.from_user.id])
async def get_username(message: types.Message):
    temp_data[message.from_user.id]["username"] = message.text
    await message.answer("Введите адрес доставки:")

@dp.message(lambda message: message.from_user.id in temp_data and "address" not in temp_data[message.from_user.id])
async def get_address(message: types.Message):
    temp_data[message.from_user.id]["address"] = message.text
    await message.answer("Введите описание заказа:")

@dp.message(lambda message: message.from_user.id in temp_data and "description" not in temp_data[message.from_user.id])
async def get_description(message: types.Message):
    user_data = temp_data[message.from_user.id]
    user_data["description"] = message.text

    # Save order to the database
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO orders (category, username, address, description) 
                      VALUES (?, ?, ?, ?)''',
                   (user_data["category"], user_data["username"], user_data["address"], user_data["description"]))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    del temp_data[message.from_user.id]
    await message.answer(f"Ваш заказ оформлен! Номер заказа: {order_id}")

@dp.message(Command("status"))
async def check_status_command(message: types.Message):
    await message.answer("Введите номер заказа для проверки статуса:")

@dp.message(lambda message: message.text.isdigit())
async def check_status(message: types.Message):
    order_id = int(message.text)
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        await message.answer(f"Статус вашего заказа: {result[0]}")
    else:
        await message.answer("Заказ с таким номером не найден.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
