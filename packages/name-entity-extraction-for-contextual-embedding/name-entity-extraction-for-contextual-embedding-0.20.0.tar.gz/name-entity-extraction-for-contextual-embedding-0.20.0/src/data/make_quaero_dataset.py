import logging
import pickle
import json
import glob
from logging.config import fileConfig
from os import path
from pathlib import Path

import click
import pandas as pd
import numpy as np
from transformers import BatchEncoding
from dotenv import find_dotenv, load_dotenv
from tqdm import tqdm
from sklearn.utils.class_weight import compute_class_weight

from src.models.utils import init_tokenizer

fileConfig(path.join(path.dirname(__file__), "../resources/log_config.ini"))
logger = logging.getLogger(__name__)


@click.command()
@click.option("--input-filepath", type=click.Path(), required=True)
@click.option("--output-filepath", type=click.Path(), required=True)
@click.option("--model-name", required=True)
def main(input_filepath: Path, output_filepath: Path, model_name: str):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info("making final data set from raw data")
    tokenizer = init_tokenizer(model_name)
    total_tokenized_labels = []
    with open(input_filepath, "rb") as file:
        quaero_dataset = pickle.load(file)
        corpus_labels = get_labels(quaero_dataset) + ["O"]
        quaero_dataset = sorted(
            quaero_dataset, key=lambda x: len(tokenizer.encode(x[0]))
        )
        for idx_example, example in enumerate(
            tqdm(quaero_dataset, position=1, leave=False, desc="pickle parsing")
        ):
            tokens = tokenizer(example[0], return_offsets_mapping=True)
            tokenized_labels = extract_tokenized_labels(tokens, example[1], "O")
            total_tokenized_labels += tokenized_labels
            id_labels = [corpus_labels.index(label) for label in tokenized_labels]
            data = {
                "sub_tokens_ids": tokens["input_ids"],
                "labels": tokenized_labels,
                "text": example[0],
                "sub_tokens": tokenizer.convert_ids_to_tokens(tokens["input_ids"])[
                    1:-1
                ],
                "labels_ids": id_labels,
            }
            write_file(output_filepath, idx_example, **data)
    weights = construct_weight_labels_dict(total_tokenized_labels, corpus_labels)
    write_metadata(output_filepath, corpus_labels, weights)


def write_file(output_filepath: Path, idx_example: int, **data: dict):
    normalize_index = str(idx_example).zfill(4)
    with open(f"{output_filepath}/quaero-{normalize_index}.pickle", "wb") as file:
        pickle.dump(data, file)
    with open(f"{output_filepath}/quaero-{normalize_index}.csv", "w") as file:
        csv = pd.DataFrame(columns=data.keys())
        for col, value in data.items():
            csv.at[0, col] = str(value) if isinstance(value, list) else value
        csv.to_csv(file)


def construct_weight_labels_dict(
    total_tokenized_labels: list, corpus_labels: list
) -> dict:
    labels_index = [corpus_labels.index(l) for l in corpus_labels]
    total_corpus_index = [corpus_labels.index(t) for t in total_tokenized_labels]
    weights = compute_class_weight(
        class_weight="balanced",
        classes=np.array(labels_index),
        y=np.array(total_corpus_index),
    )
    return {corpus_labels[idx]: weight for idx, weight in enumerate(weights)}


def write_metadata(output_filepath: Path, labels: list, weights: dict):
    files = glob.glob(f"{output_filepath}/*.pickle")
    len_files = len(files)
    len_labels = len(labels)
    with open(f"{output_filepath}/metadata.json", "w") as file:
        json.dump(
            {
                "files": files,
                "number of files": len_files,
                "labels": labels,
                "number of labels": len_labels,
                "labels weights": weights,
            },
            file,
        )


def get_labels(dataset: dict) -> list:
    entities = list(set(label[2] for el in dataset for label in el[1]["entities"]))
    entities = [[f"B-{entity}", f"I-{entity}"] for entity in entities]
    return [entity for ent_list in entities for entity in ent_list]


def extract_tokenized_labels(tokens: BatchEncoding, labels: dict, o_value: str) -> list:
    ids = tokens["input_ids"][1:-1]
    tokenized_labels = [o_value] * len(ids)
    offsets = tokens["offset_mapping"][1:-1]
    start_token = 0
    end_token = 0
    for label in list(labels.values())[0]:
        for idx_offset, offset in enumerate(offsets):
            if offset[0] == label[0]:
                start_token = idx_offset
            if offset[1] == label[1]:
                end_token = idx_offset
                break

        tokenized_labels[start_token : end_token + 1] = ["I-" + label[2]] * len(
            tokenized_labels[start_token : end_token + 1]
        )
        tokenized_labels[start_token] = "B-" + label[2]
    return [o_value] + tokenized_labels + [o_value]


if __name__ == "__main__":
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    # pylint: disable=no-value-for-parameter
    main()
