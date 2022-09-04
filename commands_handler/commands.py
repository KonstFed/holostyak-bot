"""
This file contains description of all commands that
exist in bot and start with slash (/).
Also it includes processing of messages that are destinated to 
change the state of the idea.
"""


from aiogram                         import types
from random                          import randint

from configs.bot_config              import API_TOKEN, db_man, dp, bot

from commands_handler.current_ideas  import Idea
from commands_handler                import inline_handler

from commands_handler.keyboards.edit_idea import edit_idea_kb

from commands_handler.current_ideas import refresh_idea

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command.
    Initialise chat
    """
    await message.reply("Hi!\n"
                        "I'm Holostyak bot!\n"
                        "Powered by ABOBA.")

@dp.message_handler(commands = ['help'])
async def print_commands(message: types.Message):
    await message.reply("/save - save new recipe\n"
                        "/delete - delete recipe\n"
                        "/idea - gives random dish\n"
                        "/show_all - shows all dishes?")

@dp.message_handler(commands=['save'])
async def save_idea(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (member.is_chat_admin()):
        # arguments = message.get_args()
        # db_man.add_row(message.chat.id, arguments)

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text = "Add name"  , callback_data = "add_name"))
        keyboard.add(types.InlineKeyboardButton(text = "Add season", callback_data = "add_season"))
        keyboard.add(types.InlineKeyboardButton(text = "Add author", callback_data = "add_author"))

        await message.reply("Creating new idea", reply_markup = keyboard)
    else:
        await message.reply("You are not admin")

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

@dp.message_handler()
async def message_handler(message: types.Message):
    """
    Checks whether this message should change te state of the idea or not
    and if yes it changes it.
    """

    if message.via_bot != None and \
       message.via_bot.bot._BaseBot__token == API_TOKEN:
        await inline_command_handler(message)
        return

    # if the user don't have opened ideas
    if Idea.current_ideas.get(message.from_user.id) is None         \
    or Idea.current_ideas.get(message.from_user.id).edit_state == '':
        return

    idea = Idea.current_ideas[message.from_user.id]
    idea.__setattr__(idea.edit_state, message.md_text)
    idea.edit_state = ''

    await message.delete()

    await refresh_idea(message.from_user.id, idea.inline_message_id, None, edit_idea_kb())

async def inline_command_handler(message: types.Message):
    title = message.text.partition('\n')[0]
    
    match title:
        case inline_handler.create_idea_title:
            if (Idea.current_ideas.get(message.from_user.id) is None):
                Idea.current_ideas[message.from_user.id] = Idea()

            Idea.current_ideas[message.from_user.id].chat_id = message.chat.id
            Idea.last_id += 1
            Idea.current_ideas[message.from_user.id].number = Idea.last_id
        case _:
            pass