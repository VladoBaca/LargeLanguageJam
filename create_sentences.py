"""
"""

import datasets
from datasets.arrow_dataset import DatasetDict


def extract_3_lines(example: DatasetDict) -> DatasetDict:
    for lang in example['text']:
        example['text'][lang] = '\n'.join(example['text'][lang].split('\n')[0:3])
    return example


if __name__ == "__main__":
    # dl dataset
    ds_constructor = datasets.load_dataset("multi_eurlex", "all_languages", split='test')
    # shuffle (for topic diversity)
    ds_shuff = ds_constructor.shuffle(seed=42)
    # select first 100 docs
    ds_sample = ds_shuff.select(range(100))
    # extract first 3 lines
    ds_sample = ds_sample.map(extract_3_lines)
    # export
    ds_sample.to_json('data/sentences.json')
