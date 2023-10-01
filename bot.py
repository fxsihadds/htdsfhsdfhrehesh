_A='pyrogram'
import configparser,os
from pyrogram import Client
config=configparser.ConfigParser()
config.read('config.ini')
app=Client('my_bot',api_id=config[_A]['api_id'],api_hash=config[_A]['api_hash'],bot_token=config[_A]['bot_token'])
handlers_dir='handlers'
users_dir='users'
for filename in os.listdir(handlers_dir):
	if filename.endswith('.py'):module_name=filename[:-3];module=__import__(f"{handlers_dir}.{module_name}",fromlist=[module_name]);module.register(app)
for filename in os.listdir(users_dir):
	if filename.endswith('.py'):module_name=filename[:-3];module=__import__(f"{users_dir}.{module_name}",fromlist=[module_name]);module.register(app)
print('BOT Alive')
app.run()
