"""Message model for inter-agent communication in Lyra.

Messages are the foundation for swarm coordination, emotional influence,
shared knowledge, and future mesh/blockchain event propagation.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Structured message passed between Lyra agents.

    Attributes:
        from_agent: Name of the sending agent
        to_agent: Name of the recipient (or "broadcast" / "swarm")
        content: Human-readable message content
        msg_type: Category (general, status, encouragement, task, emotional, alert, ...)
        timestamp: When the message was created
        payload: Optional structured data (dict)
    """

    from_agent: str = Field(..., description="Name of the sending agent")
    to_agent: str = Field(..., description="Recipient name, 'broadcast', or 'swarm'")
    content: str = Field(..., min_length=1, description="Message body")
    msg_type: str = Field("general", description="Type of message (general, status, encouragement, task, ...)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Optional[dict[str, Any]] = Field(default=None, description="Optional structured data")

    def __str__(self) -> str:
        return (
            f"[{self.msg_type.upper()}] {self.from_agent} → {self.to_agent}: {self.content}"
        )

    model_config = {
        "json_encoders": {datetime: lambda v: v.isoformat()}
    }
