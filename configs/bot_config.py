from aiogram                        import Bot, Dispatcher
from commands_handler.current_ideas import Idea
from database.db_utils              import db_manager

import json
import logging

config    = open('configs/config.json')
config    = json.load(config)
API_TOKEN = config['bot']['token']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp  = Dispatcher(bot)

db_man = db_manager(config['db'])

Idea.load_ideas_from_db()