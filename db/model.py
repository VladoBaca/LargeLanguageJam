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
        try:
            with self.connection as cursor:
                query = "SELECT text, vector FROM sentences WHERE language = ?"
                vals = [language]
                if topic is not None:
                    query += " AND topic = ?"
                    vals.append(topic)
                cursor.execute(query, tuple(vals))
                results = cursor.fetchall()

                return results
        except sqlite3.DatabaseError as ex:
            logging.warning(f"Could not select records: {ex}")

    def insert_sentence(self, text: str, language: str = "en", topic: Optional[int] = None):
        query = "INSERT INTO sentences (text, language, topic_id) VALUES (?, ?, ?)"

        try:
            with self.connection as cursor:
                cursor.execute(query, (text, language, topic))
        except sqlite3.DatabaseError as ex:
            logger.error(ex)

    def update_sentence(self, s_id, **kwargs):
        query = "UPDATE playlist "
        vals = []
        for arg, val in kwargs.items():
            query += f", {arg}=?"
            vals.append(val)
        query += " WHERE id=?"
        vals.append(s_id)

        try:
            with self.connection as cursor:
                cursor.execute(query, tuple(vals))
        except sqlite3.DatabaseError as ex:
            logger.error(ex)
