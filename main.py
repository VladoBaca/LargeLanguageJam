import json
import sqlite3
from typing import List
from numpy import dot
from numpy.linalg import norm

from api.openai import get_vector
from init import db_model
from perturbator import perturb


def update_vector(sentence: sqlite3.Row, table="sentences"):
    text = sentence["text"].split("\n")
    vector = json.dumps(get_vector(text[2]))
    db_model.update_table(table, sentence["id"], vector=vector)


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

def sim(vec1: List[float], vec2: List[float]):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def comparations():
    sentences_cz = db_model.select_sentences("cs")
    sentences_en = db_model.select_sentences("en")

    # compare 3 czech sentences
    print("Dist matrix for 3 CZ sentences")
    print(sim(json.loads(sentences_cz[0]['vector']), json.loads(sentences_cz[2]['vector'])))
    print(sim(json.loads(sentences_cz[2]['vector']), json.loads(sentences_cz[5]['vector'])))
    print(sim(json.loads(sentences_cz[0]['vector']), json.loads(sentences_cz[5]['vector'])))

    print("Dist matrix for 3 EN sentences")
    print(sim(json.loads(sentences_en[0]['vector']), json.loads(sentences_en[2]['vector'])))
    print(sim(json.loads(sentences_en[2]['vector']), json.loads(sentences_en[5]['vector'])))
    print(sim(json.loads(sentences_en[0]['vector']), json.loads(sentences_en[5]['vector'])))

    print("Same sentence in CZ and EN")
    print(sim(json.loads(sentences_cz[0]['vector']), json.loads(sentences_en[0]['vector'])))
    print(sim(json.loads(sentences_cz[2]['vector']), json.loads(sentences_en[2]['vector'])))
    print(sim(json.loads(sentences_cz[5]['vector']), json.loads(sentences_en[5]['vector'])))
    print("Some sentence in CZ and EN")
    print(sim(json.loads(sentences_cz[2]['vector']), json.loads(sentences_en[5]['vector'])))

    pert1 = db_model.select_perturbance(sentences_cz[0]['id'])
    pert2 = db_model.select_perturbance(sentences_cz[2]['id'])
    pert3 = db_model.select_perturbance(sentences_cz[5]['id'])

    print("3 sentences and their perturbances")
    print(sim(json.loads(sentences_en[0]['vector']), json.loads(pert1['vector'])))
    print(sim(json.loads(sentences_en[2]['vector']), json.loads(pert2['vector'])))
    print(sim(json.loads(sentences_en[5]['vector']), json.loads(pert3['vector'])))


if __name__ == "__main__":
    #pipeline()

    # update perturbation vectors
    #for pert in db_model.select_perturbances():
    #    if pert["vector"] is None:
    #        update_vector(pert, table="perturbations")

    print(comparations())
