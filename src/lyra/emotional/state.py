"""EmotionalState - Pydantic model for agent emotional configuration and dynamics.

Designed to be extensible for complex affective computing,
self-regulation, and integration with memory + decision systems.
"""

from pydantic import BaseModel, Field


class EmotionalState(BaseModel):
    """Represents the current emotional configuration of a Lyra agent.

    Emotions are modeled as continuous values [0.0, 1.0] for flexibility.
    Future extensions: valence/arousal, emotion vectors, decay functions,
    influence on reasoning weights, and persistent mood.
    """

    joy: float = Field(0.6, ge=0.0, le=1.0, description="Happiness / positive affect")
    curiosity: float = Field(0.75, ge=0.0, le=1.0, description="Drive to explore and learn")
    empathy: float = Field(0.7, ge=0.0, le=1.0, description="Attunement to others / swarm members")
    focus: float = Field(0.65, ge=0.0, le=1.0, description="Concentration and task persistence")
    calm: float = Field(0.8, ge=0.0, le=1.0, description="Emotional regulation / low reactivity")

    @property
    def dominant_emotion(self) -> str:
        """Return the emotion with the highest current value."""
        emotions = {
            "joy": self.joy,
            "curiosity": self.curiosity,
            "empathy": self.empathy,
            "focus": self.focus,
            "calm": self.calm,
        }
        return max(emotions, key=emotions.get)

    def modulate(self, emotion: str, delta: float) -> None:
        """Adjust a specific emotion by delta (clamped to [0,1])."""
        if hasattr(self, emotion):
            current = getattr(self, emotion)
            new_val = max(0.0, min(1.0, current + delta))
            setattr(self, emotion, new_val)

    def reset_to_baseline(self) -> None:
        """Return to a neutral, curious, calm baseline."""
        self.joy = 0.6
        self.curiosity = 0.75
        self.empathy = 0.7
        self.focus = 0.65
        self.calm = 0.8

    def model_dump(self, **kwargs) -> dict:
        """Return dict representation (Pydantic v2 compatible)."""
        return super().model_dump(**kwargs)
