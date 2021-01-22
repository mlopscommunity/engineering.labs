import logging
import hashlib
import asyncio
from pathlib import Path
from typing import Mapping

import pandas as pd


def file_exists(file_path: Path) -> bool:
    if file_path.exists():
        if not file_path.is_file():
            raise ValueError(f"{str(file_path)} already exists, but it is not a file.")
        else:
            logging.info(f"{str(file_path)} already exists, skipping download.")
            return True
    else:
        return False


def verify_checksum(file_path: Path, checksum: str) -> bool:
    logging.info(f"Checking hash for {str(file_path)}, should be {checksum}")
    hasher = hashlib.new("sha256")
    buffer = bytearray(16 * 1024 * 1024)  # 16 MB
    view = memoryview(buffer)
    with file_path.open("rb", buffering=0) as stream:
        read = stream.readinto(buffer)
        while read:
            hasher.update(view[:read])
            read = stream.readinto(buffer)
    got_checksum = hasher.hexdigest()
    logging.info(f"Got {got_checksum} " + "(match!)" if got_checksum == checksum else "(don't match!)")
    return got_checksum == checksum


async def run_subproc(exe: str, *args: str) -> None:
    logging.info(f"Running '{exe} {' '.join(args)}'")
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


def dump_pds(dump_root: Path, pds: Mapping[str, pd.DataFrame]) -> None:
    if dump_root.exists():
        if not dump_root.is_dir():
            raise ValueError(f"{dump_root} is not a directory.")
    else:
        dump_root.mkdir(parents=True, exist_ok=True)
    for df_name, df in pds.items():
        df_file_path = dump_root / df_name
        logging.info(f"Saving {df_name} as {str(df_file_path)}")
        df.to_pickle(str(df_file_path))
