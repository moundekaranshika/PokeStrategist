"""
PokéStrategist - Baseline 3: Heuristic Agent
Evaluates immediate 1-step action transitions using the explainable BoardEvaluator.
"""

from typing import List, Optional
from copy import deepcopy

from src.schema import GameState, Action, ActionType
from src.strategy.action_generator import ActionGenerator
from src.strategy.board_evaluator import BoardEvaluator
from src.planning.monte_carlo import MonteCarloPlanner

class HeuristicAgent:
    def __init__(self, evaluator: Optional[BoardEvaluator] = None):
        self.name = "HeuristicAgent"
        self.evaluator = evaluator or BoardEvaluator()
        self.planner_helper = MonteCarloPlanner(self.evaluator)

    def select_action(self, state: GameState) -> Action:
        legal_actions = ActionGenerator.generate_legal_actions(state)
        if not legal_actions:
            return Action(action_type=ActionType.PASS_TURN)

        best_action = legal_actions[0]
        best_score = -float("inf")

        for action in legal_actions:
            # Clone and apply 1 step
            sim_state = deepcopy(state)
            self.planner_helper._apply_action(sim_state, action, player_idx=0)
            score = self.evaluator.score(sim_state)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action
