"""
This file contains methods related to inline menu
(buttons, icons, and related functions).
"""

from aiogram.types                             import InlineQuery, User, ParseMode
from aiogram                                   import types

from commands_handler.current_ideas            import Idea

from configs.bot_config                        import bot, dp
from commands_handler.inline_actions.new_idea  import new_idea_kb

icon_idea = 'https://cdn-icons-png.flaticon.com/512/427/427735.png'

@dp.inline_handler()
async def query_handler(inline_query: InlineQuery):
    """
    Adds buttons in inline menu.

    Params
    ------
    inline_query - object of current query
    """

    await bot.answer_inline_query(inline_query.id, 
                                  results = [
                                    new_idea(inline_query.from_user.id)
                                  ], 
                                  cache_time=1)
    
@dp.chosen_inline_handler()
async def chosen_handler(chosen_result: types.ChosenInlineResult):
    """
    Handle part of the action that happens 
    after pressing button in inline menu.

    Param
    -----
    chosen_result - contains info about pressed button
    """

    match chosen_result.result_id:
        case '1':  
            Idea.current_ideas[chosen_result.from_user.id] = Idea(chosen_result.inline_message_id)
        case _:
            pass # then we do nothing

def new_idea(user: User):
    """
    Creates 'New Idea' button in inline menu.

    Param
    -----
    user - user that called this menu
    """

    idea_description  = 'Suggest new idea!'
    idea_message_text = repr(Idea())

    keyboard = None

    if Idea.current_ideas.get(user) is not None:
        idea_description  = 'You should finish editing previous idea before starting new one'
        idea_message_text = 'No-no - finish with previous idea first'
    else:
        keyboard                    = new_idea_kb()

    return types.InlineQueryResultArticle (
        id = '1', title = 'Add new idea',
        description = idea_description, 
        reply_markup = keyboard,
        thumb_url    = icon_idea, 
        thumb_width  = 48, 
        thumb_height = 48,
        input_message_content = types.InputTextMessageContent(
                                    message_text = idea_message_text,
                                    parse_mode   = ParseMode.MARKDOWN
                                )
    )



    