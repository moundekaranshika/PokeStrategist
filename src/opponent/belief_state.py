"""
PokéStrategist - Opponent Belief State
Maintains probability distributions over hidden opponent archetypes,
card holdings, and strategic intent based on observable game actions.
"""

from typing import Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass, field

from src.schema import Card, EnergyType
from src.deck.archetypes import ArchetypeCategory, ARCHETYPE_PROFILES

@dataclass
class OpponentBeliefState:
    archetype_probabilities: Dict[str, float] = field(default_factory=dict)
    known_discarded_cards: List[Card] = field(default_factory=list)
    revealed_cards: List[Card] = field(default_factory=list)
    observed_energy_types: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    estimated_boss_orders_remaining: int = 2
    estimated_iono_remaining: int = 3
    estimated_switch_remaining: int = 2
    estimated_ko_threat_prob: float = 0.2
    total_observations_count: int = 0

    def __post_init__(self):
        if not self.archetype_probabilities:
            # Initialize with uniform prior over archetypes
            uniform_prob = 1.0 / len(ArchetypeCategory)
            self.archetype_probabilities = {
                arch.value: uniform_prob for arch in ArchetypeCategory
            }

    def get_most_likely_archetype(self) -> str:
        return max(self.archetype_probabilities.items(), key=lambda x: x[1])[0]

    def get_archetype_entropy(self) -> float:
        """Calculates Shannon entropy of the belief distribution to measure uncertainty."""
        import math
        entropy = 0.0
        for p in self.archetype_probabilities.values():
            if p > 1e-7:
                entropy -= p * math.log2(p)
        return round(entropy, 3)
