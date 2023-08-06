"""
Main interface for workmailmessageflow service client

Usage::

    ```python
    import boto3
    from mypy_boto3_workmailmessageflow import WorkMailMessageFlowClient

    client: WorkMailMessageFlowClient = boto3.client("workmailmessageflow")
    ```
"""
from typing import Any, Dict, Type

from botocore.client import ClientMeta

from mypy_boto3_workmailmessageflow.type_defs import (
    GetRawMessageContentResponseTypeDef,
    RawMessageContentTypeDef,
)

__all__ = ("WorkMailMessageFlowClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidContentLocation: Type[BotocoreClientError]
    MessageFrozen: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class WorkMailMessageFlowClient:
    """
    [WorkMailMessageFlow.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.can_paginate)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.generate_presigned_url)
        """
    def get_raw_message_content(self, messageId: str) -> GetRawMessageContentResponseTypeDef:
        """
        [Client.get_raw_message_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.get_raw_message_content)
        """
    def put_raw_message_content(
        self, messageId: str, content: RawMessageContentTypeDef
    ) -> Dict[str, Any]:
        """
        [Client.put_raw_message_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.put_raw_message_content)
        """
