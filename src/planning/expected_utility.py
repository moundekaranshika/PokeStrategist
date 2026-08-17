"""
PokéStrategist - Expected Utility Computation Engine
Calculates stochastic expectation over outcome states given candidate actions.
"""

from typing import Dict, List, Any
from src.schema import GameState, Action
from src.strategy.board_evaluator import BoardEvaluator

class ExpectedUtilityCalculator:
    def __init__(self, board_evaluator: Optional[BoardEvaluator] = None):
        self.evaluator = board_evaluator or BoardEvaluator()

    def calculate_expected_utility(self, rollout_states: List[GameState]) -> float:
        """
        Computes the empirical mean of state values from Monte Carlo rollout branches.
        """
        if not rollout_states:
            return 0.0
        scores = [self.evaluator.score(s) for s in rollout_states]
        return sum(scores) / len(scores)
