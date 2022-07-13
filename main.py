
import logging
from unittest import skip
from aiogram import Bot, Dispatcher, types, executor
from click import argument

from db_utils import db_manager
import json

config = open('config.json')
config = json.load(config)
API_TOKEN = config['bot']['token']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


db_man = db_manager(config['db'])


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command.
    Initialise chat
    """
    await message.reply("Hi!\nI'm Holostyak bot!\nPowered by ABOBA.")



@dp.message_handler(commands=['save'])
async def save_idea(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (member.is_chat_admin()):
        arguments = message.get_args()
        db_man.add_row(message.chat.id,arguments)
        await message.reply("your arguments: " + arguments)
    else:
        await message.reply("You are not admin")


@dp.message_handler(commands=['show_all'])
async def save_idea(message: types.Message):
    records = db_man.get_all(message.chat.id)
    msg = "your ideas:\n"
    for record in records:
        for elem in record:
            msg+=str(elem)+" "
        msg+="\n"
    await message.reply(msg)


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)