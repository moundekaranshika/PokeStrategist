"""
PokéStrategist - Game State Representation
Maintains an explicit, strictly separated state representation between
the agent's own private knowledge, global visible board state,
and hidden opponent beliefs.
"""

from typing import Dict, List, Optional, Any
from copy import deepcopy

from src.schema import Card, InPlayPokemon, PlayerState, VisibleOpponentState, GameState, Action, ActionType, PokemonStage

class GameStateManager:
    @staticmethod
    def create_initial_state(
        own_deck: List[Card],
        opponent_deck: List[Card],
        seed: Optional[int] = None
    ) -> GameState:
        """
        Sets up a standard tournament opening state:
        - 7 cards in hand
        - 1 Active Basic Pokemon
        - Up to 2 Bench Basic Pokemon
        - 6 Prize cards each
        """
        import random
        if seed is not None:
            random.seed(seed)

        own_deck_copy = list(own_deck)
        opp_deck_copy = list(opponent_deck)
        random.shuffle(own_deck_copy)
        random.shuffle(opp_deck_copy)

        # Setup own side
        own_hand = [own_deck_copy.pop() for _ in range(7)]
        # Find a basic pokemon for active
        own_basics = [c for c in own_hand if c.is_basic_pokemon]
        if not own_basics:
            # Simple mulligan handling for setup
            basic_candidates = [c for c in own_deck_copy if c.is_basic_pokemon]
            if basic_candidates:
                chosen = basic_candidates[0]
                own_deck_copy.remove(chosen)
                own_hand.append(chosen)
                own_basics = [chosen]

        active_card = own_basics[0] if own_basics else Card(
            id="BASIC-FALLBACK", name="Basic Starter", expansion="Standard", collection_number="001",
            category=Card.category if hasattr(Card, 'category') else None, hp=70
        )
        if active_card in own_hand:
            own_hand.remove(active_card)

        own_active = InPlayPokemon(card=active_card, current_hp=active_card.hp)
        own_bench = []

        # Setup prizes
        own_prizes = 6
        for _ in range(min(6, len(own_deck_copy))):
            own_deck_copy.pop()

        # Setup opponent side
        opp_hand = [opp_deck_copy.pop() for _ in range(7)]
        opp_basics = [c for c in opp_hand if c.is_basic_pokemon]
        if not opp_basics:
            basic_candidates = [c for c in opp_deck_copy if c.is_basic_pokemon]
            if basic_candidates:
                chosen = basic_candidates[0]
                opp_deck_copy.remove(chosen)
                opp_hand.append(chosen)
                opp_basics = [chosen]

        opp_active_card = opp_basics[0] if opp_basics else active_card
        if opp_active_card in opp_hand:
            opp_hand.remove(opp_active_card)

        opp_active = InPlayPokemon(card=opp_active_card, current_hp=opp_active_card.hp)
        opp_bench = []

        for _ in range(min(6, len(opp_deck_copy))):
            opp_deck_copy.pop()

        own_player_state = PlayerState(
            active=own_active,
            bench=own_bench,
            hand=own_hand,
            deck_count=len(own_deck_copy),
            discard_pile=[],
            lost_zone=[],
            prizes_remaining=own_prizes
        )

        opp_visible_state = VisibleOpponentState(
            active=opp_active,
            bench=opp_bench,
            hand_size=len(opp_hand),
            prizes_remaining=6,
            discard_pile=[],
            lost_zone=[],
            revealed_cards=[],
            known_energy_count=0,
            supporter_played_this_turn=False
        )

        state = GameState(
            turn=1,
            active_player_index=0,
            own_state=own_player_state,
            opponent_visible_state=opp_visible_state,
            game_phase="MAIN",
            legal_actions=[],
            action_history=["Turn 1 started. Both players deployed Active Pokémon."]
        )
        return state

    @staticmethod
    def clone_state(state: GameState) -> GameState:
        """Performs deep copy for forward simulation rollouts."""
        return deepcopy(state)
