"""
PokéStrategist - Explainable Board Evaluator
Computes transparent, component-level utility scores for Pokémon TCG states.
Every scoring decision is strictly explainable without hidden magic numbers.
"""

from typing import Dict, Any, Tuple
from src.schema import GameState, InPlayPokemon

class BoardEvaluator:
    def __init__(self,
                 prize_weight: float = 300.0,
                 active_hp_weight: float = 0.8,
                 bench_weight: float = 0.4,
                 energy_weight: float = 40.0,
                 ko_pressure_weight: float = 120.0,
                 hand_size_weight: float = 15.0):
        self.prize_weight = prize_weight
        self.active_hp_weight = active_hp_weight
        self.bench_weight = bench_weight
        self.energy_weight = energy_weight
        self.ko_pressure_weight = ko_pressure_weight
        self.hand_size_weight = hand_size_weight

    def evaluate(self, state: GameState) -> Dict[str, Any]:
        """
        Evaluates the current GameState from the perspective of Player 0 (Self).
        Returns total_score and decomposed component metrics.
        """
        if state.is_terminal:
            if state.winner == 0:
                return {"total_score": 10000.0, "components": {"win": 10000.0}}
            elif state.winner == 1:
                return {"total_score": -10000.0, "components": {"loss": -10000.0}}

        own = state.own_state
        opp = state.opponent_visible_state

        # 1. Prize Differential
        # Lower prizes remaining is better
        prize_diff = (opp.prizes_remaining - own.prizes_remaining)
        prize_score = prize_diff * self.prize_weight

        # 2. Active Pokemon Advantage
        own_active_hp = own.active.current_hp if own.active else 0
        opp_active_hp = opp.active.current_hp if opp.active else 0
        active_hp_diff = own_active_hp - opp_active_hp
        active_score = active_hp_diff * self.active_hp_weight

        # 3. Bench Strength
        own_bench_hp = sum(p.current_hp for p in own.bench)
        opp_bench_hp = sum(p.current_hp for p in opp.bench)
        bench_score = (own_bench_hp - opp_bench_hp) * self.bench_weight

        # 4. Energy Advantage
        own_energy_total = (own.active.total_energy_count if own.active else 0) + sum(p.total_energy_count for p in own.bench)
        opp_energy_total = (opp.active.total_energy_count if opp.active else 0) + sum(p.total_energy_count for p in opp.bench)
        energy_score = (own_energy_total - opp_energy_total) * self.energy_weight

        # 5. Knockout Pressure
        ko_score = 0.0
        if own.active and opp.active:
            # Check if own active can KO opp active
            for atk in own.active.card.attacks:
                if own.active.total_energy_count >= atk.total_energy_cost:
                    dmg = atk.damage
                    # Apply weakness multiplier
                    if opp.active.card.weakness_type == own.active.card.energy_type:
                        dmg *= opp.active.card.weakness_multiplier
                    if dmg >= opp.active.current_hp:
                        ko_score += self.ko_pressure_weight
                        break

            # Check if opponent active can KO own active
            for atk in opp.active.card.attacks:
                if opp.active.total_energy_count >= atk.total_energy_cost:
                    dmg = atk.damage
                    if own.active.card.weakness_type == opp.active.card.energy_type:
                        dmg *= own.active.card.weakness_multiplier
                    if dmg >= own.active.current_hp:
                        ko_score -= self.ko_pressure_weight
                        break

        # 6. Hand Resource / Card Advantage
        hand_diff = len(own.hand) - opp.hand_size
        hand_score = hand_diff * self.hand_size_weight

        components = {
            "prize_advantage": round(prize_score, 2),
            "active_pokemon_hp": round(active_score, 2),
            "bench_strength": round(bench_score, 2),
            "energy_advantage": round(energy_score, 2),
            "knockout_pressure": round(ko_score, 2),
            "hand_card_advantage": round(hand_score, 2)
        }

        total = round(sum(components.values()), 2)
        return {
            "total_score": total,
            "components": components
        }

    def score(self, state: GameState) -> float:
        return self.evaluate(state)["total_score"]
