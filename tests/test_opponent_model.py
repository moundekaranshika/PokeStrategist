"""
Unit Tests for PokéStrategist Bayesian Opponent Modeling.
"""

import unittest
from src.card_database import CardDatabase
from src.opponent.belief_state import OpponentBeliefState
from src.opponent.opponent_model import OpponentModel
from src.schema import Card, CardCategory, PokemonStage
from src.deck.archetypes import ArchetypeCategory

class TestOpponentModel(unittest.TestCase):
    def setUp(self):
        self.model = OpponentModel()

    def test_initial_belief_is_uniform(self):
        belief = self.model.belief
        probs = belief.archetype_probabilities
        self.assertEqual(len(probs), len(ArchetypeCategory))
        # Uniform initial probability
        for p in probs.values():
            self.assertAlmostEqual(p, 1.0 / len(ArchetypeCategory), places=3)

    def test_bayesian_update_on_aggressive_card(self):
        # Reveal an aggressive basic pokemon
        card = Card(
            id="TEST-004",
            name="Roaring Moon ex",
            expansion="TEST",
            collection_number="004",
            category=CardCategory.POKEMON,
            stage=PokemonStage.BASIC,
            hp=230
        )
        self.model.observe_card_revealed(card)
        probs = self.model.belief.archetype_probabilities
        # Aggressive archetype probability should increase relative to control/stall
        self.assertGreater(probs[ArchetypeCategory.AGGRESSIVE.value], probs[ArchetypeCategory.CONTROL_STALL.value])

    def test_hand_size_and_energy_update(self):
        self.model.update_from_visible_state(
            hand_size=6,
            bench_size=4,
            active_energy_count=3,
            prizes_remaining=4,
            turn=3
        )
        self.assertGreater(self.model.belief.estimated_ko_threat_prob, 0.3)

    def test_reset_model(self):
        self.model.belief.archetype_probabilities[ArchetypeCategory.AGGRESSIVE.value] = 0.99
        self.model.reset()
        for p in self.model.belief.archetype_probabilities.values():
            self.assertAlmostEqual(p, 1.0 / len(ArchetypeCategory), places=3)

if __name__ == "__main__":
    unittest.main()
