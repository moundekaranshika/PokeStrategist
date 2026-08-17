"""
PokéStrategist - Card Database & Indexing Layer
Provides fast multi-index queries, filtering, card lookup, and archetype resolution.
"""

from typing import Dict, List, Optional, Set
from collections import defaultdict

from src.schema import Card, CardCategory, PokemonStage, EnergyType, TrainerType
from src.data_loader import DataLoader

class CardDatabase:
    def __init__(self, data_path: str = "data/raw/EN_Card_Data.csv"):
        self.loader = DataLoader(data_path)
        self.cards: List[Card] = []
        self._id_index: Dict[str, Card] = {}
        self._name_index: Dict[str, List[Card]] = defaultdict(list)
        self._type_index: Dict[EnergyType, List[Card]] = defaultdict(list)
        self._category_index: Dict[CardCategory, List[Card]] = defaultdict(list)
        self._stage_index: Dict[PokemonStage, List[Card]] = defaultdict(list)
        self._trainer_index: Dict[TrainerType, List[Card]] = defaultdict(list)
        self._evolution_tree: Dict[str, List[Card]] = defaultdict(list) # base_name -> evolved cards
        self._is_loaded = False

    def load(self) -> 'CardDatabase':
        """Loads and indexes the card dataset."""
        self.cards = self.loader.load_cards()
        self._rebuild_indices()
        self._is_loaded = True
        return self

    def _rebuild_indices(self):
        self._id_index.clear()
        self._name_index.clear()
        self._type_index.clear()
        self._category_index.clear()
        self._stage_index.clear()
        self._trainer_index.clear()
        self._evolution_tree.clear()

        for card in self.cards:
            self._id_index[card.id] = card
            self._name_index[card.name.lower()].append(card)
            self._category_index[card.category].append(card)

            if card.is_pokemon:
                self._type_index[card.energy_type].append(card)
                self._stage_index[card.stage].append(card)
                if card.previous_stage:
                    self._evolution_tree[card.previous_stage.lower()].append(card)

            if card.is_trainer:
                self._trainer_index[card.trainer_type].append(card)

    def __len__(self) -> int:
        return len(self.cards)

    def get_by_id(self, card_id: str) -> Optional[Card]:
        return self._id_index.get(card_id)

    def get_by_name(self, name: str) -> List[Card]:
        return self._name_index.get(name.lower(), [])

    def get_first_by_name(self, name: str) -> Optional[Card]:
        matches = self.get_by_name(name)
        return matches[0] if matches else None

    def search(self,
               category: Optional[CardCategory] = None,
               energy_type: Optional[EnergyType] = None,
               stage: Optional[PokemonStage] = None,
               trainer_type: Optional[TrainerType] = None,
               min_hp: int = 0,
               min_damage: int = 0,
               name_query: Optional[str] = None,
               query_str: Optional[str] = None) -> List[Card]:
        """Multi-criteria search over cards."""
        results = self.cards

        if category is not None:
            results = [c for c in results if c.category == category]
        if energy_type is not None:
            results = [c for c in results if c.energy_type == energy_type]
        if stage is not None:
            results = [c for c in results if c.stage == stage]
        if trainer_type is not None:
            results = [c for c in results if c.trainer_type == trainer_type]
        if min_hp > 0:
            results = [c for c in results if c.hp >= min_hp]
        if min_damage > 0:
            results = [c for c in results if any(a.damage >= min_damage for a in c.attacks)]
        q = name_query or query_str
        if q:
            q_lower = q.lower()
            results = [
                c for c in results
                if q_lower in c.name.lower() or q_lower in c.expansion.lower() or any(q_lower in a.name.lower() for a in c.attacks) or (c.ability and q_lower in c.ability.name.lower())
            ]
        return results

    def get_evolutions_for(self, pokemon_name: str) -> List[Card]:
        return self._evolution_tree.get(pokemon_name.lower(), [])

    def get_basic_pokemon(self) -> List[Card]:
        return [c for c in self.cards if c.is_basic_pokemon]

    def count(self) -> int:
        return len(self.cards)
