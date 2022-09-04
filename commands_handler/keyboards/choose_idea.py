from math                                 import ceil
from aiogram                              import types
from aiogram.types                        import CallbackQuery, InlineKeyboardMarkup, ParseMode
from commands_handler.current_ideas       import refresh_idea
from commands_handler.keyboards.edit_idea import edit_idea_kb

from configs.bot_config                   import bot, dp, db_man

from commands_handler.current_ideas       import Idea

from enums.ChooseAction                   import ChooseAction
from aiogram.utils.callback_data          import CallbackData

idea_data = CallbackData('idea_no', 'number', 'action')
page_data = CallbackData('page_no', 'number', 'action')

def choose_idea_kb(action: ChooseAction, page_no = 1):
    page_size = 4

    keyboard = InlineKeyboardMarkup()
    
    first_idea = (page_no - 1) * page_size
    last_idea  = first_idea    + page_size

    max_page_no = ceil(len(Idea.tmp_db) / page_size)

    close_button = types.InlineKeyboardButton(text = 'Close', callback_data = 'close_choose_menu')

    if max_page_no == 0:
        keyboard.add(close_button)
        return keyboard

    ideas = Idea.tmp_db[first_idea:last_idea]

    for idea in ideas:
        keyboard.add(types.InlineKeyboardButton(text = idea.name, 
                                                callback_data = idea_data.new(
                                                    number = idea.number,
                                                    action = action.name
                                                )))

    back_button    = types.InlineKeyboardButton(text   = '«', callback_data = page_data.new(
                                                    number = (page_no - 1),
                                                    action = action.name
                                                ))
    forward_button = types.InlineKeyboardButton(text   = '»', callback_data = page_data.new(
                                                    number = (page_no + 1),
                                                    action = action.name
                                                ))

    page_counter   = types.InlineKeyboardButton(text = str(page_no) + '/' + str(max_page_no), 
                                                callback_data = 'page_counter')
    if max_page_no == 1:
        keyboard.row(page_counter)
    elif page_no == 1:
        keyboard.row(page_counter, forward_button)
    elif page_no == max_page_no:
        keyboard.row(back_button, page_counter)
    else:
        keyboard.row(back_button, page_counter, forward_button)

    keyboard.add(close_button)

    return keyboard

@dp.callback_query_handler(lambda c: c.data == 'close_choose_menu')
async def get_idea(callback_query: CallbackQuery):
    await bot.edit_message_text(
            inline_message_id = callback_query.inline_message_id, 
            text              = '*closed*',
            parse_mode        = ParseMode.MARKDOWN
        )

@dp.callback_query_handler(lambda c: c.data.startswith('idea_no'))
async def get_idea(callback_query: CallbackQuery):
    number = int(callback_query.data.split(':')[1])
    action = callback_query.data.split(':')[2]

    idea = get_idea_by_number(number, callback_query)

    match action:
        case ChooseAction.EDIT.name:
            Idea.current_ideas[callback_query.from_user.id] = idea
            await refresh_idea(callback_query.from_user.id, callback_query.inline_message_id, idea, edit_idea_kb())
        case ChooseAction.DELETE.name:
            db_man.delete_row(idea.number)
            Idea.tmp_db.remove(idea)
            await bot.edit_message_reply_markup(inline_message_id = callback_query.inline_message_id,
                                                reply_markup      = choose_idea_kb(ChooseAction[action], 1))
        case ChooseAction.SHOW.name:
            await refresh_idea(callback_query.from_user.id, callback_query.inline_message_id, idea)
        case _:
            pass # do nothing

@dp.callback_query_handler(lambda c: c.data.startswith('page_no'))
async def change_page(callback_query: CallbackQuery):
    number    = int(callback_query.data.split(':')[1])
    action    = ChooseAction[callback_query.data.split(':')[2]]

    await bot.edit_message_reply_markup(reply_markup = choose_idea_kb(action, number),
                                        inline_message_id = callback_query.inline_message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('page_counter'))
async def get_idea(callback_query: CallbackQuery):
    pass # We do nothing here

def get_idea_by_number(number: int, callback_query: CallbackQuery):
    for idea in Idea.tmp_db:
        if idea.number == number:
            idea.inline_message_id = callback_query.inline_message_id
            return idea

    return None
