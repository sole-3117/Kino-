import os 
from dotenv import load_dotenv 
load_dotenv() BOT_TOKEN = os.getenv('BOT_TOKEN') MAIN_ADMIN = int(os.getenv('MAIN_ADMIN', '6887251996'))
DATABASE_PATH = os.getenv('DATABASE_PATH', './bot.db')

