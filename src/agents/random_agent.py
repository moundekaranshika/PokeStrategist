"""
PokéStrategist - Baseline 1: Random Agent
Uniformly samples any legal action from the action generator.
"""

import random
from typing import List, Optional
from src.schema import GameState, Action, ActionType
from src.strategy.action_generator import ActionGenerator

class RandomAgent:
    def __init__(self, seed: Optional[int] = None):
        self.name = "RandomAgent"
        if seed is not None:
            random.seed(seed)

    def select_action(self, state: GameState) -> Action:
        legal_actions = ActionGenerator.generate_legal_actions(state)
        if not legal_actions:
            return Action(action_type=ActionType.PASS_TURN)
        return random.choice(legal_actions)
