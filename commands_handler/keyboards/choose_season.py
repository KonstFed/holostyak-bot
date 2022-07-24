from aiogram                        import types
from aiogram.types                  import CallbackQuery, InlineKeyboardMarkup

from configs.bot_config             import bot, dp

from commands_handler.current_ideas import Idea

from enums.Season                         import Season

from commands_handler.current_ideas      import refresh_idea

def choose_season_kb():
    keyboard = InlineKeyboardMarkup()

    winter = types.InlineKeyboardButton(text = 'Winter', callback_data = 'WINTER')
    spring = types.InlineKeyboardButton(text = 'Spring', callback_data = 'SPRING')
    summer = types.InlineKeyboardButton(text = 'Summer', callback_data = 'SUMMER')
    autumn = types.InlineKeyboardButton(text = 'Autumn', callback_data = 'AUTUMN')

    keyboard.row(winter, spring)
    keyboard.row(summer, autumn)

    keyboard.add(types.InlineKeyboardButton(text = 'Any', callback_data = 'ANY'))

    keyboard.add(types.InlineKeyboardButton(text = '« back', callback_data = 'back_to_creating_idea'))

    return keyboard

@dp.callback_query_handler(lambda c: c.data in Season._member_names_)
async def choosing_season(callback_query: CallbackQuery):
    from commands_handler.keyboards.edit_idea import edit_idea_kb

    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return

    idea = Idea.current_ideas[callback_query.from_user.id]
    idea.season = Season.__getitem__(callback_query.data)

    await refresh_idea(callback_query.from_user.id, idea.inline_message_id, None, edit_idea_kb())

@dp.callback_query_handler(lambda c: c.data == 'back_to_creating_idea')
async def back_to_creating_idea(callback_query: CallbackQuery):
    from commands_handler.keyboards.edit_idea import edit_idea_kb

    if Idea.current_ideas.get(callback_query.from_user.id) is None:
        await callback_query.answer('Only user who created idea can edit it now') 
        return
    
    inline_message_id = Idea.current_ideas[callback_query.from_user.id].inline_message_id

    await bot.edit_message_reply_markup(reply_markup      = edit_idea_kb(),
                                        inline_message_id = inline_message_id
                                       )