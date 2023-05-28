import sqlite3
import logging
from .connection import ConnManager
from typing import List, Optional

logger = logging.getLogger(__name__)


class DBModel:

    def __init__(self, config):
        self.config = config
        self.connection = ConnManager()

    def select_sentences(self, language: str = "en", topic: Optional[int] = None) -> List[sqlite3.Row]:
        try:
            with self.connection as cursor:
                query = "SELECT id, text, vector FROM sentences WHERE language = ?"
                vals = [language]
                if topic is not None:
                    query += " AND topic = ?"
                    vals.append(topic)
                cursor.execute(query, tuple(vals))
                results = cursor.fetchall()

                return results
        except sqlite3.DatabaseError as ex:
            logging.warning(f"Could not select records: {ex}")

    def select_perturbance(self, sentence_id: int) -> Optional[sqlite3.Row]:
        try:
            with self.connection as cursor:
                query = "SELECT text, vector FROM perturbations WHERE sentence_id = ?"
                vals = [sentence_id]
                cursor.execute(query, tuple(vals))
                return cursor.fetchone()
        except sqlite3.DatabaseError as ex:
            logging.warning(f"Could not select perturbance: {ex}")

    def select_perturbances(self):
        try:
            with self.connection as cursor:
                query = "SELECT id, text, vector FROM perturbations"
                cursor.execute(query)
                return cursor.fetchall()
        except sqlite3.DatabaseError as ex:
            logging.warning(f"Could not select perturbance: {ex}")

    def insert_sentence(self, text: str, language: str = "en", topic: Optional[int] = None):
        query = f"INSERT INTO sentences (text, language, topic_id) VALUES (?, ?, ?)"

        try:
            with self.connection as cursor:
                cursor.execute(query, (text, language, topic))
        except sqlite3.DatabaseError as ex:
            logger.error(ex)

    def insert_perturbance(self, sentence_id: int, text: str, model: str):
        query = f"INSERT INTO perturbations (sentence_id, text, model) VALUES (?, ?, ?)"

        try:
            with self.connection as cursor:
                cursor.execute(query, (sentence_id, text, model))
        except sqlite3.DatabaseError as ex:
            logger.error(ex)

    def update_sentence(self, s_id, **kwargs):
        self.update_table("sentences", s_id, **kwargs)

    def update_perturbance(self, s_id, **kwargs):
        self.update_table("perturbations", s_id, **kwargs)

    def update_table(self, table_name, s_id, **kwargs):
        query = f"UPDATE {table_name} SET"
        vals = []
        for arg, val in kwargs.items():
            query += f" {arg}=?,"
            vals.append(val)
        query = query[:len(query) - 1] + " WHERE id=?"
        vals.append(s_id)

        try:
            with self.connection as cursor:
                cursor.execute(query, tuple(vals))
        except sqlite3.DatabaseError as ex:
            logger.error(ex)
