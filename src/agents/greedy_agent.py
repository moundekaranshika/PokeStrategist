"""
PokéStrategist - Baseline 2: Greedy Agent
Selects actions that maximize immediate single-turn damage or immediate setup.
"""

from typing import List
from src.schema import GameState, Action, ActionType
from src.strategy.action_generator import ActionGenerator

class GreedyAgent:
    def __init__(self):
        self.name = "GreedyAgent"

    def select_action(self, state: GameState) -> Action:
        legal_actions = ActionGenerator.generate_legal_actions(state)
        if not legal_actions:
            return Action(action_type=ActionType.PASS_TURN)

        # 1. Highest damage attack if available
        attack_actions = [a for a in legal_actions if a.action_type == ActionType.ATTACK and a.attack]
        if attack_actions:
            attack_actions.sort(key=lambda a: a.attack.damage if a.attack else 0, reverse=True)
            return attack_actions[0]

        # 2. Attach energy to Active
        energy_active = [a for a in legal_actions if a.action_type == ActionType.ATTACH_ENERGY and a.target_index == -1]
        if energy_active:
            return energy_active[0]

        # 3. Evolve Active
        evolve_active = [a for a in legal_actions if a.action_type == ActionType.EVOLVE and a.target_index == -1]
        if evolve_active:
            return evolve_active[0]

        # 4. Play Supporter
        supporter_actions = [a for a in legal_actions if a.action_type == ActionType.PLAY_SUPPORTER]
        if supporter_actions:
            return supporter_actions[0]

        # 5. Bench basic
        bench_actions = [a for a in legal_actions if a.action_type == ActionType.BENCH_BASIC]
        if bench_actions:
            return bench_actions[0]

        # Fallback to first available action
        return legal_actions[0]
