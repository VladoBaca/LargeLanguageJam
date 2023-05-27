import sqlite3
import logging
from .connection import ConnManager
from typing import List, Optional

logger = logging.getLogger(__name__)


class DBModel:

    def __init__(self, config):
        self.config = config
        self.connection = ConnManager()

    def select_sentences(self, language: str = "en", topic: Optional[int] = None) -> List[str]:
        # TODO here
        try:
            with self.connection as cursor:
                query = "SELECT text FROM sentences WHERE language = ?"
                keywords = [language]
                if topic is not None:
                    query += " AND topic = ?"
                    keywords.append(topic)
                cursor.execute(query, tuple(keywords))
                results = cursor.fetchall()

                return results
        except sqlite3.DatabaseError as ex:
            logging.warning(f"Could not select records: {ex}")
