"""
# Notebook 04: Monte Carlo Forward Simulation & Risk-Aware Utility Optimization
PokéStrategist Research Suite

Demonstrates:
1. Monte Carlo forward rollouts across stochastic candidate action branches
2. Risk model penalty calculation under inferred opponent threat
3. Full decision trace extraction and human-readable explanation
"""

import os
import sys
sys.path.insert(0, os.path.abspath("."))

from src.schema import GameState, PlayerState, VisibleOpponentState, InPlayPokemon, Card, CardCategory, PokemonStage, Attack, Action, ActionType
from src.strategy.board_evaluator import BoardEvaluator
from src.planning.monte_carlo import MonteCarloPlanner
from src.strategy.risk_model import RiskModel
from src.opponent.opponent_model import OpponentModel

def run_notebook_04():
    print("=" * 70)
    print("  PokéStrategist - Notebook 04: Monte Carlo & Risk Optimization")
    print("=" * 70)

    evaluator = BoardEvaluator()
    planner = MonteCarloPlanner(evaluator, default_simulations=50)
    risk_model = RiskModel()
    opp_model = OpponentModel()

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
    opp_mon = Card(
        id="SVI-081",
        name="Miraidon ex",
        expansion="SVI",
        collection_number="081",
        category=CardCategory.POKEMON,
        stage=PokemonStage.BASIC,
        hp=220,
        rule_box_text="ex rule"
    )
    fire_e = Card(id="SVI-E01", name="Fire Energy", expansion="SVI", collection_number="E01", category=CardCategory.ENERGY)

    state = GameState(
        turn=2,
        own_state=PlayerState(
            active=InPlayPokemon(card=char, current_hp=330, attached_energies=[fire_e, fire_e]),
            hand=[fire_e],
            prizes_remaining=6
        ),
        opponent_visible_state=VisibleOpponentState(
            active=InPlayPokemon(card=opp_mon, current_hp=220),
            prizes_remaining=6
        )
    )

    candidate_actions = [
        Action(action_type=ActionType.ATTACK, attack=char.attacks[0]),
        Action(action_type=ActionType.ATTACH_ENERGY, target_index=-1, energy_card=fire_e),
        Action(action_type=ActionType.PASS_TURN)
    ]

    print(f"\n[+] Running {len(candidate_actions)} Monte Carlo Rollout Branches (N=50 per action)...")
    plan_results = planner.plan(state, candidate_actions, belief=opp_model.belief, num_simulations=50)

    print("\n--- Monte Carlo Expected Utility Rankings ---")
    for res in plan_results:
        breakdown = risk_model.compute_risk_adjusted_score(
            expected_utility=res["expected_utility"],
            state=state,
            action=res["action"],
            opp_threat_prob=opp_model.belief.estimated_ko_threat_prob
        )
        print(f"  Action: {res['description']}")
        print(f"    • Raw Expected Utility (EU): {res['expected_utility']:+.2f} (StdDev: ±{res['std_dev']:.2f})")
        print(f"    • Risk Penalty:              -{breakdown['risk_penalty']:.2f}")
        print(f"    • Future Value Bonus:        +{breakdown['future_value_bonus']:.2f}")
        print(f"    • Final Composite Score:      {breakdown['final_score']:+.2f}\n")

if __name__ == "__main__":
    run_notebook_04()
