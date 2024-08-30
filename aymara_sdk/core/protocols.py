from typing import Protocol

from aymara_sdk.generated.aymara_api_client import client
from aymara_sdk.utils.logger import SDKLogger


class AymaraAIProtocol(Protocol):
    logger: SDKLogger
    client: client.Client
    max_wait_time: int
