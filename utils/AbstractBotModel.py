import json
from abc import abstractmethod
from types import SimpleNamespace

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .Singletone import SingletonABC


class AbstractBotModel(SingletonABC):

    def __init__(self, config_file_name='project.json'):
        with open(config_file_name, "r") as file:
            self.config = json.loads(file.read(), object_hook=lambda data: SimpleNamespace(**data))
        self._bot = Bot(token=self.config.api.token)
        self._memory_storage = MemoryStorage()
        self._dispatcher = Dispatcher(self._bot, storage=self._memory_storage)
        self._dispatcher.middleware.setup(LoggingMiddleware())

    def get_dispatcher(self):
        return self._dispatcher

    def get_bot(self):
        return self._bot

    def get_storage(self):
        return self._memory_storage

    @abstractmethod
    async def on_startup(self, _dispatcher):
        pass

    @abstractmethod
    async def on_shutdown(self, _dispatcher):
        logger.info("Closing storage...")
        await _dispatcher.storage.close()
        await _dispatcher.storage.wait_closed()
        logger.info("Bot shutdown...")

    @abstractmethod
    def start(self):
        pass
