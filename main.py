
import logging
from aiogram import Bot, Dispatcher, types, executor

from aiogram.types import CallbackQuery

from db_utils import db_manager
import json
from random import randint

config = open('configs/config.json')
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
    await message.reply("Hi!\n\
                         I'm Holostyak bot!\n\
                         Powered by ABOBA.")

@dp.message_handler(commands = ['help'])
async def print_commands(message: types.Message):
    return await message.reply("/save - save new recipe\n     \
                                /delete - delete recipe\n     \
                                /idea - gives random dish\n   \
                                /show_all - shows all dishes?")

@dp.message_handler(commands=['save'])
async def save_idea(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (member.is_chat_admin()):
        # arguments = message.get_args()
        # db_man.add_row(message.chat.id, arguments)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text = "Add name", callback_data = "add_name"))
        keyboard.add(types.InlineKeyboardButton(text = "Add season", callback_data = "add_season"))
        keyboard.add(types.InlineKeyboardButton(text = "Add type", callback_data = "add_type"))

        await message.reply("Creating new idea", reply_markup = keyboard)
    else:
        await message.reply("You are not admin")

@dp.callback_query_handler(lambda c: c.data == 'add_name')
async def add_name(callback_query: CallbackQuery):
    await bot.send_message("Tadam")

@dp.message_handler(commands=['delete'])
async def save_idea(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (member.is_chat_admin()):
        arguments = message.get_args()
        if arguments.isnumeric():
            db_man.add_row(message.chat.id,arguments)
        else:
            await message.reply("You should place number of idea that you want delete after command /delete")
    else:
        await message.reply("You are not admin")

def idea2str(idea):
    """transform row about dish in format for user"""
    woNone = list(map(lambda x: "" if x==None else str(x), idea))
    out = "name: " + woNone[2] + "\ndescription: " + woNone[3] + "\ncooked: " + woNone[5]
    return out

@dp.message_handler(commands=['idea'])
async def give_idea(message: types.Message):
    """Gives random idea of what to cook"""
    records = db_man.get_all(message.chat.id)
    ind = randint(0,len(records))
    await message.reply(idea2str(records[ind]))

@dp.message_handler(commands=['show_all'])
async def save_idea(message: types.Message):
    """Saves idea what to cook in db. Only admins can do it"""
    records = db_man.get_all(message.chat.id)
    msg = "your ideas:\n"
    for record in records:
        for elem in record:
            msg+=str(elem)+" "
        msg+="\n"
    await message.reply(msg)


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)
