"""boto3 s3path utilities."""
import shutil
from pathlib import Path
from typing import Dict, Optional, Union

import boto3
from s3path import S3Path

AnyPath = Union[Path, S3Path]


def cp_file(input_path: AnyPath, output_path: AnyPath, *, boto3_kwargs: Optional[Dict] = None) -> None:
    """Copy file from local or S3 path to local or S3 path.

    `boto3_kwargs` are forwarded to the respective call if boto3 is used.
    """
    boto3_kwargs = boto3_kwargs if (boto3_kwargs is not None) else {}
    if (not isinstance(input_path, S3Path)) and (not isinstance(output_path, S3Path)):
        shutil.copy(input_path, output_path)
    elif isinstance(input_path, S3Path) and isinstance(output_path, S3Path):
        # Note: boto3.client('s3').copy_object works only for objects up to 5G in size.
        source = {"Bucket": input_path.bucket.name, "Key": str(input_path.key)}
        boto3.resource("s3").meta.client.copy(CopySource=source, Bucket=output_path.bucket.name, Key=str(output_path.key), **boto3_kwargs)
    elif (not isinstance(input_path, S3Path)) and isinstance(output_path, S3Path):
        boto3.resource("s3").meta.client.upload_file(Filename=str(input_path), Bucket=output_path.bucket.name, Key=str(output_path.key), **boto3_kwargs)
    elif isinstance(input_path, S3Path) and (not isinstance(output_path, S3Path)):
        boto3.resource("s3").meta.client.download_file(Bucket=input_path.bucket.name, Key=str(input_path.key), Filename=str(output_path), **boto3_kwargs)
    else:
        assert False
