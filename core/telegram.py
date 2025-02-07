from abc import ABC, abstractmethod
import logging

from telegram.ext import Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class BotTelegramCore(ABC):
    def __init__(self, token, port, server_url):
        logging.info('Inicializando o bot...')
        self.token = token
        self.port = port
        self.server_url = server_url

        self.updater = Updater(self.token)
        self.config_handlers()

    @abstractmethod
    def config_handlers(self):
        raise NotImplementedError('Cannot call config_handler from BotCore')

    def run_web(self):
        """Start the bot as a webhook server"""

        self.updater.start_webhook(
            listen="0.0.0.0",
            port=self.port,
            url_path=self.token
        )

        self.updater.bot.set_webhook(f"{self.server_url}/{self.token}")

        logging.info('Bot está rodando como um webserver!')
        self.updater.idle()

    def run_cmd(self):
        """Start the bot as a python script loop"""
        self.updater.start_polling()

        logging.info('Bot está rodando como um script python!')
        self.updater.idle()
