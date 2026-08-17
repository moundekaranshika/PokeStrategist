"""
PokéStrategist - Card Feature Engineering Pipeline
Calculates mathematically grounded, explainable strategic features for Pokémon cards.
Does not fabricate nonexistent fields; safely handles missing and sparse attributes.
"""

from typing import Dict, List, Optional
from src.schema import Card, StrategicFeatures, PokemonStage

class CardFeatureExtractor:
    @staticmethod
    def extract_features(card: Card) -> StrategicFeatures:
        """
        Extracts strategic features from a single Card.
        Returns a StrategicFeatures instance populated with derived ratios.
        """
        if not card.is_pokemon:
            is_draw = any(w in (card.effect or "").lower() or w in card.name.lower() for w in ["draw", "research", "iono", "judge"])
            features = StrategicFeatures(is_draw_supporter=is_draw)
            card.features = features
            return features

        hp = card.hp
        retreat = card.retreat_cost
        attacks = card.attacks or []

        # Find best attack stats
        max_dmg = 0
        min_energy = 999
        best_efficiency = 0.0

        for a in attacks:
            if a.damage > max_dmg:
                max_dmg = a.damage
            if a.total_energy_cost < min_energy and a.total_energy_cost > 0:
                min_energy = a.total_energy_cost
            eff = a.damage / max(1, a.total_energy_cost)
            if eff > best_efficiency:
                best_efficiency = eff

        if min_energy == 999:
            min_energy = 0

        # Setup requirement score (0 for Basic, 1 for Stage 1, 2 for Stage 2)
        stage_score = 0
        if card.stage == PokemonStage.STAGE_1:
            stage_score = 1
        elif card.stage == PokemonStage.STAGE_2:
            stage_score = 2
        elif card.stage in [PokemonStage.VMAX, PokemonStage.VSTAR]:
            stage_score = 1

        # Check if Rule Box / Multi-prize card
        is_rule_box = bool(card.rule_box_text) or "ex" in card.name or "V" in card.name or "VSTAR" in card.name or "VMAX" in card.name
        prize_yield = 2 if is_rule_box else 1

        # Survivability index: HP normalized against mobility and prize trade
        # Higher HP with low retreat and single prize gives high trade efficiency
        survivability = (hp / max(1, retreat + 1)) / (prize_yield)

        # Offensive potential: weighted product of burst damage and energy efficiency
        offensive = (max_dmg * 0.7) + (best_efficiency * 15.0)

        # Defensive potential: Raw durability metric
        defensive = hp - (retreat * 15.0)

        # Tempo score: attack speed vs requirement
        tempo = (best_efficiency / max(1, stage_score + 1)) * (1.2 if card.ability else 1.0)

        features = StrategicFeatures(
            hp=hp,
            max_damage=max_dmg,
            min_energy_cost=min_energy,
            attack_efficiency=round(best_efficiency, 2),
            survivability_index=round(survivability, 2),
            offensive_potential=round(offensive, 2),
            defensive_potential=round(defensive, 2),
            setup_requirement_score=stage_score,
            tempo_score=round(tempo, 2),
            is_rule_box=is_rule_box,
            prize_yield=prize_yield
        )
        card.features = features
        return features

    @classmethod
    def extract_card_features(cls, card: Card) -> StrategicFeatures:
        return cls.extract_features(card)

    @classmethod
    def process_all_cards(cls, cards: List[Card]) -> Dict[str, StrategicFeatures]:
        """Extracts and assigns features for a collection of cards."""
        return {c.id: cls.extract_features(c) for c in cards}
