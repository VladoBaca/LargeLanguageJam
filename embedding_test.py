#from openai.embeddings_utils import get_embedding
import os
import openai
openai.api_key = "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"


a0="Hello there! Is there a typo in this sentence? Are you sure?"
a1="Hello tuere! Is there a typo in this sentence? Are you sure?"
a2="HeNfz thure!wls ChOre v MQpk iV thisyZUibenWz? Aea FoC IFXeh"
a3=""


def get_vector(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]


print(len(get_vector(a0)))
print(len(get_vector(a1)))
