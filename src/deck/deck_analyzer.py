"""
PokéStrategist - Deck & Card Pool Analyzer
Evaluates 60-card deck lists and card pools using feature-based scoring
and identifies strategic archetypes without arbitrary assumptions.
"""

from typing import Dict, List, Tuple, Any
from collections import Counter

from src.schema import Card, CardCategory, PokemonStage, EnergyType, TrainerType
from src.deck.archetypes import ArchetypeCategory, ARCHETYPE_PROFILES
from src.features.card_features import CardFeatureExtractor

class DeckAnalyzer:
    def __init__(self, cards: List[Card]):
        self.cards = cards
        # Ensure features are computed
        for c in self.cards:
            if c.is_pokemon and not c.features:
                CardFeatureExtractor.extract_features(c)

    def analyze(self) -> Dict[str, Any]:
        """Performs full structural and strategic evaluation of the deck."""
        total_count = len(self.cards)
        if total_count == 0:
            return {"error": "Empty deck"}

        # Composition split
        pokemon_cards = [c for c in self.cards if c.is_pokemon]
        trainer_cards = [c for c in self.cards if c.is_trainer]
        energy_cards = [c for c in self.cards if c.is_energy]

        p_ratio = len(pokemon_cards) / total_count
        t_ratio = len(trainer_cards) / total_count
        e_ratio = len(energy_cards) / total_count

        # Energy type distribution
        energy_types = Counter([c.energy_type.value for c in energy_cards if c.energy_type != EnergyType.NONE])
        pokemon_types = Counter([c.energy_type.value for c in pokemon_cards if c.energy_type != EnergyType.NONE])

        # Evolution stage distribution
        stage_dist = Counter([c.stage.value for c in pokemon_cards])

        # Trainer subtypes
        trainer_types = Counter([c.trainer_type.value for c in trainer_cards])

        # Key attackers and abilities
        key_pokemon = sorted(
            [c for c in pokemon_cards if c.features],
            key=lambda x: (x.features.offensive_potential + x.features.hp),
            reverse=True
        )[:5]

        # Strongest attacks
        strongest_attacks = []
        for p in pokemon_cards:
            for atk in p.attacks:
                strongest_attacks.append({
                    "pokemon": p.name,
                    "attack": atk.name,
                    "damage": atk.damage,
                    "cost": atk.energy_cost_str,
                    "efficiency": round(atk.damage / max(1, atk.total_energy_cost), 2),
                    "effect": atk.effect_text
                })
        strongest_attacks.sort(key=lambda a: a["damage"], reverse=True)
        top_attacks = strongest_attacks[:5]

        # Archetype scoring
        archetype_scores = self._score_archetypes(p_ratio, t_ratio, e_ratio, pokemon_cards, trainer_cards)
        primary_archetype = max(archetype_scores.items(), key=lambda x: x[1])[0]

        # Weakness analysis
        weaknesses = Counter([c.weakness_type.value for c in pokemon_cards if c.weakness_type != EnergyType.NONE])

        # Consistency score (0-100)
        search_items = sum(1 for c in trainer_cards if any(k in c.name.lower() for k in ["ball", "poffin", "vessel", "arven", "irida"]))
        draw_supporters = sum(1 for c in trainer_cards if c.trainer_type == TrainerType.SUPPORTER and any(k in c.name.lower() for k in ["research", "iono", "judge", "colress", "sada"]))
        basics_count = stage_dist.get(PokemonStage.BASIC.value, 0)
        
        consistency_score = min(100, int(
            (min(search_items, 12) / 12.0 * 35.0) +
            (min(draw_supporters, 8) / 8.0 * 35.0) +
            (min(basics_count, 12) / 12.0 * 30.0)
        ))

        return {
            "total_cards": total_count,
            "composition": {
                "pokemon_count": len(pokemon_cards),
                "trainer_count": len(trainer_cards),
                "energy_count": len(energy_cards),
                "pokemon_ratio": round(p_ratio, 3),
                "trainer_ratio": round(t_ratio, 3),
                "energy_ratio": round(e_ratio, 3)
            },
            "stage_distribution": dict(stage_dist),
            "trainer_distribution": dict(trainer_types),
            "energy_types": dict(energy_types),
            "pokemon_types": dict(pokemon_types),
            "archetype_scores": archetype_scores,
            "primary_archetype": primary_archetype,
            "consistency_score": consistency_score,
            "key_pokemon": [{"name": p.name, "hp": p.hp, "stage": p.stage.value, "offensive": p.features.offensive_potential if p.features else 0} for p in key_pokemon],
            "top_attacks": top_attacks,
            "shared_weaknesses": dict(weaknesses)
        }

    def _score_archetypes(self, p_ratio: float, t_ratio: float, e_ratio: float, pokemon: List[Card], trainers: List[Card]) -> Dict[str, float]:
        scores = {}
        all_card_names = [c.name for c in self.cards]
        all_card_text = " ".join([f"{c.name} {c.synergy_tag} {c.rule_box_text} {c.ability.effect_text if c.ability else ''}" for c in self.cards]).lower()

        for arch_cat, profile in ARCHETYPE_PROFILES.items():
            # Ratio divergence penalty
            p_diff = abs(p_ratio - profile.ideal_pokemon_ratio)
            t_diff = abs(t_ratio - profile.ideal_trainer_ratio)
            e_diff = abs(e_ratio - profile.ideal_energy_ratio)
            ratio_match = max(0.0, 1.0 - (p_diff + t_diff + e_diff) * 1.5)

            # Keyword match bonus
            indicator_hits = sum(1 for ind in profile.key_indicators if any(ind.lower() in name.lower() for name in all_card_names))
            indicator_score = min(1.0, indicator_hits / max(1, len(profile.key_indicators) * 0.5))

            # Specific archetype heuristics
            specific_bonus = 0.0
            if arch_cat == ArchetypeCategory.SETUP_EVOLUTION:
                stage2_count = sum(1 for c in pokemon if c.stage == PokemonStage.STAGE_2)
                rare_candy = sum(1 for c in trainers if "rare candy" in c.name.lower())
                if stage2_count >= 2 and rare_candy >= 2:
                    specific_bonus += 0.3
            elif arch_cat == ArchetypeCategory.AGGRESSIVE:
                basic_rulebox = sum(1 for c in pokemon if c.stage == PokemonStage.BASIC and (c.features and c.features.is_rule_box))
                if basic_rulebox >= 2:
                    specific_bonus += 0.25
            elif arch_cat == ArchetypeCategory.ENERGY_ACCELERATION:
                if any(k in all_card_text for k in ["attach", "accelerat", "discard to", "from your discard"]):
                    specific_bonus += 0.2

            total_score = round((ratio_match * 0.35) + (indicator_score * 0.45) + (specific_bonus * 0.20), 3)
            scores[arch_cat.value] = total_score

        return scores
