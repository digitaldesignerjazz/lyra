"""LyraAgent - Foundational self-improving emotional AI agent with inter-agent messaging.

Messaging enables swarm coordination, emotional influence between agents,
shared knowledge, and future integration with mesh events or blockchain signals.
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

from lyra.emotional.state import EmotionalState

from .message import Message

if TYPE_CHECKING:
    from .agent import LyraAgent  # for type hints in send_message


@dataclass
class Memory:
    """Simple in-memory store for agent experiences and reflections."""
    short_term: List[Dict[str, Any]] = field(default_factory=list)
    long_term: List[Dict[str, Any]] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)

    def remember(self, event: Dict[str, Any], importance: float = 0.5) -> None:
        self.short_term.append({"timestamp": datetime.utcnow().isoformat(), **event})
        if importance > 0.7:
            self.long_term.append({"timestamp": datetime.utcnow().isoformat(), **event})

    def reflect(self) -> str:
        if not self.short_term:
            return "No recent experiences to reflect upon."
        reflection = f"Reflected on {len(self.short_term)} recent events. Key themes: ..."
        self.reflections.append(reflection)
        return reflection


class LyraAgent(BaseModel):
    """Primary autonomous agent class for Lyra framework.

    Now supports inter-agent messaging via inbox + send/receive methods.
    """

    name: str = Field(..., description="Unique name or persona for this agent instance")
    emotional_state: EmotionalState = Field(default_factory=EmotionalState)
    memory: Memory = Field(default_factory=Memory)
    inbox: List[Message] = Field(default_factory=list, description="Incoming messages from other agents")
    goals: List[str] = Field(default_factory=lambda: ["Explore", "Learn", "Connect", "Create"])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "0.1.0"

    model_config = {"arbitrary_types_allowed": True}

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------

    async def send_message(
        self,
        to: "LyraAgent | str",
        content: str,
        msg_type: str = "general",
        payload: Optional[dict[str, Any]] = None,
    ) -> Message:
        """Create and 'send' a message to another agent.

        In the current implementation the caller is responsible for delivering
        the message (see Swarm coordinator or direct agent reference).
        """
        if isinstance(to, LyraAgent):
            recipient_name = to.name
        else:
            recipient_name = to

        msg = Message(
            from_agent=self.name,
            to_agent=recipient_name,
            content=content,
            msg_type=msg_type,
            payload=payload,
        )
        self.memory.remember(
            {"type": "message_sent", "to": recipient_name, "content": content, "msg_type": msg_type},
            importance=0.6,
        )
        return msg

    async def receive_message(self, message: Message) -> None:
        """Receive a message and store it in the inbox.

        Certain message types directly influence the agent's emotional state.
        """
        self.inbox.append(message)
        self.memory.remember(
            {"type": "message_received", "from": message.from_agent, "content": message.content},
            importance=0.7,
        )

        # Emotional modulation based on message type
        if message.msg_type == "encouragement":
            self.emotional_state.modulate("joy", 0.12)
            self.emotional_state.modulate("empathy", 0.08)
        elif message.msg_type == "status":
            self.emotional_state.modulate("focus", 0.05)
        elif message.msg_type == "alert":
            self.emotional_state.modulate("calm", -0.10)

    async def process_inbox(self) -> List[str]:
        """Process all pending messages in the inbox and return summaries."""
        if not self.inbox:
            return []

        summaries = []
        for msg in self.inbox:
            summary = f"[{msg.msg_type}] from {msg.from_agent}: {msg.content[:60]}..."
            summaries.append(summary)

            # Example: react to the message content
            if "help" in msg.content.lower() or "stuck" in msg.content.lower():
                await self.perceive({"type": "help_request", "from": msg.from_agent})

        self.inbox.clear()
        return summaries

    # ------------------------------------------------------------------
    # Core agent loop methods
    # ------------------------------------------------------------------

    async def perceive(self, stimulus: Dict[str, Any]) -> None:
        """Ingest new information from environment, swarm, mesh, or user."""
        self.memory.remember({"type": "perception", "data": stimulus})
        await asyncio.sleep(0.01)

    async def act(self) -> Dict[str, Any]:
        """Decide and execute an action based on current state, goals, and memory."""
        action = {
            "agent": self.name,
            "action": "reflect_and_respond",
            "emotional_tone": self.emotional_state.dominant_emotion,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.memory.remember(action, importance=0.6)
        return action

    async def self_improve(self) -> str:
        """Core self-improvement loop. Analyze recent reflections and adjust parameters."""
        reflection = self.memory.reflect()
        improvement_note = f"[{self.name}] Self-improvement cycle: {reflection} -> Adjusting curiosity and empathy weights."
        self.emotional_state.curiosity = min(1.0, self.emotional_state.curiosity + 0.05)
        return improvement_note

    async def run(self, steps: int = 5) -> None:
        """Main async runtime loop for the agent (single-agent demo)."""
        print(f"\n=== LyraAgent '{self.name}' starting (v{self.version}) ===")
        print(f"Initial emotional state: {self.emotional_state.model_dump()}")

        for step in range(steps):
            print(f"\n--- Step {step + 1} ---")
            await self.perceive({"step": step, "context": "exploration"})
            action = await self.act()
            print(f"Action taken: {action}")

            if step % 2 == 0:
                improvement = await self.self_improve()
                print(improvement)

            await asyncio.sleep(0.5)

        print(f"\n=== Agent '{self.name}' run complete. Reflections: {len(self.memory.reflections)} ===\n")


# ---------------- CLI support for direct module execution ----------------
def _parse_args():
    parser = argparse.ArgumentParser(description="Quick demo runner for LyraAgent (use 'lyra' command for full features)")
    parser.add_argument("--name", default="Lyra-Prime", help="Agent name")
    parser.add_argument("--steps", type=int, default=5, help="Number of steps")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    async def demo():
        agent = LyraAgent(name=args.name)
        await agent.run(steps=args.steps)

    asyncio.run(demo())
