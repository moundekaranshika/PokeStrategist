"""
PokéStrategist - Monte Carlo Forward Simulation Planner
Simulates stochastic rollouts of candidate actions against plausible opponent
belief responses to compute high-confidence Expected Utility rankings.
"""

import random
from typing import Dict, List, Tuple, Any, Optional
from copy import deepcopy

from src.schema import GameState, Action, ActionType, InPlayPokemon, Card
from src.strategy.board_evaluator import BoardEvaluator
from src.opponent.belief_state import OpponentBeliefState
from src.deck.archetypes import ArchetypeCategory

class MonteCarloPlanner:
    def __init__(
        self,
        board_evaluator: Optional[BoardEvaluator] = None,
        default_simulations: int = 50,
        rollout_depth: int = 2
    ):
        self.evaluator = board_evaluator or BoardEvaluator()
        self.default_simulations = default_simulations
        self.rollout_depth = rollout_depth

    def plan(
        self,
        state: GameState,
        candidate_actions: List[Action],
        belief: Optional[OpponentBeliefState] = None,
        num_simulations: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluates each candidate action via forward Monte Carlo simulation rollouts.
        Returns sorted list of actions with expected utility, confidence, and rollout metrics.
        """
        n_sims = num_simulations or self.default_simulations
        action_results: List[Dict[str, Any]] = []

        if not candidate_actions:
            return []

        for action in candidate_actions:
            rollout_scores: List[float] = []

            for _ in range(n_sims):
                # 1. Clone state
                sim_state = deepcopy(state)

                # 2. Apply our action
                self._apply_action(sim_state, action, player_idx=0)

                # 3. Simulate opponent response based on belief state
                self._simulate_opponent_turn(sim_state, belief)

                # 4. Evaluate resulting leaf state
                leaf_score = self.evaluator.score(sim_state)
                rollout_scores.append(leaf_score)

            mean_utility = sum(rollout_scores) / len(rollout_scores)
            variance = sum((s - mean_utility) ** 2 for s in rollout_scores) / len(rollout_scores)
            std_dev = (variance ** 0.5)

            action_results.append({
                "action": action,
                "description": action.describe(),
                "expected_utility": round(mean_utility, 2),
                "std_dev": round(std_dev, 2),
                "num_simulations": n_sims,
                "min_utility": round(min(rollout_scores), 2),
                "max_utility": round(max(rollout_scores), 2)
            })

        # Sort by expected utility descending
        action_results.sort(key=lambda x: x["expected_utility"], reverse=True)
        return action_results

    def _apply_action(self, state: GameState, action: Action, player_idx: int):
        """Applies an action to the mutable simulation state."""
        own = state.own_state if player_idx == 0 else None
        opp = state.opponent_visible_state if player_idx == 0 else None

        if not own:
            return

        if action.action_type == ActionType.ATTACK and action.attack and own.active and opp and opp.active:
            damage = action.attack.damage
            # Check weakness
            if opp.active.card.weakness_type == own.active.card.energy_type:
                damage *= opp.active.card.weakness_multiplier
            opp.active.current_hp -= damage
            if opp.active.current_hp <= 0:
                # Prize taken
                prizes_to_take = 2 if (opp.active.card.features and opp.active.card.features.is_rule_box) else 1
                own.prizes_remaining = max(0, own.prizes_remaining - prizes_to_take)
                if own.prizes_remaining == 0:
                    state.is_terminal = True
                    state.winner = 0
                else:
                    # Promote bench if available
                    if opp.bench:
                        opp.active = opp.bench.pop(0)
                    else:
                        state.is_terminal = True
                        state.winner = 0

        elif action.action_type == ActionType.ATTACH_ENERGY and action.energy_card:
            if action.energy_card in own.hand:
                own.hand.remove(action.energy_card)
            own.energy_attached_this_turn = True
            if action.target_index == -1 and own.active:
                own.active.attached_energies.append(action.energy_card)
            elif action.target_index is not None and 0 <= action.target_index < len(own.bench):
                own.bench[action.target_index].attached_energies.append(action.energy_card)

        elif action.action_type == ActionType.BENCH_BASIC and action.card:
            if action.card in own.hand:
                own.hand.remove(action.card)
            new_pkmn = InPlayPokemon(card=action.card, current_hp=action.card.hp)
            own.bench.append(new_pkmn)

        elif action.action_type == ActionType.EVOLVE and action.card:
            if action.card in own.hand:
                own.hand.remove(action.card)
            target = own.active if action.target_index == -1 else (own.bench[action.target_index] if 0 <= action.target_index < len(own.bench) else None)
            if target:
                hp_delta = action.card.hp - target.card.hp
                target.card = action.card
                target.current_hp += max(0, hp_delta)

        elif action.action_type == ActionType.PLAY_SUPPORTER and action.card:
            if action.card in own.hand:
                own.hand.remove(action.card)
            own.discard_pile.append(action.card)
            own.supporter_played_this_turn = True

    def _simulate_opponent_turn(self, state: GameState, belief: Optional[OpponentBeliefState]):
        """Simulates stochastic opponent response weighted by belief state."""
        opp = state.opponent_visible_state
        own = state.own_state

        if state.is_terminal or not opp.active or not own.active:
            return

        # Estimate opponent attack power based on archetype
        likely_arch = belief.get_most_likely_archetype() if belief else ArchetypeCategory.BALANCED.value
        
        base_threat = 40
        if "Aggressive" in likely_arch:
            base_threat = 120
        elif "Burst" in likely_arch:
            base_threat = 160
        elif "Setup" in likely_arch:
            base_threat = 70

        # Add stochastic variance
        simulated_opp_dmg = max(0, int(random.gauss(base_threat, 30)))
        
        # Check weakness
        if own.active.card.weakness_type == opp.active.card.energy_type:
            simulated_opp_dmg *= 2

        own.active.current_hp -= simulated_opp_dmg

        if own.active.current_hp <= 0:
            prizes_lost = 2 if (own.active.card.features and own.active.card.features.is_rule_box) else 1
            opp.prizes_remaining = max(0, opp.prizes_remaining - prizes_lost)
            if opp.prizes_remaining == 0:
                state.is_terminal = True
                state.winner = 1
            else:
                if own.bench:
                    own.active = own.bench.pop(0)
                else:
                    state.is_terminal = True
                    state.winner = 1
