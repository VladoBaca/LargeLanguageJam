from init import db_model

if __name__ == "__main__":
    sentences = db_model.select_sentences("cz")
    for sentence in sentences:
        print(sentence["text"])
