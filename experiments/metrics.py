"""
PokéStrategist - Experimental Metrics & Analytics Engine
Calculates research-grade evaluation metrics across multi-agent tournaments and ablation trials.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class MatchResult:
    winner: int # 0: Agent 0, 1: Agent 1, -1: Draw
    turns_taken: int
    p0_prizes_left: int
    p1_prizes_left: int
    p0_total_damage: int
    p1_total_damage: int
    p0_actions_count: int
    execution_time_sec: float

@dataclass
class AgentExperimentMetrics:
    agent_name: str
    total_matches: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    win_rate: float = 0.0
    avg_game_length_turns: float = 0.0
    avg_prize_differential: float = 0.0
    avg_damage_dealt: float = 0.0
    avg_decision_time_sec: float = 0.0

    def compute(self, results: List[MatchResult], is_player_0: bool = True):
        self.total_matches = len(results)
        if self.total_matches == 0:
            return

        self.wins = sum(1 for r in results if (r.winner == 0 if is_player_0 else r.winner == 1))
        self.losses = sum(1 for r in results if (r.winner == 1 if is_player_0 else r.winner == 0))
        self.draws = sum(1 for r in results if r.winner == -1)

        self.win_rate = round(self.wins / self.total_matches, 3)
        self.avg_game_length_turns = round(sum(r.turns_taken for r in results) / self.total_matches, 2)
        
        # Prize differential: positive means took more prizes than opponent
        prize_diffs = [
            (r.p1_prizes_left - r.p0_prizes_left) if is_player_0 else (r.p0_prizes_left - r.p1_prizes_left)
            for r in results
        ]
        self.avg_prize_differential = round(sum(prize_diffs) / self.total_matches, 2)

        damages = [r.p0_total_damage if is_player_0 else r.p1_total_damage for r in results]
        self.avg_damage_dealt = round(sum(damages) / self.total_matches, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "matches": self.total_matches,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "win_rate": self.win_rate,
            "avg_game_length_turns": self.avg_game_length_turns,
            "avg_prize_differential": self.avg_prize_differential,
            "avg_damage_dealt": self.avg_damage_dealt
        }
