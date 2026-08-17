"""
PokéStrategist - Candidate Action Generator
Generates all strictly valid, rule-compliant candidate actions for a given GameState.
"""

from typing import List, Optional
from src.schema import (
    GameState, Action, ActionType, Card, CardCategory,
    PokemonStage, TrainerType, InPlayPokemon
)

class ActionGenerator:
    @staticmethod
    def generate_legal_actions(state: GameState) -> List[Action]:
        """
        Enumerates all legal candidate actions for the current active player.
        """
        legal_actions: List[Action] = []
        player = state.own_state if state.active_player_index == 0 else None
        
        # If we are generating for player 0
        if player is None or player.active is None:
            return [Action(action_type=ActionType.PASS_TURN)]

        hand = player.hand
        active = player.active
        bench = player.bench

        # 1. ATTACK ACTIONS
        if active and active.current_hp > 0:
            for atk in active.card.attacks:
                if active.total_energy_count >= atk.total_energy_cost:
                    legal_actions.append(Action(
                        action_type=ActionType.ATTACK,
                        attack=atk,
                        metadata={"target": "opponent_active", "damage": atk.damage}
                    ))

        # 2. ATTACH ENERGY ACTIONS (Limit 1 per turn from hand)
        if not player.energy_attached_this_turn:
            energy_cards = [c for c in hand if c.is_energy]
            for e_card in energy_cards:
                # Can attach to Active (target_index = -1)
                legal_actions.append(Action(
                    action_type=ActionType.ATTACH_ENERGY,
                    energy_card=e_card,
                    target_index=-1,
                    metadata={"target_name": active.card.name}
                ))
                # Can attach to Bench slots (target_index = 0, 1, 2...)
                for idx, b_pkmn in enumerate(bench):
                    legal_actions.append(Action(
                        action_type=ActionType.ATTACH_ENERGY,
                        energy_card=e_card,
                        target_index=idx,
                        metadata={"target_name": b_pkmn.card.name}
                    ))

        # 3. BENCH BASIC POKEMON (Max 5 on bench)
        if len(bench) < 5:
            basic_cards = [c for c in hand if c.is_basic_pokemon]
            for b_card in basic_cards:
                legal_actions.append(Action(
                    action_type=ActionType.BENCH_BASIC,
                    card=b_card,
                    metadata={"name": b_card.name}
                ))

        # 4. EVOLUTION ACTIONS
        evolution_cards = [c for c in hand if c.is_pokemon and c.stage in [PokemonStage.STAGE_1, PokemonStage.STAGE_2, PokemonStage.VSTAR, PokemonStage.EX]]
        for evo_card in evolution_cards:
            prev = evo_card.previous_stage.lower() if evo_card.previous_stage else ""
            if prev:
                # Check Active
                if prev in active.card.name.lower():
                    legal_actions.append(Action(
                        action_type=ActionType.EVOLVE,
                        card=evo_card,
                        target_index=-1,
                        metadata={"target_name": active.card.name}
                    ))
                # Check Bench
                for idx, b_pkmn in enumerate(bench):
                    if prev in b_pkmn.card.name.lower():
                        legal_actions.append(Action(
                            action_type=ActionType.EVOLVE,
                            card=evo_card,
                            target_index=idx,
                            metadata={"target_name": b_pkmn.card.name}
                        ))

        # 5. PLAY TRAINERS (Supporters & Items)
        trainer_cards = [c for c in hand if c.is_trainer]
        for t_card in trainer_cards:
            if t_card.trainer_type == TrainerType.SUPPORTER and not player.supporter_played_this_turn:
                legal_actions.append(Action(
                    action_type=ActionType.PLAY_SUPPORTER,
                    card=t_card,
                    metadata={"name": t_card.name}
                ))
            elif t_card.trainer_type == TrainerType.ITEM:
                legal_actions.append(Action(
                    action_type=ActionType.PLAY_ITEM,
                    card=t_card,
                    metadata={"name": t_card.name}
                ))

        # 6. RETREAT ACTIVE
        if bench and active.total_energy_count >= active.card.retreat_cost and active.card.retreat_cost > 0:
            for idx, b_pkmn in enumerate(bench):
                legal_actions.append(Action(
                    action_type=ActionType.RETREAT,
                    target_index=idx,
                    metadata={"target_name": b_pkmn.card.name}
                ))

        # 7. PASS TURN (Always legal default fallback)
        legal_actions.append(Action(action_type=ActionType.PASS_TURN))

        state.legal_actions = legal_actions
        return legal_actions
