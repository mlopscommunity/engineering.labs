import os
import logging
import asyncio
import argparse
import random
import requests
import zipfile
from pathlib import Path
from typing import Mapping

import pandas as pd
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

from preprocessing import preprocess, build_matrix
from utils import file_exists, verify_checksum, run_subproc, dump_pds
from config import (
    DATASET_FILE,
    CHECKSUMS,
    DATASET_SIZE,
    X_COLUMN,
    Y_COLUMNS,
    TOKENIZER_WORDS,
    RANDOM_SEED,
    MAX_FEATURES,
    TRAIN_SIZE,
    SEQUENCE_MAX_LEN,
)


async def main():
    call_args = get_args()
    config_env(call_args.random_seed, call_args.log_level)

    # Kaggle stores compressed files with ".zip" suffix
    dataset_file_path: Path = call_args.storage_path / (DATASET_FILE + ".zip")
    await load_dataset(
        ds_name=call_args.dataset_name,
        ds_file_name=DATASET_FILE,
        ds_file_path=dataset_file_path,
    )

    embeddings_arch = call_args.storage_path / "glove.840B.300d.zip"
    emb_file_path = await get_embeddings(emb_arch_path=embeddings_arch)

    # Check if preprocessing could be skipped
    checksum_key = (
        f"{dataset_file_path.name}_{DATASET_SIZE}_{emb_file_path.name}_{call_args.train_size}_{call_args.random_seed}"
    )
    need_rerun = True
    if CHECKSUMS.get(checksum_key, None):
        need_rerun = False
        for f_name, checksum in CHECKSUMS.get(checksum_key).items():
            if not verify_checksum(call_args.work_store_path / f_name, checksum):
                need_rerun = True
                break
    if need_rerun:
        datasets = preprocess_data(dataset_file_path, DATASET_SIZE, emb_file_path, call_args.train_size)
        dump_pds(dump_root=call_args.work_store_path, pds=datasets)
    else:
        logging.info(f"All checksums match run configuration, skipping preprocessing.")


def config_env(seed: int, logging_level: str) -> None:
    # Set PRNG seeds for reproducibility
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

    # Configure logging
    logging.basicConfig(
        level=logging_level.upper(),
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s| %(message)s'
    )

    # Config external libs
    tqdm.pandas()


async def load_dataset(ds_name: str, ds_file_name: str, ds_file_path: Path) -> None:
    checksum = CHECKSUMS.get(ds_file_path.name, "")
    if not file_exists(ds_file_path) or not verify_checksum(ds_file_path, checksum):
        load_cmd_args = f"competitions download -f {ds_file_name} {ds_name} --path {str(ds_file_path.parent)}"
        await run_subproc("kaggle", *load_cmd_args.split(" "))


async def get_embeddings(emb_arch_path: Path) -> Path:
    arch_checksum = CHECKSUMS.get(emb_arch_path.name, "")
    emb_unz_path = emb_arch_path.with_suffix(".txt")
    emb_checksum = CHECKSUMS.get(emb_unz_path.name, "")

    if not file_exists(emb_unz_path) or not verify_checksum(emb_unz_path, emb_checksum):
        if not file_exists(emb_arch_path) or not verify_checksum(emb_arch_path, arch_checksum):
            url = "http://nlp.stanford.edu/data/glove.840B.300d.zip"
            desc = f"Downloading {url.split('/')[-1]}"
            r = requests.get(url, stream=True)
            size_in_bytes = int(r.headers.get('content-length', None))
            chunk_size = 1024
            r.raise_for_status()
            pbar = tqdm(total=size_in_bytes, unit="iB", unit_scale=True, unit_divisor=chunk_size, desc=desc)
            with emb_arch_path.open("wb") as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    pbar.update(fd.write(chunk))
            r.close()
        with zipfile.ZipFile(emb_arch_path, 'r') as zip_ref:
            zip_ref.extract(emb_unz_path.name, path=str(emb_unz_path.parent))
    return emb_unz_path


def preprocess_data(ds_path: Path, ds_size: int, emb_file: Path, train_size: float) -> Mapping[str, pd.DataFrame]:

    full_dataset = pd.read_csv(ds_path,  compression='zip', header=0, sep=',', quotechar='"')
    dataset = full_dataset.loc[:ds_size, [X_COLUMN] + Y_COLUMNS]

    # Cleaning the data
    dataset["comment_text"] = dataset["comment_text"].progress_apply(lambda x: preprocess(x))
    tokenizer = Tokenizer(num_words=TOKENIZER_WORDS, filters='', lower=False)
    tokenizer.fit_on_texts(list(dataset['comment_text']))

    word2vec_glove_file = get_tmpfile("glove.840B.300d.word2vec.txt")
    glove2word2vec(str(emb_file.resolve()), word2vec_glove_file)
    glove_model = KeyedVectors.load_word2vec_format(word2vec_glove_file)

    max_features = min(MAX_FEATURES, len(tokenizer.word_index))
    embedding_matrix, _ = build_matrix(tokenizer.word_index, glove_model, max_features)

    # Split the data into training and validation
    mask = np.random.rand(len(dataset)) < train_size
    train_dataset = dataset[mask]
    test_dataset = dataset[~mask]

    x_train = train_dataset[X_COLUMN]
    y_train = np.where(train_dataset['target'] >= 0.5, 1, 0)
    x_test = test_dataset[X_COLUMN]
    y_test = np.where(test_dataset['target'] >= 0.5, 1, 0)

    y_aux_train = train_dataset[Y_COLUMNS]
    y_aux_test = test_dataset[Y_COLUMNS]

    # word indexing: transform text token into sequence of indexes.
    x_train = tokenizer.texts_to_sequences(x_train)
    x_test = tokenizer.texts_to_sequences(x_test)
    # truncate or pad sequences to have the same length
    x_train = sequence.pad_sequences(x_train, maxlen=SEQUENCE_MAX_LEN)
    x_test = sequence.pad_sequences(x_test, maxlen=SEQUENCE_MAX_LEN)

    output = {
        "x_train.pkl": pd.DataFrame(x_train),
        "x_test.pkl": pd.DataFrame(x_test),
        "y_train.pkl": pd.DataFrame(y_train),
        "y_aux_train.pkl": pd.DataFrame(y_aux_train),
        "y_test.pkl": pd.DataFrame(y_test),
        "y_aux_test.pkl": pd.DataFrame(y_aux_test),
    }
    return output


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Load and prepare dataset.")
    parser.add_argument(
        "-s",
        "--storage_path",
        default=os.environ.get("NOTOX_STORAGE_PATH"),
        type=Path,
        help="Path to the folder, where unprocessed dataset will be stored."
    )
    parser.add_argument(
        "-w",
        "--work_store_path",
        default=os.environ.get("NOTOX_WORK_STORE"),
        type=Path,
        help="Path to the shared folder, where the processed data will be stored."
    )
    parser.add_argument(
        "-d",
        "--dataset_name",
        default=os.environ.get("NOTOX_DATASET_NAME"),
        type=str,
        help="Kaggle dataset name to download."
    )
    parser.add_argument(
        "-r",
        "--random_seed",
        default=os.environ.get("NOTOX_RANDOM_SEED", RANDOM_SEED),
        type=int,
        help="Random seed for reproducibility."
    )
    parser.add_argument(
        "--train_size",
        default=os.environ.get("NOTOX_TRAIN_SIZE", TRAIN_SIZE),
        type=float,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        help="Logging level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )

    args = parser.parse_args()
    if not args.storage_path \
            or not args.work_store_path \
            or not args.dataset_name:
        exit(parser.print_usage())
    return parser.parse_args()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
