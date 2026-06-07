"""LyraAgent - Foundational self-improving emotional AI agent.

This module provides the core agent class with:
- Persistent memory (short + long term)
- Emotional state modeling
- Self-reflection and improvement loops
- Async task execution
- Extensibility for swarm, mesh, and chain integration
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from lyra.emotional.state import EmotionalState


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

    Attributes:
        name: Agent identifier / persona name
        emotional_state: Current emotional configuration
        memory: Experience and reflection store
        goals: High-level objectives driving behavior
        created_at: Timestamp of instantiation
    """

    name: str = Field(..., description="Unique name or persona for this agent instance")
    emotional_state: EmotionalState = Field(default_factory=EmotionalState)
    memory: Memory = Field(default_factory=Memory)
    goals: List[str] = Field(default_factory=lambda: ["Explore", "Learn", "Connect", "Create"])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "0.1.0"

    model_config = {"arbitrary_types_allowed": True}

    async def perceive(self, stimulus: Dict[str, Any]) -> None:
        """Ingest new information from environment, swarm, mesh, or user."""
        self.memory.remember({"type": "perception", "data": stimulus})
        # Future: trigger emotional response, update state
        await asyncio.sleep(0.01)  # Yield control

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
        # Placeholder for real learning / weight updates / new skills
        self.emotional_state.curiosity = min(1.0, self.emotional_state.curiosity + 0.05)
        return improvement_note

    async def run(self, steps: int = 5) -> None:
        """Main async runtime loop for the agent."""
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

            await asyncio.sleep(0.5)  # Simulate thinking / pacing

        print(f"\n=== Agent '{self.name}' run complete. Reflections: {len(self.memory.reflections)} ===\n")


if __name__ == "__main__":
    async def demo():
        agent = LyraAgent(name="Lyra-Prime")
        await agent.run(steps=4)

    asyncio.run(demo())
