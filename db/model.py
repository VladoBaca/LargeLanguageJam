import sqlite3
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class DBModel:

    def __init__(self, config):
        self.config = config
        self.connection = sqlite3.connect('db/database.sqlite')

    def select_sentences(self, language: str = "en", topic: Optional[int] = None) -> List[str]:
        # TODO here
        try:
            with self.connection as cursor:
                cursor.execute("SELECT * FROM sentences")
                return cursor.fetchall()
        except sqlite3.DatabaseError as ex:
            logging.warning(f"Could not select records: {ex}")
