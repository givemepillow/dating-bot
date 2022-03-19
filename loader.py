import locale

from sqlalchemy.orm import sessionmaker

from utils import WebhookModel, PollingModel
from orm import create_database_engine
from repository import SqlAlchemyRepository

import argparse

__all__ = ['dp', 'bot_engine', 'bot', 'repository']

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

parser = argparse.ArgumentParser("main.py")
parser.add_argument("--mode", "-m", nargs=1,
                    help="Run the application in polling mode or webhook mode.",
                    default='polling',
                    choices=['polling', 'webhook']
                    )

args = parser.parse_args()

db_engine = create_database_engine(
    database_engine='postgres',
    drop=False,
    create=True,
    echo=False,
    data_source='settlements.csv'
)

Session = sessionmaker(bind=db_engine)

repository = SqlAlchemyRepository(Session=Session)

bot_engine = WebhookModel() if args.mode[0] == 'webhook' else PollingModel()
memory_storage = bot_engine.get_storage()
dp = bot_engine.get_dispatcher()
bot = bot_engine.get_bot()
