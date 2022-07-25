"""
Contains actions related to creating new idea.
"""

from aiogram                        import types
from aiogram.types                  import CallbackQuery, InlineKeyboardMarkup, User, ParseMode

from configs.bot_config             import bot, dp, db_man

from commands_handler.current_ideas import Idea


async def refresh_new_idea(from_user: User, inline_message: str, keyboard = None):
    """
    Refreshes message sent from inline mode,
    used while editing idea
    """
    if Idea.current_ideas.get(from_user) is None:
        return

    await bot.edit_message_text(text              = repr(Idea.current_ideas[from_user]), 
                                inline_message_id = inline_message, 
                                parse_mode        = ParseMode.MARKDOWN,
                                reply_markup      = new_idea_kb()
                               )

def new_idea_kb():
    """
    Defines the keyboard for 'Create New Idea' menu
    """
    
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(types.InlineKeyboardButton(text = 'Edit name'   , callback_data = 'edit_name'   ))
    keyboard.add(types.InlineKeyboardButton(text = 'Edit season' , callback_data = 'edit_season' ))
    keyboard.add(types.InlineKeyboardButton(text = 'Edit author' , callback_data = 'edit_author' ))
    keyboard.add(types.InlineKeyboardButton(text = 'Done'        , callback_data = 'edit_done'   ))

    return keyboard

@dp.callback_query_handler(lambda c: c.data in ['edit_name', 'edit_season', 'edit_author'])
async def add_name(callback_query: CallbackQuery):
    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    field_name = callback_query.data[5::]

    await callback_query.answer(f"Print new {field_name} in the chat") 

    Idea.current_ideas[callback_query.from_user.id].edit_state = field_name

@dp.callback_query_handler(lambda c: c.data == 'edit_done')
async def add_name(callback_query: CallbackQuery):
    # In case if somebody already saved all changes - we do nothing.
    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    idea = Idea.current_ideas[callback_query.from_user.id]

    idea.edit_state = ''

    await callback_query.answer('Writing to database!') 

    # TODO: Add writing into database !!!!!!!!!!!
    db_man.add_row(callback_query.chat_instance,idea.name, idea.author, idea.season)
    
    await bot.edit_message_reply_markup(inline_message_id = idea.inline_message_id, 
                                        reply_markup      = None)

    Idea.current_ideas.pop(callback_query.from_user.id)
     