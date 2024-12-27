# from aiogram import Bot, Dispatcher, types, F
# from aiogram.filters import Command
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from config import token
# import asyncio

# bot = Bot(token=token)
# dp = Dispatcher()

# AVTO = {
#     "Зимний шины": 1500,
#     "Летние шины": 1000,
#     "Все сезоный шины": 860,
#     "Шипованный шины": 1550
# }

# MOB = {
#     "Зарядник тайпси": 350,
#     "IPhone зарядник": 400,
#     "Защитное стекло": 250
# }

# orders = {}

# @dp.message(Command("start"))
# async def start(message: types.Message):
#     await message.answer("Добро пожаловать в онлайн магазин.\nДля выбора авто запчастей переходите-> /avto\nДля выбора мобильных запчастей переходите-> /mob")

# @dp.message(Command("avto"))
# async def avto(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     for spares, price in AVTO.items():
#         builder.button(
#             text=f"{spares} - {price}",
#             callback_data=f"avto_{spares}"
#         )
#     builder.adjust(2)
#     await message.answer("Каталог авто запчастей:", reply_markup=builder.as_markup())

# @dp.callback_query(F.data.startswith("avto_"))
# async def choose_spares(callback: types.CallbackQuery):
#     spares = callback.data.split("_")[1]
#     orders[callback.from_user.id] = {"spares": spares, "category": "avto", "quantity": 1}

#     builder = InlineKeyboardBuilder()
#     for i in range(1, 6):
#         builder.button(
#             text=str(i),
#             callback_data=f"quantity_{i}"
#         )
#     builder.adjust(2)
#     await callback.message.answer(f"Вы выбрали {spares}. Укажите количество:", reply_markup=builder.as_markup())

# @dp.message(Command("mob"))
# async def mob(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     for zap, price in MOB.items():
#         builder.button(
#             text=f"{zap} - {price}",
#             callback_data=f"mob_{zap}"
#         )
#     builder.adjust(2)
#     await message.answer("Список товара для телефона:", reply_markup=builder.as_markup())

# @dp.callback_query(F.data.startswith("mob_"))
# async def choose_zap(callback: types.CallbackQuery):
#     zap = callback.data.split("_")[1]
#     orders[callback.from_user.id] = {"zap": zap, "category": "mob", "quantity": 1}

#     builder = InlineKeyboardBuilder()
#     for i in range(1, 6):
#         builder.button(
#             text=str(i),
#             callback_data=f"quantity_{i}"
#         )
#     builder.adjust(2)
#     await callback.message.answer(f"Вы выбрали {zap}. Укажите количество:", reply_markup=builder.as_markup())

# @dp.callback_query(F.data.startswith("quantity_"))
# async def choose_quantity(callback: types.CallbackQuery):
#     quantity = int(callback.data.split("_")[1])
#     user_id = callback.from_user.id

#     if user_id in orders:
#         category = orders[user_id]["category"]
#         if category == "avto":
#             spares = orders[user_id]["spares"]
#             price = AVTO[spares] * quantity
#         elif category == "mob":
#             zap = orders[user_id]["zap"]
#             price = MOB[zap] * quantity

#         orders[user_id]["quantity"] = quantity

#         builder = InlineKeyboardBuilder()
#         builder.button(
#             text="Подтвердить заказ",
#             callback_data="confirm_orders"
#         )

#         await callback.message.answer(
#             f"Ваш заказ: {spares if category == 'avto' else zap} x {quantity} = {price} сомов.\nПодтвердите заказ?",
#             reply_markup=builder.as_markup()
#         )

# @dp.callback_query(F.data == "confirm_orders")
# async def confirm_orders(callback: types.CallbackQuery):
#     user_id = callback.from_user.id

#     if user_id in orders:
#         category = orders[user_id]["category"]
#         if category == "avto":
#             spares = orders[user_id]["spares"]
#             quantity = orders[user_id]["quantity"]
#             total_price = AVTO[spares] * quantity
#         elif category == "mob":
#             zap = orders[user_id]["zap"]
#             quantity = orders[user_id]["quantity"]
#             total_price = MOB[zap] * quantity

#         del orders[user_id]

#         await callback.message.answer(
#             f"Спасибо за заказ!\nВы заказали: {spares if category == 'avto' else zap} x {quantity}.\nИтог к оплате: {total_price} сомов"
#         )

# async def main():
#     print("Запуск бота")
#     await dp.start_polling(bot)

# asyncio.run(main())
