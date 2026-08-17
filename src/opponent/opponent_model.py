"""
PokéStrategist - Opponent Modeling Engine
Applies Bayesian updates to the OpponentBeliefState upon observing
actions, cards played, energy attachments, searches, and attacks.
"""

from typing import Dict, List, Optional
from src.schema import Card, Action, ActionType, EnergyType
from src.opponent.belief_state import OpponentBeliefState
from src.deck.archetypes import ArchetypeCategory, ARCHETYPE_PROFILES

class OpponentModel:
    def __init__(self):
        self.belief = OpponentBeliefState()

    def reset(self):
        self.belief = OpponentBeliefState()

    def observe_card_revealed(self, card: Card):
        """Alias for observe_card_played."""
        self.observe_card_played(card)

    def observe_card_played(self, card: Card):
        """Bayesian update on observing a card played from the opponent's hand."""
        self.belief.total_observations_count += 1
        name = card.name.lower()

        # Update specific card counters
        if "boss" in name:
            self.belief.estimated_boss_orders_remaining = max(0, self.belief.estimated_boss_orders_remaining - 1)
        elif "iono" in name or "judge" in name:
            self.belief.estimated_iono_remaining = max(0, self.belief.estimated_iono_remaining - 1)
        elif "switch" in name or "rope" in name or "prime catcher" in name:
            self.belief.estimated_switch_remaining = max(0, self.belief.estimated_switch_remaining - 1)

        # Compute likelihoods P(card | Archetype)
        likelihoods = {}
        for arch in ArchetypeCategory:
            profile = ARCHETYPE_PROFILES[arch]
            lh = 1.0

            # Match indicators
            if any(ind.lower() in name for ind in profile.key_indicators):
                lh *= 3.5

            if card.is_pokemon:
                if arch == ArchetypeCategory.SETUP_EVOLUTION and card.stage.value in ["Stage 1", "Stage 2"]:
                    lh *= 2.8
                elif arch == ArchetypeCategory.AGGRESSIVE and card.stage.value == "Basic" and (card.features and card.features.is_rule_box):
                    lh *= 2.5
                elif arch == ArchetypeCategory.DEFENSIVE and card.hp >= 160:
                    lh *= 2.0

            if card.is_trainer:
                if arch == ArchetypeCategory.CONTROL_DISRUPTION and any(k in name for k in ["iono", "judge", "path", "devolution"]):
                    lh *= 3.0
                elif arch == ArchetypeCategory.ENERGY_ACCELERATION and any(k in name for k in ["patch", "retrieval", "vessel"]):
                    lh *= 2.5

            likelihoods[arch.value] = lh

        self._bayesian_update(likelihoods)

    def observe_energy_attached(self, energy_type: EnergyType, target_name: str):
        """Bayesian update when opponent attaches an energy."""
        self.belief.observed_energy_types[energy_type.value] += 1
        self.belief.total_observations_count += 1

        likelihoods = {}
        for arch in ArchetypeCategory:
            # Energy attachment increases threat probability
            likelihoods[arch.value] = 1.2
        self.belief.estimated_ko_threat_prob = min(0.95, self.belief.estimated_ko_threat_prob + 0.15)
        self._bayesian_update(likelihoods)

    def observe_attack(self, attack_name: str, damage_dealt: int):
        """Bayesian update when opponent executes an attack."""
        likelihoods = {}
        for arch in ArchetypeCategory:
            if damage_dealt >= 200:
                likelihoods[arch.value] = 2.5 if arch in [ArchetypeCategory.SINGLE_TARGET_BURST, ArchetypeCategory.AGGRESSIVE] else 0.8
            elif damage_dealt <= 50:
                likelihoods[arch.value] = 2.0 if arch in [ArchetypeCategory.CONTROL_DISRUPTION, ArchetypeCategory.SPREAD_SNIPER] else 0.9
            else:
                likelihoods[arch.value] = 1.0
        self._bayesian_update(likelihoods)

    def update_from_visible_state(
        self,
        hand_size: int,
        bench_size: int,
        active_energy_count: int,
        prizes_remaining: int,
        turn: int
    ):
        """Updates threat estimation based on visible board metrics."""
        threat = 0.2
        threat += min(0.4, active_energy_count * 0.12)
        threat += min(0.2, bench_size * 0.05)
        threat += min(0.2, (7 - prizes_remaining) * 0.05)
        if hand_size >= 5:
            threat += 0.1
        self.belief.estimated_ko_threat_prob = min(0.98, round(threat, 2))

    def _bayesian_update(self, likelihoods: Dict[str, float]):
        """Standard Bayes Rule: P(A|x) = P(x|A) * P(A) / sum(P(x|A') * P(A'))"""
        new_probs = {}
        total_evidence = 0.0

        for arch_name, prior in self.belief.archetype_probabilities.items():
            lh = likelihoods.get(arch_name, 1.0)
            posterior = prior * lh
            new_probs[arch_name] = posterior
            total_evidence += posterior

        if total_evidence > 0:
            for arch_name in new_probs:
                # Add Dirichlet / Laplace smoothing (alpha=0.01) to prevent zeroing out
                smoothed = (new_probs[arch_name] / total_evidence) + 0.005
                new_probs[arch_name] = smoothed
            
            # Re-normalize
            total_smoothed = sum(new_probs.values())
            for arch_name in new_probs:
                self.belief.archetype_probabilities[arch_name] = round(new_probs[arch_name] / total_smoothed, 4)
