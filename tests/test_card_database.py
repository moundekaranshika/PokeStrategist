"""
Unit Tests for PokéStrategist Card Database and Schema.
"""

import unittest
import os
from src.card_database import CardDatabase
from src.schema import Card, CardCategory, PokemonStage, EnergyType

class TestCardDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_path = "data/raw/EN_Card_Data.csv"
        cls.card_db = CardDatabase(cls.data_path).load()

    def test_database_loads_cards(self):
        self.assertGreater(len(self.card_db), 1000)

    def test_card_fields_integrity(self):
        card = self.card_db.get_by_id("MEW-001")
        if not card:
            card = self.card_db.cards[0]
        self.assertIsNotNone(card.id)
        self.assertIsNotNone(card.name)
        self.assertIsInstance(card.category, CardCategory)

    def test_search_by_name(self):
        charizards = self.card_db.search(name_query="Charizard")
        self.assertGreater(len(charizards), 0)
        for c in charizards:
            self.assertIn("charizard", c.name.lower())

    def test_filter_by_category_and_stage(self):
        basics = self.card_db.get_basic_pokemon()
        self.assertGreater(len(basics), 100)
        for b in basics:
            self.assertEqual(b.stage, PokemonStage.BASIC)
            self.assertEqual(b.category, CardCategory.POKEMON)

    def test_energy_filter(self):
        energies = self.card_db.search(category=CardCategory.ENERGY)
        self.assertGreater(len(energies), 0)
        for e in energies:
            self.assertEqual(e.category, CardCategory.ENERGY)

if __name__ == "__main__":
    unittest.main()
