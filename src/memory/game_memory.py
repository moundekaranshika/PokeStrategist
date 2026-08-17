"""
PokéStrategist - Game Memory (Short-Term & Turn History)
Records intra-game chronological events, prize milestones, and state deltas.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class TurnEvent:
    turn_number: int
    player_index: int
    action_type: str
    description: str
    prizes_before: int
    prizes_after: int
    damage_dealt: int = 0
    energy_attached: bool = False
    supporter_used: Optional[str] = None

class GameMemory:
    def __init__(self):
        self.events: List[TurnEvent] = []
        self.turn_count: int = 1
        self.own_prizes_taken: int = 0
        self.opp_prizes_taken: int = 0
        self.cards_played_by_self: List[str] = []
        self.cards_played_by_opp: List[str] = []

    def record_turn_event(self, event: TurnEvent):
        self.events.append(event)
        if event.player_index == 0:
            prizes_delta = event.prizes_before - event.prizes_after
            if prizes_delta > 0:
                self.own_prizes_taken += prizes_delta
        else:
            prizes_delta = event.prizes_before - event.prizes_after
            if prizes_delta > 0:
                self.opp_prizes_taken += prizes_delta

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_turns": self.turn_count,
            "total_events": len(self.events),
            "own_prizes_taken": self.own_prizes_taken,
            "opp_prizes_taken": self.opp_prizes_taken,
            "recent_actions": [e.description for e in self.events[-5:]]
        }
