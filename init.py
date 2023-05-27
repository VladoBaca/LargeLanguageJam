from api.openai import OpenAIAPI
from config import Config
from db import DBModel
from logger import Logger

config = Config()
logger = Logger(config)
openai_api = OpenAIAPI(config)

db_model = DBModel(config)
