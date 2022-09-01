"""
This file contains methods related to inline menu
(buttons, icons, and related functions).
"""
import random

from aiogram.types                             import InlineQuery, User, ParseMode
from aiogram                                   import types

from commands_handler.current_ideas            import Idea
from commands_handler.keyboards.choose_idea    import choose_idea_kb

from configs.bot_config                        import bot, dp
from commands_handler.keyboards.edit_idea      import edit_idea_kb
from enums.ChooseAction                        import ChooseAction

icon_idea        = 'https://cdn-icons-png.flaticon.com/512/427/427735.png'
icon_edit        = 'https://cdn-icons-png.flaticon.com/512/2921/2921179.png'
icon_delete      = 'https://cdn-icons-png.flaticon.com/512/3221/3221897.png'
icon_show_all    = 'https://cdn-icons-png.flaticon.com/512/3534/3534031.png'
icon_get_random  = 'https://cdn-icons.flaticon.com/png/512/5726/premium/5726624.png?token=exp=1658657095~hmac=0621f33a59e91b91e57eb800d50670bf'

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
                                    edit_idea(inline_query.from_user.id),
                                    delete_idea(inline_query.from_user.id),
                                    get_random_idea(),
                                    show_all_ideas()
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
    elif len(Idea.tmp_db) == 0:
        idea_description  = 'Nothing to edit'
        idea_message_text = 'Okay, may be you want to try to delete something?'
    else:
        keyboard          = choose_idea_kb(ChooseAction.EDIT)

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

def delete_idea(user: User):
    idea_description  = 'You can delete already existing ideas'
    idea_message_text = 'Choose idea to delete'

    keyboard = None

    if Idea.current_ideas.get(user) is not None:
        idea_description  = 'You should finish editing previous idea before starting new one'
        idea_message_text = 'No-no - finish with previous idea first'
    elif len(Idea.tmp_db) == 0:
        idea_description  = 'Nothing to delete'
        idea_message_text = 'See? Nothing to delete :)'
    else:
        keyboard          = choose_idea_kb(ChooseAction.DELETE)

    return types.InlineQueryResultArticle (
        id = '3', title = 'Delete idea',
        description  = idea_description, 
        reply_markup = keyboard,
        thumb_url    = icon_delete, 
        thumb_width  = 48, 
        thumb_height = 48,
        input_message_content = types.InputTextMessageContent(
                                    message_text = idea_message_text,
                                    parse_mode   = ParseMode.MARKDOWN
                                )
    )

def get_random_idea():
    idea_description  = 'You can get random idea from your list'
    idea_message_text = 'I know what you are going to do tonight! You will do ...'

    if len(Idea.tmp_db) == 0:
        idea_description  = 'Hm.. It seams that you still do not have an idea. What could that mean?'
        idea_message_text = 'Abrakadabra! And from zero ideas you get nothing!\nAh, wait, I have an idea - you want to add an idea!'
    else:
        idea_message_text = repr(random.choice(Idea.tmp_db))

    return types.InlineQueryResultArticle (
        id = '4', title = 'Get random idea',
        description  = idea_description, 
        thumb_url    = icon_get_random, 
        thumb_width  = 48, 
        thumb_height = 48,
        input_message_content = types.InputTextMessageContent(
                                    message_text = idea_message_text,
                                    parse_mode   = ParseMode.MARKDOWN
                                )
    )

def show_all_ideas():
    idea_description  = 'You can see all existing ideas'
    idea_message_text = 'Show me all our ideas!'

    keyboard = None

    if len(Idea.tmp_db) == 0:
        idea_description  = 'You do not have ideas :( may be you want to add one?'
        idea_message_text = 'No, adding button is different, try again :)'
    else:
        keyboard          = choose_idea_kb(ChooseAction.SHOW)

    return types.InlineQueryResultArticle (
        id = '5', title = 'Show all ideas',
        description  = idea_description, 
        reply_markup = keyboard,
        thumb_url    = icon_show_all, 
        thumb_width  = 48, 
        thumb_height = 48,
        input_message_content = types.InputTextMessageContent(
                                    message_text = idea_message_text,
                                    parse_mode   = ParseMode.MARKDOWN
                                )
    )
