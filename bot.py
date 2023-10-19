import configparser
import os
import logging
from pyrogram import Client
from pyrogram.types import Message


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read('config.ini')

plugins = dict(
    root="plugins",
)


handlers_dir = 'handlers'
users_dir = 'users'


app = Client(
    'my_bot',
    api_id=config['pyrogram']['api_id'],
    api_hash=config['pyrogram']['api_hash'],
    bot_token=config['pyrogram']['bot_token'],
    plugins=plugins,
    workers=10
)

for filename in os.listdir(handlers_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = __import__(
            f'{handlers_dir}.{module_name}', fromlist=[module_name])
        module.register(app)

for filename in os.listdir(users_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = __import__(f'{users_dir}.{module_name}',
                            fromlist=[module_name])
        module.register(app)


app.run()
