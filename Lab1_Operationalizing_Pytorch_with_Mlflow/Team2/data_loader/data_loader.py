import os
import logging
import asyncio
import argparse
import random
from pathlib import Path
from typing import Optional, List

import pandas as pd
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from nltk.tokenize.treebank import TreebankWordTokenizer
from keras.preprocessing.text import Tokenizer
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

from config import (
    DATASET_FILE,
    DATASET_SIZE,
    COLUMNS_TO_USE,
    SYMBOLS_TO_DELETE,
    SYMBOLS_TO_ISOLATE,
    TOKENIZER_WORDS,
)


def main():
    call_args = get_args()
    config_env(call_args.random_seed)
    loop = asyncio.get_event_loop()

    # Kaggle stores compressed files with ".zip" suffix
    dataset_file_path = call_args.storage_path / (DATASET_FILE + ".zip")
    loop.run_until_complete(
        load_ds_if_needed(
            call_args.dataset_name, DATASET_FILE, dataset_file_path
        )
    )
    embeddings_file = call_args.storage_path / "glove.840B.300d.zip"
    loop.run_until_complete(load_embeddings_if_needed(embeddings_file))

    preprocess_data(dataset_file_path, DATASET_SIZE, embeddings_file)


def preprocess_data(ds_path: Path, ds_size: int, emb_file: Path) -> pd.DataFrame:
    full_dataset = pd.read_csv(ds_path,  compression='zip', header=0, sep=',', quotechar='"')
    dataset = full_dataset.loc[:ds_size, COLUMNS_TO_USE]

    # Cleaning the data
    remove_dict = {ord(c): f'' for c in SYMBOLS_TO_DELETE}
    isolate_dict = {ord(c): f' {c} ' for c in SYMBOLS_TO_ISOLATE}
    treebank_tokenizer = TreebankWordTokenizer()

    def handle_symbols(x):
        x = x.translate(remove_dict)
        x = x.translate(isolate_dict)
        return x

    def handle_contractions(x):
        x = treebank_tokenizer.tokenize(x)
        return x

    def fix_quote(x):
        x = [x_[1:] if x_.startswith("'") else x_ for x_ in x]
        x = ' '.join(x)
        return x

    def preprocess(x):
        # 1. Remove all symbols in the corpus that do not appear in the embeddings.
        x = handle_symbols(x)
        # 2. Handle contractions using the TreebankTokenizer.
        x = handle_contractions(x)
        # 3. Remove the apostrophe symbol at the beginning of the token words.
        x = fix_quote(x)
        return x

    dataset["comment_text"] = dataset["comment_text"].progress_apply(lambda x: preprocess(x))
    tokenizer = Tokenizer(num_words=TOKENIZER_WORDS, filters='', lower=False)
    tokenizer.fit_on_texts(list(dataset['comment_text']))

    glove_file = datapath(str(emb_file))
    word2vec_glove_file = get_tmpfile("glove.840B.300d.word2vec.txt")
    glove2word2vec(glove_file, word2vec_glove_file)
    glove_model = KeyedVectors.load_word2vec_format(word2vec_glove_file)


async def load_ds_if_needed(ds_name: str, ds_file_name: str, ds_file_path: Path) -> None:
    if not file_exists(ds_file_path):
        load_cmd_args = f"competitions download -f {ds_file_name} {ds_name} --path {str(ds_file_path.parent)}"
        await _run_subproc("kaggle", *load_cmd_args.split(" "))


async def load_embeddings_if_needed(emb_file_path: Path) -> Path:
    if not file_exists(emb_file_path):
        load_cmd_args = f"http://nlp.stanford.edu/data/glove.840B.300d.zip -O {str(emb_file_path)}"
        await _run_subproc("wget", *load_cmd_args.split(" "))

    unzipped_emb_path = emb_file_path.with_suffix(".txt")
    if not file_exists(unzipped_emb_path):
        unzip_args = f"-d {unzipped_emb_path}"
        await _run_subproc("unzip", *unzip_args.split(" "))
    return unzipped_emb_path


def file_exists(file_path: Path) -> bool:
    if file_path.exists():
        if not file_path.is_file():
            raise ValueError(f"{str(file_path)} already exists, but it is not a file.")
        else:
            logging.info(f"{str(file_path)} already exists, skipping download.")
            return True
    else:
        return False


async def _run_subproc(exe: str, *args: str) -> None:
    subproc = await asyncio.create_subprocess_exec(exe, *args)
    try:
        return_code = await subproc.wait()
        if return_code != 0:
            raise SystemExit(return_code)
    finally:
        if subproc.returncode is None:
            # Kill process if not finished
            # (e.g. if KeyboardInterrupt or cancellation was received)
            subproc.kill()
            await subproc.wait()


def config_env(seed: int) -> None:
    # Set PRNG seeds for reproducibility
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s| %(message)s'
    )

    # Config external libs
    tqdm.pandas()


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
        default=os.environ.get("NOTOX_RANDOM_SEED"),
        type=int,
        help="Random seed for reproducibility."
    )

    args = parser.parse_args()
    if not args.storage_path \
            or not args.work_store_path \
            or not args.dataset_name \
            or not args.random_seed:
        exit(parser.print_usage())
    return parser.parse_args()


if __name__ == "__main__":
    main()
