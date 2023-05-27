import logging

import openai
from init import config

logger = logging.getLogger(__name__)
openai.api_key = config.openai_api["url"]


def get_vector(text: str):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]
