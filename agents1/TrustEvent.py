from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TrustEvent:
    """
    Represents an event that affects trust beliefs.
    Tracks actions related to trust, such as searching, finding victims,
    and rescuing them, as well as detecting lies.
    """

    event_type: str  # Type of event (Search, Found, Collect, Lie Detected, etc.)

    time: int  # The tick count when the event occurred

    agent: str  # The agent involved in the event

    target: int | None = None  # The target of the action (room, victim, etc.)

    achievedTime: int | None = None  # The tick count when the event was achieved

