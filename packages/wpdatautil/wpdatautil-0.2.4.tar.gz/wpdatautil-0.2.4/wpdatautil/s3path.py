"""s3path utilities."""
import shutil
from pathlib import Path
from typing import Union

from s3path import S3Path

AnyPath = Union[Path, S3Path]


def rmdirtree(path: AnyPath) -> None:
    """Remove the local or S3 path."""
    if isinstance(path, S3Path):
        if path.exists():
            path.rmdir()
    else:
        shutil.rmtree(path, ignore_errors=True)
    assert list(path.rglob("*")) == []
