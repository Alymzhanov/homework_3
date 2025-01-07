from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
import asyncio, logging, os, aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

bot = Bot(token=os.environ.get("token"))
dp = Dispatcher()

user_data = {}

async def send_email(to_email, message_body):
    message = EmailMessage()
    message.set_content(message_body)
    message['Subject'] = 'Сообщение от бота'
    message['From'] = SMTP_USER
    message['To'] = to_email

    try:
        logging.info(f"Отправка сообщения на {to_email}")
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD
        )
        logging.info("Успешно отправлено")
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")

@dp.message(Command("start"))
async def start(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer(
        "Привет! Я бот, который отправит сообщение на указанную вами почту! "
        "Введите адрес электронной почты, чтобы продолжить."
    )

@dp.message(lambda message: "@" in message.text and "." in message.text)
async def email_handler(message: types.Message):
    user_id = message.from_user.id
    user_email = message.text.strip()
    user_data[user_id]["email"] = user_email
    await message.answer("Введите текст сообщения, которое нужно отправить.")

@dp.message(lambda message: message.from_user.id in user_data and "email" in user_data[message.from_user.id] and "message" not in user_data[message.from_user.id])
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text.strip()
    user_data[user_id]["message"] = user_message

    email = user_data[user_id]["email"]
    await message.answer(
        f"Вы хотите отправить следующее сообщение на {email}:\n\n"
        f"{user_message}\n\nПодтвердите отправку (Да/Нет)."
    )

@dp.message(lambda message: message.text.lower() in ["да", "нет"])
async def confirmation_handler(message: types.Message):
    user_id = message.from_user.id
    if message.text.lower() == "да":
        email = user_data[user_id]["email"]
        user_message = user_data[user_id]["message"]

        try:
            await send_email(email, user_message)
            await message.answer("Сообщение успешно отправлено!")
        except Exception as e:
            await message.answer(f"Не удалось отправить сообщение. Ошибка: {e}")

        user_data.pop(user_id, None)
    else:
        user_data.pop(user_id, None)
        await message.answer("Отправка отменена. Вы можете начать заново, введя адрес электронной почты.")

@dp.message(lambda message: "@" not in message.text or "." not in message.text)
async def error_handler(message: types.Message):
    await message.answer("Пожалуйста, введите корректный адрес электронной почты.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
