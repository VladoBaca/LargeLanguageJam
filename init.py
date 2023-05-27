from config import Config
from db import DBModel
from logger import Logger

config = Config()
logger = Logger(config)

db_model = DBModel(config)
