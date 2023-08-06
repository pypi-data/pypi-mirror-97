"""pypolars smart_open utilities."""
import logging
from pathlib import Path
from typing import Any

import pypolars as pl
import smart_open

from wpdatautil.pathlib import path_to_uri
from wpdatautil.timeit import Timer

log = logging.getLogger(__name__)


def read_parquet_path(path: Path, *, df_description: str = "dataframe", **kwargs: Any) -> pl.DataFrame:
    """Return a dataframe read from the given path using `smart_open`.

    :param path: This must be a `pathlib` or `s3path` path.
    :param df_description: Optional description of dataframe.
    :param kwargs: These are forwarded to `pl.read_parquet`.
    """
    uri = path_to_uri(path)
    timer = Timer()
    read_description = f"{df_description} from {uri} using smart-open"
    log.debug(f"Reading {read_description}.")
    try:
        with smart_open.open(uri, "rb") as input_file:
            df = pl.read_parquet(input_file, **kwargs)
    except Exception as exception:  # pylint: disable=broad-except
        log.info(f"Error reading {read_description}: {exception.__class__.__qualname__}: {exception}")
        raise
    log.info(f"Read {read_description} returning {len(df):,} rows in {timer}.")
    return df
