"""
Class object for OpenPayload
Documentation: https://system-bridge.timmo.dev
"""
from ..base import BridgeBase


class OpenPayload(BridgeBase):
    @property
    def path(self) -> str:
        return self.attributes.get("path", "")
