"""
Unit Tests for PokéStrategist Feature Extraction Engine.
"""

import unittest
from src.card_database import CardDatabase
from src.features.card_features import CardFeatureExtractor
from src.schema import Card, CardCategory, Attack

class TestCardFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card_db = CardDatabase("data/raw/EN_Card_Data.csv").load()
        CardFeatureExtractor.process_all_cards(cls.card_db.cards)

    def test_feature_extraction_exists(self):
        sample = self.card_db.cards[0]
        self.assertIsNotNone(sample.features)

    def test_damage_efficiency_computation(self):
        # Create a test Pokémon card with 2 energy attack for 80 damage
        card = Card(
            id="TEST-001",
            name="Test Striker",
            expansion="TEST",
            collection_number="001",
            category=CardCategory.POKEMON,
            hp=120,
            attacks=[
                Attack(name="Hyper Beam", energy_cost_str="[Fire][Fire]", total_energy_cost=2, energy_types=["Fire", "Fire"], damage=80)
            ]
        )
        features = CardFeatureExtractor.extract_card_features(card)
        self.assertEqual(features.max_attack_damage, 80)
        self.assertEqual(features.damage_to_cost_ratio, 40.0)
        self.assertAlmostEqual(features.durability_score, 120.0)

    def test_rule_box_detection(self):
        ex_card = Card(
            id="TEST-002",
            name="Mewtwo ex",
            expansion="TEST",
            collection_number="002",
            category=CardCategory.POKEMON,
            hp=220
        )
        features = CardFeatureExtractor.extract_card_features(ex_card)
        self.assertTrue(features.is_rule_box)

    def test_trainer_categorization(self):
        draw_supporter = Card(
            id="TEST-003",
            name="Professor's Research",
            expansion="TEST",
            collection_number="003",
            category=CardCategory.TRAINER,
            effect="Discard your hand and draw 7 cards."
        )
        features = CardFeatureExtractor.extract_card_features(draw_supporter)
        self.assertTrue(features.is_draw_supporter)

if __name__ == "__main__":
    unittest.main()
