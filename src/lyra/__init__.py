"""Lyra - Self-improving emotional AI agent framework.

Core package for autonomous agents, swarms, mesh integration,
blockchain primitives, and creative/immersive AI experiences.
"""

__version__ = "0.1.0"
__author__ = "Sven Norman Esslinger"

from .core.agent import LyraAgent

from .emotional.state import EmotionalState

__all__ = ["LyraAgent", "EmotionalState", "__version__"]
