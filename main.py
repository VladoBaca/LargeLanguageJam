from init import db_model
from api.openai import get_vector


if __name__ == "__main__":
    db_model.insert_sentence("Ahoj svete", "cz")

    sentences = db_model.select_sentences("cz")
    for sentence in sentences:
        print(sentence["text"])
        if sentence["vector"] is None:
            # TODO vector
            db_model.update_sequence(sentence["id"], vector)
