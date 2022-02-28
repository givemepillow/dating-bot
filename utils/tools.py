from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook, start_polling
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from loguru import logger as log

from abc import ABC, abstractmethod
from types import SimpleNamespace
import json

from utils.singletone import SingletonABC


class AbstractModel(SingletonABC):

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
        log.info("Closing storage...")
        await _dispatcher.storage.close()
        await _dispatcher.storage.wait_closed()
        log.info("Bot shutdown...")

    @abstractmethod
    def start(self):
        pass


class WebhookModel(AbstractModel):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)
        await self._bot.set_webhook(self.config.webhook.host + self.config.webhook.path)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)
        await self._bot.delete_webhook()

    def start(self):
        log.warning("The application is running in webhook mode.")
        start_webhook(
            dispatcher=self._dispatcher,
            webhook_path=self.config.webhook.path,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
            skip_updates=True,
            host=self.config.webapp.host,
            port=self.config.webapp.port,
        )


class PollingModel(AbstractModel):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)

    def start(self):
        log.warning("The application is running in polling mode.")
        start_polling(
            dispatcher=self._dispatcher,
            skip_updates=True,
            on_shutdown=self.on_shutdown,
            on_startup=self.on_startup
        )
