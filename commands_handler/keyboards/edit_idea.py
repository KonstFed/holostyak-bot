"""
Contains actions related to creating new idea.
"""

from aiogram                        import types
from aiogram.types                  import CallbackQuery, InlineKeyboardMarkup, ParseMode

from configs.bot_config             import bot, dp, db_man

from commands_handler.current_ideas import Idea

from enums.Season import Season

def edit_idea_kb():
    """
    Defines the keyboard for 'Create New Idea' menu
    """
    
    keyboard = InlineKeyboardMarkup()
    
    edit_name        = types.InlineKeyboardButton(text = 'Edit name'        , callback_data = 'edit_name'   )
    edit_season      = types.InlineKeyboardButton(text = 'Edit season'      , callback_data = 'edit_season' )
    edit_author      = types.InlineKeyboardButton(text = 'Edit author'      , callback_data = 'edit_author' )
    edit_description = types.InlineKeyboardButton(text = 'Edit description' , callback_data = 'edit_description' )

    edit_done        = types.InlineKeyboardButton(text = 'Done ✓'           , callback_data = 'edit_done'   )
    edit_cancel      = types.InlineKeyboardButton(text = 'Cancel 🞩'         , callback_data = 'edit_cancel')

    keyboard.row(edit_name, edit_season)
    keyboard.row(edit_author, edit_description)

    keyboard.add(edit_done)

    keyboard.add(edit_cancel)

    return keyboard

@dp.callback_query_handler(lambda c: c.data in ['edit_name', 'edit_author', 'edit_description'])
async def edit_idea(callback_query: CallbackQuery):
    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    field_name = callback_query.data[5::]

    await callback_query.answer(f"Print new {field_name} in the chat") 

    Idea.current_ideas[callback_query.from_user.id].edit_state = field_name

@dp.callback_query_handler(lambda c: c.data == 'edit_season')
async def choose_season(callback_query: CallbackQuery):
    from commands_handler.keyboards.choose_season import choose_season_kb
    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    await callback_query.answer('Choose season of the year: ')

    inline_message_id = Idea.current_ideas[callback_query.from_user.id].inline_message_id
    
    await bot.edit_message_reply_markup(reply_markup      = choose_season_kb(),
                                        inline_message_id = inline_message_id
                                       )

@dp.callback_query_handler(lambda c: c.data == 'edit_done')
async def finish_editing(callback_query: CallbackQuery):
    # In case if somebody already saved all changes - we do nothing.
    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    if Idea.current_ideas[callback_query.from_user.id].name == '':
        await callback_query.answer('Name cannot be empty') 
        return

    idea = Idea.current_ideas[callback_query.from_user.id]

    idea.edit_state = ''

    await callback_query.answer('Writing to database!') 

    # TODO: Add writing into database !!!!!!!!!!!
    # if current idea exist --> change 
    # else append
    does_exist = False
    
    for idea_db in Idea.tmp_db:
        if idea.number == idea_db.number:
            does_exist = True
            idea_db    = idea
            break

    if not does_exist:
        int_season = idea.season.value
        db_man.add_row(idea.name, idea.author, idea.description, int_season)
        Idea.tmp_db.append(idea)
    
    await bot.edit_message_reply_markup(inline_message_id = idea.inline_message_id, 
                                        reply_markup      = None)

    Idea.current_ideas.pop(callback_query.from_user.id)
     
@dp.callback_query_handler(lambda c: c.data == 'edit_cancel')
async def cancel_editing(callback_query: CallbackQuery):
    # In case if somebody already saved all changes - we do nothing.
    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    idea = Idea.current_ideas[callback_query.from_user.id]

    await bot.edit_message_text(inline_message_id = idea.inline_message_id,
                                parse_mode        = ParseMode.MARKDOWN,
                                text              = '*canceled*')

    Idea.last_id -= 1

    Idea.current_ideas.pop(callback_query.from_user.id)
