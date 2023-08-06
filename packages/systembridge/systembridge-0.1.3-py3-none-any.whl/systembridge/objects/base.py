"""Bridge: Base"""
import logging


class BridgeBase:
    """Base class for Bridge."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class BridgeBaseClient(BridgeBase):
    """Base class for Bridge."""

    def __init__(self, client: "BridgeClient", attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client
