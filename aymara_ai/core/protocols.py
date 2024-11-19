from typing import Protocol

from aymara_ai.generated.aymara_api_client import client
from aymara_ai.utils.logger import SDKLogger


class AymaraAIProtocol(Protocol):
    logger: SDKLogger
    client: client.Client
