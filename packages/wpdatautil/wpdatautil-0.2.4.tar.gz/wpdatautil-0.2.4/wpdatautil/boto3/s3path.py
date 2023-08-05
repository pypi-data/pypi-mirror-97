"""boto3 s3path utilities."""
import shutil
from pathlib import Path
from typing import Union

import boto3
from s3path import S3Path

AnyPath = Union[Path, S3Path]


def cp_file(input_path: AnyPath, output_path: AnyPath) -> None:
    """Copy file from local or S3 path to local or S3 path."""
    if (not isinstance(input_path, S3Path)) and (not isinstance(output_path, S3Path)):
        shutil.copy(input_path, output_path)
    elif isinstance(input_path, S3Path) and isinstance(output_path, S3Path):
        # Note: boto3.client('s3').copy_object works only for objects up to 5G in size.
        boto3.resource("s3").meta.client.copy(CopySource={"Bucket": input_path.bucket.name, "Key": str(input_path.key)}, Bucket=output_path.bucket.name, Key=str(output_path.key))
    elif (not isinstance(input_path, S3Path)) and isinstance(output_path, S3Path):
        boto3.resource("s3").meta.client.upload_file(Filename=str(input_path), Bucket=output_path.bucket.name, Key=str(output_path.key))
    elif isinstance(input_path, S3Path) and (not isinstance(output_path, S3Path)):
        boto3.resource("s3").meta.client.download_file(Bucket=input_path.bucket.name, Key=str(input_path.key), Filename=str(output_path))
    else:
        assert False
