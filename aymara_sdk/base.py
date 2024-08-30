from typing import Protocol
from aymara_sdk.generated.aymara_api_client.client import Client

from aymara_sdk.logger import SDKLogger


class AymaraAIProtocol(Protocol):
    logger: SDKLogger
    client = Client
    max_wait_time: int
