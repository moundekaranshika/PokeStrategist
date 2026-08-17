"""
PokéStrategist - Strategic Memory (Long-Term Cross-Game Knowledge)
Tracks cumulative statistics across games, matchup winrates,
opponent archetype frequencies, and calibration of strategic predictions.
"""

from typing import Dict, List, Any
from collections import defaultdict

class StrategicMemory:
    def __init__(self):
        # Matchup stats: (own_archetype, opp_archetype) -> {"wins": int, "losses": int, "games": int}
        self.matchup_matrix: Dict[str, Dict[str, int]] = defaultdict(lambda: {"wins": 0, "losses": 0, "games": 0})
        self.archetype_observations_history: Dict[str, int] = defaultdict(int)
        self.total_games_played: int = 0
        self.total_wins: int = 0

    def record_game_result(self, own_archetype: str, opp_archetype: str, won: bool):
        self.total_games_played += 1
        if won:
            self.total_wins += 1

        matchup_key = f"{own_archetype} vs {opp_archetype}"
        stats = self.matchup_matrix[matchup_key]
        stats["games"] += 1
        if won:
            stats["wins"] += 1
        else:
            stats["losses"] += 1

        self.archetype_observations_history[opp_archetype] += 1

    def get_matchup_winrate(self, own_archetype: str, opp_archetype: str) -> float:
        matchup_key = f"{own_archetype} vs {opp_archetype}"
        stats = self.matchup_matrix.get(matchup_key)
        if not stats or stats["games"] == 0:
            return 0.50 # Neutral uninformative prior
        return round(stats["wins"] / stats["games"], 3)

    def get_overall_winrate(self) -> float:
        if self.total_games_played == 0:
            return 0.0
        return round(self.total_wins / self.total_games_played, 3)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_games": self.total_games_played,
            "overall_winrate": self.get_overall_winrate(),
            "archetype_frequencies": dict(self.archetype_observations_history),
            "matchups": dict(self.matchup_matrix)
        }
