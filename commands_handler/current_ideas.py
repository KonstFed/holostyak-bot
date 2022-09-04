"""
In order to reduce the load on the database, we firstly 
collect all the ideas in this class, and send it when 
user finished his work with the idea.
"""

from aiogram.utils.markdown import text, bold

from enums.Season           import Season
from aiogram.types          import User, ParseMode

class Idea:
    """
    Represents a new idea
    """

    # All the ideas that are not finished yet.
    current_ideas = dict()
    
    last_id = 0

    tmp_db = []

    def __init__(self, inline_message_id = None) -> None:
        self.name        = ''
        self.season      = Season.ANY
        self.author      = ''
        self.description = ''

        self.chat_id     = ''
        self.inline_message_id = inline_message_id

        self.edit_state  = ''
        self.number = 0        

    # TODO: get idea number from database
    def __repr__(self) -> text:
        num = Idea.last_id + 1 if self.number == 0 else self.number
        return bold('Idea number: ' + str(num)) + '\n\n' \
             + 'Idea: '        + self.name              + '\n'   \
             + 'Season: '      + self.season._name_     + '\n'   \
             + 'Author: '      + self.author            + '\n'   \
             + 'Description: ' + self.description

    @classmethod
    def load_ideas_from_db(cls):
        # Get strings of all ideas that consist of
        # id, name, author, description, season (0, 1, 2, 3, 4), times_cooked 
        from configs.bot_config import db_man

        ideas = db_man.get_all()

        for idea_db in ideas:
            idea = Idea()
            idea.number      = idea_db[0]
            idea.name        = idea_db[1]
            idea.author      = idea_db[2]
            idea.description = idea_db[3]
            idea.season      = Season(idea_db[4])

            cls.tmp_db.append(idea)

        # get last_id
        cls.last_id = db_man.get_last_id()

    @classmethod
    def increase_last_id(cls):
        cls.last_id += 1
        return cls.last_id

async def refresh_idea(from_user_id: User, inline_message_id: str, idea = None, keyboard = None):
    """
    Refreshes message sent from inline mode,
    used while editing idea
    """
    from configs.bot_config import bot

    if idea is None:
        idea = Idea.current_ideas.get(from_user_id)
        if idea is None:
            return

    await bot.edit_message_text(text              = repr(idea), 
                                inline_message_id = inline_message_id, 
                                parse_mode        = ParseMode.MARKDOWN,
                                reply_markup      = keyboard
                               )