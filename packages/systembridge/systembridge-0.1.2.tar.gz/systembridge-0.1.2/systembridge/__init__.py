"""Bridge: Init"""
from aiohttp import ClientResponse
from typing import Any, List

from .client import BridgeClient
from .objects.audio import Audio
from .objects.base import BridgeBase
from .objects.battery import Battery
from .objects.bluetooth import Bluetooth
from .objects.command.payload import CommandPayload
from .objects.command.response import CommandResponse
from .objects.cpu import Cpu
from .objects.filesystem import Filesystem
from .objects.graphics import Graphics
from .objects.information import Information
from .objects.memory import Memory
from .objects.network import Network
from .objects.os import Os
from .objects.processes import Processes
from .objects.system import System

BASE_HEADERS = {"Accept": "application/json"}


class Bridge(BridgeBase):
    """Main class for Bridge."""

    def __init__(self, client: BridgeClient, base_url: str, api_key: str) -> None:
        """Initialize the token manager class."""
        self._client = client
        self._base_url = base_url
        self._api_key = api_key
        self._audio: List[Audio] = []
        self._battery: Battery = {}
        self._bluetooth: Bluetooth = {}
        self._cpu: Cpu = {}
        self._filesystem: Filesystem = {}
        self._graphics: Graphics = {}
        self._information: Information = {}
        self._memory: Memory = {}
        self._os: Os = {}
        self._processes: Processes = {}
        self._system: System = {}

    @property
    def audio(self) -> List[Audio]:
        return self._audio

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def bluetooth(self) -> Bluetooth:
        return self._bluetooth

    @property
    def cpu(self) -> Cpu:
        return self._cpu

    @property
    def filesystem(self) -> Filesystem:
        return self._filesystem

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def information(self) -> Information:
        return self._information

    @property
    def memory(self) -> Memory:
        return self._memory

    @property
    def network(self) -> Network:
        return self._network

    @property
    def os(self) -> Os:
        return self._os

    @property
    def processes(self) -> Processes:
        return self._processes

    @property
    def system(self) -> System:
        return self._system

    async def async_get(self, path: str) -> Any:
        """Generic Getter"""
        response: ClientResponse = await self._client.get(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
        )
        return await response.json()

    async def async_post(self, path: str, payload: Any) -> Any:
        """Generic Getter"""
        response: ClientResponse = await self._client.post(
            f"{self._base_url}{path}",
            headers={**BASE_HEADERS, "api-key": self._api_key},
            json=payload,
        )
        return await response.json()

    async def async_get_audio(self) -> List[Audio]:
        """Get audio information"""
        self._audio = [Audio(audio) for audio in await self.async_get("/audio") or []]
        return self._audio

    async def async_get_battery(self) -> Battery:
        """Get battery information"""
        self._battery = Battery(await self.async_get("/battery"))
        return self._battery

    async def async_get_bluetooth(self) -> Bluetooth:
        """Get bluetooth information"""
        self._bluetooth = Bluetooth(await self.async_get("/bluetooth"))
        return self._bluetooth

    async def async_send_command(self, payload: CommandPayload) -> CommandResponse:
        """Get cpu information"""
        return CommandResponse(await self.async_post("/command", payload))

    async def async_get_cpu(self) -> Cpu:
        """Get cpu information"""
        self._cpu = Cpu(await self.async_get("/cpu"))
        return self._cpu

    async def async_get_filesystem(self) -> Filesystem:
        """Get filesystem information"""
        self._filesystem = Filesystem(await self.async_get("/filesystem"))
        return self._filesystem

    async def async_get_graphics(self) -> Graphics:
        """Get graphics information"""
        self._graphics = Graphics(await self.async_get("/graphics"))
        return self._graphics

    async def async_get_information(self) -> Information:
        """Get information"""
        self._information = Information(await self.async_get("/information"))
        return self._information

    async def async_get_memory(self) -> Memory:
        """Get memory information"""
        self._memory = Memory(await self.async_get("/memory"))
        return self._memory

    async def async_get_network(self) -> Network:
        """Get network information"""
        self._network = Network(await self.async_get("/network"))
        return self._network

    async def async_get_os(self) -> Os:
        """Get os information"""
        self._os = Os(await self.async_get("/os"))
        return self._os

    async def async_get_processes(self) -> Processes:
        """Get processes information"""
        self._processes = Processes(await self.async_get("/processes"))
        return self._processes

    async def async_get_system(self) -> System:
        """Get system information"""
        self._system = System(await self.async_get("/system"))
        return self._system
