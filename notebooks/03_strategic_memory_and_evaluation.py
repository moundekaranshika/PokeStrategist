"""
# Notebook 03: Strategic Memory & Dynamic Board Evaluation
PokéStrategist Research Suite

Demonstrates:
1. Multi-factor board state scoring (Prize race, Active tempo, Bench depth, Energy investment)
2. Strategic episodic memory tracking cross-turn evolution chains and energy momentum
"""

import os
import sys
sys.path.insert(0, os.path.abspath("."))

from src.strategy.board_evaluator import BoardEvaluator
from src.memory.strategic_memory import StrategicMemory
from src.memory.game_memory import GameMemory
from src.schema import GameState, PlayerState, VisibleOpponentState, InPlayPokemon, Card, CardCategory, PokemonStage, Attack

def run_notebook_03():
    print("=" * 70)
    print("  PokéStrategist - Notebook 03: Strategic Memory & Evaluation")
    print("=" * 70)

    evaluator = BoardEvaluator()
    memory = StrategicMemory()

    # Create active Pokémon
    char = Card(
        id="OBF-125",
        name="Charizard ex",
        expansion="OBF",
        collection_number="125",
        category=CardCategory.POKEMON,
        stage=PokemonStage.STAGE_2,
        hp=330,
        attacks=[Attack(name="Burning Darkness", energy_cost_str="[Fire][Fire]", total_energy_cost=2, energy_types=["Fire", "Fire"], damage=180)],
        rule_box_text="ex rule"
    )
    fire_e = Card(id="SVI-E01", name="Fire Energy", expansion="SVI", collection_number="E01", category=CardCategory.ENERGY)

    state = GameState(
        turn=3,
        own_state=PlayerState(
            active=InPlayPokemon(card=char, current_hp=330, attached_energies=[fire_e, fire_e]),
            prizes_remaining=4
        ),
        opponent_visible_state=VisibleOpponentState(
            prizes_remaining=5
        )
    )

    # 1. Evaluate board
    score = evaluator.score(state)
    print(f"\n[+] Composite Board State Score: {score:.2f}")

    # 2. Record game memory turn events
    game_mem = GameMemory()
    from src.memory.game_memory import TurnEvent
    game_mem.record_turn_event(TurnEvent(
        turn_number=3,
        player_index=0,
        action_type="ATTACK",
        description="Attack: Burning Darkness (180 DMG)",
        prizes_before=6,
        prizes_after=4,
        damage_dealt=180,
        energy_attached=True
    ))

    # 3. Record cross-game strategic match memory
    memory.record_game_result(own_archetype="Stage 2 Engine / Setup", opp_archetype="Aggressive / Turbo", won=True)
    memory.record_game_result(own_archetype="Stage 2 Engine / Setup", opp_archetype="Control / Disruption", won=False)
    memory.record_game_result(own_archetype="Stage 2 Engine / Setup", opp_archetype="Aggressive / Turbo", won=True)

    print("\n[+] Turn Event History Summary:")
    print(f"  • Own Prizes Taken: {game_mem.own_prizes_taken}")
    print(f"  • Recent Action: {game_mem.events[0].description}")

    print("\n[+] Strategic Cross-Game Memory Summary:")
    print(f"  • Total Games Played: {memory.total_games_played}")
    print(f"  • Overall Win Rate: {memory.get_overall_winrate() * 100:.1f}%")
    print(f"  • Win Rate vs 'Aggressive / Turbo': {memory.get_matchup_winrate('Stage 2 Engine / Setup', 'Aggressive / Turbo') * 100:.1f}%")

if __name__ == "__main__":
    run_notebook_03()
