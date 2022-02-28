import loguru

from handlers import dp
from loader import bot_engine

if __name__ == '__main__':
    loguru.logger.info(f"Number of handlers: {len(dp.message_handlers.handlers)}.")
    bot_engine.start()
