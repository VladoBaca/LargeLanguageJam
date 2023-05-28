import json
import sqlite3
from typing import List
from numpy import dot
from numpy.linalg import norm

from api.openai import get_vector
from init import db_model
from perturbator import perturb


def sentence_to_vector(sentence_text):
    text = sentence_text.split("\n")
    vector = json.dumps(get_vector(text[2]))
    return vector


def update_vector(sentence: sqlite3.Row, table="sentences"):
    vector = sentence_to_vector(sentence["text"])
    db_model.update_table(table, sentence["id"], vector=vector)


def pipeline():
    target_languages = [
        "cs", "da", "de", "en", "es", "et", "fi",
        "fr", "hr", "hu", "it", "lt", "lv", "mt",
        "nl", "pl", "pt", "ro", "sk", "sl", "sv"
    ]

    probs = [0.05, 0.1, 0.2, 0.3]

    for lang in target_languages:
        print(f"Starting lang {lang}")
        sentences = db_model.select_sentences(lang)
        for sentence in sentences:
            if sentence["vector"] is None:
                update_vector(sentence)
            perturbations = db_model.select_sentence_perturbations(sentence["id"])
            model_perturbations = {p["model"]: p for p in perturbations}
            for prob in probs:
                prob_key = f"prob{prob}"
                if prob_key in model_perturbations:
                    perturbation = model_perturbations[prob_key]
                    if perturbation["vector"] is None:
                        update_vector(perturbation, table="perturbations")
                else:
                    perturbed_text = perturb(sentence["text"], prob)
                    vector = sentence_to_vector(perturbed_text)
                    db_model.insert_perturbance(sentence["id"], perturbed_text, prob_key, vector)
            print(f"Sentence {sentence['id']} finished.")
        print(f"Language {lang} is finished.")
        print()


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
    pipeline()

    # update perturbation vectors
    #for pert in db_model.select_perturbances():
    #    if pert["vector"] is None:
    #        update_vector(pert, table="perturbations")

    #print(comparations())
