import os
import argparse
from pathlib import Path


def main():
    call_args = get_args()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Load and prepare dataset.")
    parser.add_argument(
        "-s",
        "--storage_path",
        required=True,
        type=Path,
        help="Path to the shared folder, where the dataset will be stored."
    )
    parser.add_argument(
        "-d",
        "--dataset_name",
        required=True,
        type=str,
        help="Kaggle dataset name to download."
    )
    return parser.parse_args()


