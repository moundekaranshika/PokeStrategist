"""
PokéStrategist - Game Environment Abstraction
Defines the base interface GameEnvironment and provides the LocalResearchSimulator
for local experiments, agent benchmarking, and ablation studies.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
import random

from src.schema import (
    GameState, Action, ActionType, Card, InPlayPokemon,
    PlayerState, VisibleOpponentState, PokemonStage, EnergyType
)
from src.strategy.action_generator import ActionGenerator
from src.game.state import GameStateManager

class GameEnvironment(ABC):
    """Abstract Environment Interface."""
    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> GameState:
        pass

    @abstractmethod
    def get_state(self) -> GameState:
        pass

    @abstractmethod
    def get_legal_actions(self) -> List[Action]:
        pass

    @abstractmethod
    def step(self, action: Action) -> Tuple[GameState, float, bool, Dict[str, Any]]:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass

class LocalResearchSimulator(GameEnvironment):
    """
    LOCAL RESEARCH SIMULATOR
    A standalone, authentic local simulator implementing Pokémon TCG rules
    for local experimental benchmarking when Kaggle official server is offline.
    """
    def __init__(self, deck_p0: List[Card], deck_p1: List[Card]):
        self.deck_p0 = deck_p0
        self.deck_p1 = deck_p1
        self.current_state: Optional[GameState] = None
        self.max_turns = 40
        self.p0_cards_drawn = 0
        self.p1_cards_drawn = 0

    def reset(self, seed: Optional[int] = None) -> GameState:
        self.current_state = GameStateManager.create_initial_state(
            self.deck_p0, self.deck_p1, seed=seed
        )
        self.p0_cards_drawn = 7
        self.p1_cards_drawn = 7
        return self.current_state

    def get_state(self) -> GameState:
        if not self.current_state:
            raise ValueError("Environment not initialized. Call reset() first.")
        return self.current_state

    def get_legal_actions(self) -> List[Action]:
        if not self.current_state:
            return []
        return ActionGenerator.generate_legal_actions(self.current_state)

    def is_terminal(self) -> bool:
        if not self.current_state:
            return True
        return self.current_state.is_terminal or self.current_state.turn >= self.max_turns

    def step(self, action: Action) -> Tuple[GameState, float, bool, Dict[str, Any]]:
        """
        Executes action for active player, handles battle resolution, turn progression,
        and returns (new_state, reward, is_terminal, info).
        """
        state = self.current_state
        if not state or state.is_terminal:
            return state, 0.0, True, {"reason": "Already terminal"}

        own = state.own_state
        opp = state.opponent_visible_state
        reward = 0.0
        info: Dict[str, Any] = {"action_executed": action.describe()}

        # 1. Process Action
        if action.action_type == ActionType.ATTACK and action.attack and own.active and opp.active:
            dmg = action.attack.damage
            # Check weakness
            if opp.active.card.weakness_type == own.active.card.energy_type:
                dmg *= opp.active.card.weakness_multiplier
            # Check resistance
            if opp.active.card.resistance_type == own.active.card.energy_type:
                dmg = max(0, dmg + opp.active.card.resistance_value)

            opp.active.current_hp -= dmg
            state.action_history.append(f"Turn {state.turn}: Player attacked with {action.attack.name} for {dmg} DMG.")

            if opp.active.current_hp <= 0:
                prizes = 2 if (opp.active.card.features and opp.active.card.features.is_rule_box) else 1
                own.prizes_remaining = max(0, own.prizes_remaining - prizes)
                reward += 100.0 * prizes
                state.action_history.append(f"Turn {state.turn}: Opponent's Active Pokémon Knocked Out! Took {prizes} Prize(s).")
                
                if own.prizes_remaining == 0:
                    state.is_terminal = True
                    state.winner = 0
                    reward += 500.0
                elif opp.bench:
                    opp.active = opp.bench.pop(0)
                else:
                    state.is_terminal = True
                    state.winner = 0
                    reward += 500.0

            # Attack ends turn
            self._end_turn_and_advance()

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
                hp_diff = action.card.hp - target.card.hp
                target.card = action.card
                target.current_hp += max(0, hp_diff)

        elif action.action_type == ActionType.PLAY_SUPPORTER and action.card:
            if action.card in own.hand:
                own.hand.remove(action.card)
            own.discard_pile.append(action.card)
            own.supporter_played_this_turn = True
            # Simple standard draw effect: Professor draws 3, Iono draws
            if "research" in action.card.name.lower():
                # Draw cards
                pass

        elif action.action_type == ActionType.PASS_TURN:
            self._end_turn_and_advance()

        # Check turn limit
        if state.turn >= self.max_turns:
            state.is_terminal = True
            # Judge winner by remaining prizes
            if own.prizes_remaining < opp.prizes_remaining:
                state.winner = 0
            elif opp.prizes_remaining < own.prizes_remaining:
                state.winner = 1
            else:
                state.winner = -1 # Draw

        return state, reward, state.is_terminal, info

    def _end_turn_and_advance(self):
        """Advances turn counter and resets once-per-turn flags."""
        state = self.current_state
        if not state:
            return

        state.turn += 1
        state.own_state.energy_attached_this_turn = False
        state.own_state.supporter_played_this_turn = False
        
        # Simulate simple automatic opponent counter-play during opponent's half of the turn
        opp = state.opponent_visible_state
        own = state.own_state
        if not state.is_terminal and opp.active and own.active:
            # Opponent attaches energy if needed
            opp.active.attached_energies.append(Card(id="E-DUMMY", name="Energy", expansion="", collection_number="", category=Card.category if hasattr(Card, 'category') else None))
            # Opponent attacks if has attack
            attacks = opp.active.card.attacks
            if attacks:
                best_opp_atk = max(attacks, key=lambda a: a.damage)
                opp_dmg = best_opp_atk.damage
                if own.active.card.weakness_type == opp.active.card.energy_type:
                    opp_dmg *= own.active.card.weakness_multiplier
                own.active.current_hp -= opp_dmg
                state.action_history.append(f"Turn {state.turn}: Opponent attacked with {best_opp_atk.name} for {opp_dmg} DMG.")

                if own.active.current_hp <= 0:
                    prizes = 2 if (own.active.card.features and own.active.card.features.is_rule_box) else 1
                    opp.prizes_remaining = max(0, opp.prizes_remaining - prizes)
                    state.action_history.append(f"Turn {state.turn}: Your Active Pokémon Knocked Out! Opponent took {prizes} Prize(s).")
                    if opp.prizes_remaining == 0:
                        state.is_terminal = True
                        state.winner = 1
                    elif own.bench:
                        own.active = own.bench.pop(0)
                    else:
                        state.is_terminal = True
                        state.winner = 1
