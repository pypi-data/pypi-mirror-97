"""
Main interface for workmailmessageflow service type definitions.

Usage::

    ```python
    from mypy_boto3_workmailmessageflow.type_defs import S3ReferenceTypeDef

    data: S3ReferenceTypeDef = {...}
    ```
"""
import sys

from botocore.response import StreamingBody

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = ("S3ReferenceTypeDef", "GetRawMessageContentResponseTypeDef", "RawMessageContentTypeDef")

_RequiredS3ReferenceTypeDef = TypedDict("_RequiredS3ReferenceTypeDef", {"bucket": str, "key": str})
_OptionalS3ReferenceTypeDef = TypedDict(
    "_OptionalS3ReferenceTypeDef", {"objectVersion": str}, total=False
)

class S3ReferenceTypeDef(_RequiredS3ReferenceTypeDef, _OptionalS3ReferenceTypeDef):
    pass

GetRawMessageContentResponseTypeDef = TypedDict(
    "GetRawMessageContentResponseTypeDef", {"messageContent": StreamingBody}
)

RawMessageContentTypeDef = TypedDict(
    "RawMessageContentTypeDef", {"s3Reference": "S3ReferenceTypeDef"}
)
