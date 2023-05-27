"""
"""

import json
from init import db_model


def insert_language(target_language: str) -> None:

    with open("data/sentences.json", "r") as f:
        sentences = [json.loads(l) for l in f.readlines()]
    
    for sentence in sentences:
        text = sentence['text'][target_language]
        language = target_language
        celex_id = sentence['celex_id']
        
        db_model.insert_sentence(text=text, language=language, topic=celex_id)


if __name__ == "__main__":

    target_languages = [
        "cs", "da", "de", "en", "es", "et", "fi",
        "fr", "hr", "hu", "it", "lt", "lv", "mt",
        "nl", "pl", "pt", "ro", "sk", "sl", "sv"
        ]

    for lang in target_languages:
        insert_language(lang)
