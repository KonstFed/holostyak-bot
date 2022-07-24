"""
In order to reduce the load on the database, we firstly 
collect all the ideas in this class, and send it when 
user finished his work with the idea.
"""

from aiogram.utils.markdown import text, bold

from enums.Season           import Season
from aiogram.types          import User, ParseMode
from configs.bot_config     import bot

class Idea:
    """
    Represents a new idea
    """

    # All the ideas that are not finished yet.
    current_ideas = dict()

    tmp_db = []

    def __init__(self, inline_message_id = None) -> None:
        self.name        = ''
        self.season      = Season.ANY
        self.author      = ''
        self.description = ''

        self.chat_id     = ''
        self.inline_message_id = inline_message_id

        self.edit_state  = ''
        self.number = len(self.tmp_db) # TODO: database

    # TODO: get idea number from database
    def __repr__(self) -> text:
        return bold('Idea number: ' + str(self.number)) + '\n\n' \
             + 'Idea: '        + self.name              + '\n'   \
             + 'Season: '      + self.season._name_     + '\n'   \
             + 'Author: '      + self.author            + '\n'   \
             + 'Description: ' + self.description

async def refresh_idea(from_user_id: User, inline_message_id: str, idea = None, keyboard = None):
    """
    Refreshes message sent from inline mode,
    used while editing idea
    """
    if idea is None:
        idea = Idea.current_ideas.get(from_user_id)
        if idea is None:
            return

    await bot.edit_message_text(text              = repr(idea), 
                                inline_message_id = inline_message_id, 
                                parse_mode        = ParseMode.MARKDOWN,
                                reply_markup      = keyboard
                               )