"""
This file contains methods related to inline menu
(buttons, icons, and related functions).
"""

from aiogram.types                             import InlineQuery, User, ParseMode
from aiogram                                   import types

from commands_handler.current_ideas            import Idea
from commands_handler.keyboards.choose_idea    import choose_idea_kb

from configs.bot_config                        import bot, dp
from commands_handler.keyboards.edit_idea      import edit_idea_kb
from enums.ChooseAction                        import ChooseAction

icon_idea = 'https://cdn-icons-png.flaticon.com/512/427/427735.png'
icon_edit = 'https://cdn-icons-png.flaticon.com/512/2921/2921179.png'

create_idea_title = 'Creating new idea...'

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
                                    new_idea(inline_query.from_user.id),
                                    edit_idea(inline_query.from_user.id)
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
            if (Idea.current_ideas.get(chosen_result.from_user.id) is None):
                Idea.current_ideas[chosen_result.from_user.id] = Idea()

            Idea.current_ideas[chosen_result.from_user.id].inline_message_id = chosen_result.inline_message_id
            
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
        keyboard          = edit_idea_kb()

    return types.InlineQueryResultArticle (
        id = '1', title = 'Add new idea',
        description = idea_description, 
        reply_markup = keyboard,
        thumb_url    = icon_idea, 
        thumb_width  = 48, 
        thumb_height = 48,
        input_message_content = types.InputTextMessageContent(
                                    message_text = create_idea_title + '\n\n' + idea_message_text,
                                    parse_mode   = ParseMode.MARKDOWN
                                )
    )

def edit_idea(user: User):
    idea_description  = 'You can edit already existing ideas'
    idea_message_text = 'Choose idea to edit'

    keyboard = None

    if Idea.current_ideas.get(user) is not None:
        idea_description  = 'You should finish editing previous idea before starting new one'
        idea_message_text = 'No-no - finish with previous idea first'
    else:
        keyboard          = choose_idea_kb(ChooseAction.EDIT, 1)

    return types.InlineQueryResultArticle (
        id = '2', title = 'Edit idea',
        description  = idea_description, 
        reply_markup = keyboard,
        thumb_url    = icon_edit, 
        thumb_width  = 48, 
        thumb_height = 48,
        input_message_content = types.InputTextMessageContent(
                                    message_text = idea_message_text,
                                    parse_mode   = ParseMode.MARKDOWN
                                )
    )
    