from aiogram            import executor
from configs.bot_config import dp

import commands_handler.inline_handler
import commands_handler.commands

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)
