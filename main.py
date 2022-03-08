import loguru

from handlers import dp as dispatcher
from loader import bot_engine

if __name__ == '__main__':
    loguru.logger.info(f"Number of message handlers: {len(dispatcher.message_handlers.handlers)}.")
    loguru.logger.info(f"Number of callback query handlers: {len(dispatcher.callback_query_handlers.handlers)}.")
    bot_engine.start()
