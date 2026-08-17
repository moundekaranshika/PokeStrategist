"""
PokéStrategist - Baseline 4: Probabilistic Agent
Combines board heuristics with real-time Bayesian belief tracking over opponent archetypes.
"""

from typing import List, Optional
from copy import deepcopy

from src.schema import GameState, Action, ActionType
from src.strategy.action_generator import ActionGenerator
from src.strategy.board_evaluator import BoardEvaluator
from src.opponent.opponent_model import OpponentModel
from src.planning.monte_carlo import MonteCarloPlanner

class ProbabilisticAgent:
    def __init__(self, evaluator: Optional[BoardEvaluator] = None):
        self.name = "ProbabilisticAgent"
        self.evaluator = evaluator or BoardEvaluator()
        self.opponent_model = OpponentModel()
        self.planner_helper = MonteCarloPlanner(self.evaluator)

    def select_action(self, state: GameState) -> Action:
        legal_actions = ActionGenerator.generate_legal_actions(state)
        if not legal_actions:
            return Action(action_type=ActionType.PASS_TURN)

        # Dynamic weighting based on estimated opponent threat probability
        threat_prob = self.opponent_model.belief.estimated_ko_threat_prob

        best_action = legal_actions[0]
        best_score = -float("inf")

        for action in legal_actions:
            sim_state = deepcopy(state)
            self.planner_helper._apply_action(sim_state, action, player_idx=0)
            score = self.evaluator.score(sim_state)

            # Modulate score based on opponent model threat
            if threat_prob > 0.5 and action.action_type == ActionType.RETREAT:
                score += 50.0 # Prioritize retreat when high threat detected

            if score > best_score:
                best_score = score
                best_action = action

        return best_action
