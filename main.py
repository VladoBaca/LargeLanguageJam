import json
import sqlite3

from api.openai import get_vector
from init import db_model


def update_vector(sentence: sqlite3.Row):
    vector = json.dumps(get_vector(sentence["text"]))
    db_model.update_sentence(sentence["id"], vector=vector)


def pipeline():
    sentences = db_model.select_sentences("cz")
    for sentence in sentences:
        if sentence["vector"] is None:
            update_vector(sentence)


if __name__ == "__main__":
    pipeline()
