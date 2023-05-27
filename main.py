import json
import sqlite3

from api.openai import get_vector
from init import db_model
from time import sleep
from perturbator import perturb


def update_vector(sentence: sqlite3.Row):
    text = sentence["text"].split("\n")
    vector = json.dumps(get_vector(text[2]))
    db_model.update_sentence(sentence["id"], vector=vector)
    #sleep(1)


def pipeline():
    target_languages = [
        "cs", "da", "de", "en", "es", "et", "fi",
        "fr", "hr", "hu", "it", "lt", "lv", "mt",
        "nl", "pl", "pt", "ro", "sk", "sl", "sv"
    ]

    prob = 0.05

    for lang in target_languages:
        sentences = db_model.select_sentences(lang)
        for sentence in sentences:
            if sentence["vector"] is None:
                update_vector(sentence)
                
            perturbance = db_model.select_perturbance(sentence["id"])
            if perturbance is None:
                db_model.insert_perturbance(sentence["id"], perturb(sentence["text"], prob), f"prob{prob}")

        print(f"Language {lang} is finished.")

    sentences = db_model.select_sentences("cs")
    for sentence in sentences:
        if sentence["vector"] is None:
            update_vector(sentence)


if __name__ == "__main__":
    pipeline()
