from .AbstractBotModel import AbstractBotModel
from aiogram.utils.executor import start_webhook

from loguru import logger


class WebhookModel(AbstractBotModel):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)
        await self._bot.set_webhook(self.config.webhook.host + self.config.webhook.path)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)
        await self._bot.delete_webhook()

    def start(self):
        logger.warning("The application is running in webhook mode.")
        start_webhook(
            dispatcher=self._dispatcher,
            webhook_path=self.config.webhook.path,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
            skip_updates=True,
            host=self.config.webapp.host,
            port=self.config.webapp.port,
        )
