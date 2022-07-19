"""
In order to reduce the load on the database, we firstly 
collect all the ideas in this class, and send it when 
user finished his work with the idea.
"""

from aiogram.utils.markdown import text, bold

class Idea:
    """
    Represents a new idea
    """

    # All the ideas that are not finished yet.
    current_ideas = dict()

    def __init__(self, inline_message_id = None) -> None:
        self.name      = ''
        self.season    = ''
        self.author    = ''

        self.inline_message_id = inline_message_id

        self.edit_state = ''

    # TODO: get idea number from database
    def __repr__(self) -> text:
        return bold('Idea number: 1')      + '\n\n' \
             + 'idea: '   + self.name      + '\n'   \
             + 'season: ' + self.season    + '\n'   \
             + 'author: ' + self.author