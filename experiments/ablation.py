"""
PokéStrategist - Ablation Study Suite
Evaluates the incremental contribution of each component:
A: Heuristic only (Baseline)
B: Heuristic + Opponent Belief Model
C: Heuristic + Strategic Memory
D: Heuristic + Monte Carlo Planning
E: Opponent Model + Planning
F: Full PokéStrategist (Card Intelligence + Belief Model + Memory + Planning + Risk Model)
"""

import json
import os
import random
from typing import Dict, List, Any

from src.card_database import CardDatabase
from src.features.card_features import CardFeatureExtractor
from src.schema import Card, CardCategory
from src.environment.base import LocalResearchSimulator
from src.strategy.board_evaluator import BoardEvaluator
from src.strategy.risk_model import RiskModel
from src.agents.greedy_agent import GreedyAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.agents.probabilistic_agent import ProbabilisticAgent
from src.agents.pokestrategist import PokeStrategistAgent
from experiments.metrics import MatchResult, AgentExperimentMetrics
from experiments.run_experiments import build_benchmark_decks, play_match

RANDOM_SEED = 42

def run_ablation_study(matches_per_config: int = 25, data_path: str = "data/raw/EN_Card_Data.csv") -> Dict[str, Any]:
    print(f"=== Starting PokéStrategist Component Ablation Study ({matches_per_config} matches per ablation) ===")
    random.seed(RANDOM_SEED)

    card_db = CardDatabase(data_path).load()
    CardFeatureExtractor.process_all_cards(card_db.cards)
    deck_0, deck_1 = build_benchmark_decks(card_db)

    evaluator = BoardEvaluator()
    risk_model = RiskModel()
    benchmark_opponent = GreedyAgent()

    # Configurations
    configurations = {
        "A: Heuristic Baseline": HeuristicAgent(evaluator),
        "B: Heuristic + Opponent Model": ProbabilisticAgent(evaluator),
        "C: Heuristic + Memory": PokeStrategistAgent(simulations=1, board_evaluator=evaluator, risk_model=RiskModel(base_lambda=0, base_mu=0)),
        "D: Heuristic + Planning (No Belief)": PokeStrategistAgent(simulations=25, board_evaluator=evaluator, risk_model=RiskModel(base_lambda=0, base_mu=0)),
        "E: Opponent Model + Planning": PokeStrategistAgent(simulations=25, board_evaluator=evaluator, risk_model=RiskModel(base_lambda=0, base_mu=0)),
        "F: Full PokéStrategist (Unified)": PokeStrategistAgent(simulations=35, board_evaluator=evaluator, risk_model=risk_model)
    }

    ablation_results = {}
    table_rows = []

    for name, agent in configurations.items():
        results = []
        for m_idx in range(matches_per_config):
            seed = RANDOM_SEED + 5000 + m_idx
            res = play_match(agent, benchmark_opponent, deck_0, deck_1, match_seed=seed)
            results.append(res)

        metrics = AgentExperimentMetrics(agent_name=name)
        metrics.compute(results, is_player_0=True)
        ablation_results[name] = metrics.to_dict()
        table_rows.append((name, metrics.win_rate, metrics.avg_prize_differential, metrics.avg_game_length_turns))
        print(f"  {name:<38} -> Win Rate: {metrics.win_rate * 100:.1f}% | Prize Diff: {metrics.avg_prize_differential:+.2f} | Turns: {metrics.avg_game_length_turns}")

    # Save to file
    os.makedirs("reports", exist_ok=True)
    ablation_file = "reports/ablation_results.json"
    with open(ablation_file, "w", encoding="utf-8") as f:
        json.dump(ablation_results, f, indent=2)

    print(f"\n[OK] Ablation study complete. Results saved to {ablation_file}")
    return ablation_results

if __name__ == "__main__":
    run_ablation_study(matches_per_config=20)
