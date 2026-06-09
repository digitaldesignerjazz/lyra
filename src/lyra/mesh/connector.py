"""Mesh integration layer for Lyra agents.

Provides a pluggable abstraction over decentralized networking transports
(Yggdrasil, NovaNet/QNET, future libp2p, etc.). Agents can perceive
mesh events, discover peers, and exchange messages in a transport-agnostic way.

This enables Lyra swarms to operate resiliently across private mesh networks
while maintaining emotional and self-improving behaviors.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field


class MeshConfig(BaseModel):
    """Configuration for mesh connectors."""
    enabled: bool = Field(True, description="Enable mesh connectivity")
    transport: str = Field(
        "yggdrasil",
        description="Transport backend: 'yggdrasil', 'novanet', 'simulated'",
    )
    yggdrasil_api_url: str = Field(
        "http://localhost:9001",
        description="Yggdrasil local HTTP API endpoint (if using yggdrasil transport)",
    )
    node_name: str = Field("lyra-node", description="Human-readable name for this node on the mesh")
    # Future fields: encryption keys, discovery interval, max peers, qnet settings, etc.


class MeshEvent(BaseModel):
    """Standardized event received from the mesh network."""
    event_type: str = Field(..., description="Type of event (peer_joined, message, discovery, etc.)")
    source_peer: str = Field(..., description="Origin peer identifier (Yggdrasil address or alias)")
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(..., description="Unix timestamp of the event")


class MeshConnector(ABC):
    """Abstract base class for all mesh transport implementations.

    Implementations should be async-friendly and support:
    - Connection lifecycle
    - Peer discovery
    - Bidirectional messaging
    - Event emission to registered handlers (so agents can perceive mesh activity)
    """

    def __init__(self, config: MeshConfig):
        self.config = config
        self._running: bool = False
        self._event_handlers: List[Callable[[MeshEvent], asyncio.Future | None]] = []

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the mesh network. Return True on success."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Gracefully shut down the connection."""
        ...

    @abstractmethod
    async def send(self, target_peer: str, data: Dict[str, Any]) -> bool:
        """Send arbitrary data to a specific peer on the mesh."""
        ...

    @abstractmethod
    async def get_peers(self) -> List[str]:
        """Return list of currently known/connected peer identifiers."""
        ...

    def register_event_handler(self, handler: Callable[[MeshEvent], Any]) -> None:
        """Register a callback that will be called for every incoming MeshEvent."""
        self._event_handlers.append(handler)

    async def _emit_event(self, event: MeshEvent) -> None:
        """Internal: deliver event to all registered handlers (used by concrete impls)."""
        for handler in self._event_handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as exc:
                logger.error(f"Mesh event handler failed: {exc}")


class SimulatedMeshConnector(MeshConnector):
    """Pure in-memory simulated mesh for testing, demos, and CI.

    Useful for developing agent behavior without a real mesh node running.
    Supports injecting synthetic events for testing emotional/messaging responses.
    """

    def __init__(self, config: MeshConfig):
        super().__init__(config)
        self._known_peers: List[str] = ["peer-alpha", "peer-beta", "lyra-self"]
        self._inbox: asyncio.Queue[MeshEvent] = asyncio.Queue()

    async def connect(self) -> bool:
        logger.info("[SimMesh] Simulated mesh connector activated.")
        self._running = True
        return True

    async def disconnect(self) -> None:
        self._running = False
        logger.info("[SimMesh] Disconnected.")

    async def send(self, target_peer: str, data: Dict[str, Any]) -> bool:
        if not self._running:
            logger.warning("[SimMesh] Cannot send — not connected.")
            return False
        logger.debug(f"[SimMesh] -> {target_peer}: {data}")
        # In a real impl this would serialize and transmit
        return True

    async def get_peers(self) -> List[str]:
        return self._known_peers.copy()

    async def inject_event(self, event: MeshEvent) -> None:
        """Test helper: inject a synthetic mesh event (e.g. from another node)."""
        await self._emit_event(event)


class YggdrasilConnector(MeshConnector):
    """Stub implementation targeting a local Yggdrasil node.

    Real implementation will use Yggdrasil's local HTTP API (port 9001 by default)
    or the admin socket for:
    - getSelf / getPeers
    - Sending data via the Yggdrasil TUN interface or API
    - Subscribing to peer/connection events

    See: https://yggdrasil-network.github.io/configuration.html#api
    """

    def __init__(self, config: MeshConfig):
        super().__init__(config)
        self._client = None  # Will be httpx.AsyncClient in full impl

    async def connect(self) -> bool:
        logger.info(f"[Yggdrasil] Connecting to local node at {self.config.yggdrasil_api_url}...")
        # TODO: Perform health check (GET /api/getSelf or similar)
        # TODO: Initialize httpx.AsyncClient with base_url
        self._running = True
        logger.warning(
            "[Yggdrasil] This is a stub. Full Yggdrasil integration (peer discovery, "
            "message passing, event subscription) is planned for the next milestone."
        )
        return True

    async def disconnect(self) -> None:
        self._running = False
        logger.info("[Yggdrasil] Disconnected (stub).")

    async def send(self, target_peer: str, data: Dict[str, Any]) -> bool:
        if not self._running:
            return False
        logger.info(f"[Yggdrasil] STUB: Would send message to peer {target_peer} (payload size={len(str(data))})")
        # TODO: Use Yggdrasil API or TUN interface to deliver data
        return True

    async def get_peers(self) -> List[str]:
        if not self._running:
            return []
        logger.info("[Yggdrasil] STUB: Returning simulated peer list.")
        return ["ygg-peer-0001 (stub)", "ygg-peer-0002 (stub)"]


def get_mesh_connector(config: Optional[MeshConfig] = None) -> MeshConnector:
    """Factory function to obtain a configured mesh connector."""
    cfg = config or MeshConfig()
    if not cfg.enabled:
        logger.info("Mesh connectivity disabled in config.")
        # Return a no-op connector or raise depending on desired strictness
        return SimulatedMeshConnector(cfg)

    if cfg.transport == "simulated":
        return SimulatedMeshConnector(cfg)
    elif cfg.transport == "yggdrasil":
        return YggdrasilConnector(cfg)
    elif cfg.transport == "novanet":
        # Placeholder for future NovaNet/QNET integration
        logger.warning("NovaNet transport selected — falling back to simulated for now.")
        return SimulatedMeshConnector(cfg)
    else:
        raise ValueError(f"Unsupported mesh transport: {cfg.transport}")
