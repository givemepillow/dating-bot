from .AbstractBotModel import AbstractBotModel
from aiogram.utils.executor import start_polling

from loguru import logger


class PollingModel(AbstractBotModel):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)

    def start(self):
        logger.warning("The application is running in polling mode.")
        start_polling(
            dispatcher=self._dispatcher,
            skip_updates=True,
            on_shutdown=self.on_shutdown,
            on_startup=self.on_startup
        )
