import configparser
import os
from pyrogram import Client


# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Create a Pyrogram client instance
app = Client(
    'my_bot',
    api_id=config['pyrogram']['api_id'],
    api_hash=config['pyrogram']['api_hash'],
    bot_token=config['pyrogram']['bot_token']
)

# Load command handlers from the 'handlers' folder
handlers_dir = 'handlers'
for filename in os.listdir(handlers_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = __import__(f'{handlers_dir}.{module_name}', fromlist=[module_name])
        module.register(app)

# Run the bot
print("BOT Alive")
app.run()

