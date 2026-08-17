"""
PokéStrategist - Tournament Experiment Runner
Executes reproducible, head-to-head tournament trials between all 5 agent architectures
using the LocalResearchSimulator under controlled seeds.
"""

import time
import json
import os
import random
from typing import Dict, List, Any

from src.card_database import CardDatabase
from src.features.card_features import CardFeatureExtractor
from src.schema import Card, CardCategory, PokemonStage
from src.environment.base import LocalResearchSimulator
from src.agents.random_agent import RandomAgent
from src.agents.greedy_agent import GreedyAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.agents.probabilistic_agent import ProbabilisticAgent
from src.agents.pokestrategist import PokeStrategistAgent
from experiments.metrics import MatchResult, AgentExperimentMetrics

RANDOM_SEED = 42

def build_benchmark_decks(card_db: CardDatabase) -> tuple[List[Card], List[Card]]:
    """Builds two balanced competitive standard decks from the card database."""
    all_basics = card_db.get_basic_pokemon()
    all_trainers = card_db.search(category=CardCategory.TRAINER)
    all_energies = card_db.search(category=CardCategory.ENERGY)

    # Deck 0: Fire/Dragon Setup Line
    d0_p = [c for c in all_basics if c.energy_type.value in ["Fire", "Dragon", "Colorless"]][:12]
    d0_t = all_trainers[:32]
    d0_e = all_energies[:16]
    deck_0 = (d0_p + d0_t + d0_e)[:60]

    # Deck 1: Water/Lightning Aggressive Line
    d1_p = [c for c in all_basics if c.energy_type.value in ["Water", "Lightning", "Psychic"]][:12]
    d1_t = all_trainers[:32]
    d1_e = all_energies[:16]
    deck_1 = (d1_p + d1_t + d1_e)[:60]

    return deck_0, deck_1

def play_match(agent_0, agent_1, deck_0: List[Card], deck_1: List[Card], match_seed: int) -> MatchResult:
    """Plays a single full match between two agents in the local research simulator."""
    env = LocalResearchSimulator(deck_0, deck_1)
    state = env.reset(seed=match_seed)
    
    if hasattr(agent_0, "reset_game"):
        agent_0.reset_game()
    if hasattr(agent_1, "reset_game"):
        agent_1.reset_game()

    start_time = time.time()
    p0_dmg = 0
    p1_dmg = 0
    p0_actions = 0

    while not env.is_terminal():
        # Agent 0 Turn
        action = agent_0.select_action(state)
        p0_actions += 1
        state, reward, is_term, info = env.step(action)
        if action.attack:
            p0_dmg += action.attack.damage

        if is_term:
            break

    elapsed = time.time() - start_time
    winner = state.winner if state.winner is not None else -1

    return MatchResult(
        winner=winner,
        turns_taken=state.turn,
        p0_prizes_left=state.own_state.prizes_remaining,
        p1_prizes_left=state.opponent_visible_state.prizes_remaining,
        p0_total_damage=p0_dmg,
        p1_total_damage=p1_dmg,
        p0_actions_count=p0_actions,
        execution_time_sec=round(elapsed, 3)
    )

def run_tournament(matches_per_pair: int = 20, data_path: str = "data/raw/EN_Card_Data.csv") -> Dict[str, Any]:
    print(f"=== Starting PokéStrategist Benchmark Tournament ({matches_per_pair} matches per pairing) ===")
    random.seed(RANDOM_SEED)

    card_db = CardDatabase(data_path).load()
    CardFeatureExtractor.process_all_cards(card_db.cards)
    deck_0, deck_1 = build_benchmark_decks(card_db)

    agents = [
        RandomAgent(seed=RANDOM_SEED),
        GreedyAgent(),
        HeuristicAgent(),
        ProbabilisticAgent(),
        PokeStrategistAgent(simulations=25)
    ]

    results_matrix = {}
    metrics_summary = {}

    for i, a0 in enumerate(agents):
        for j, a1 in enumerate(agents):
            if i == j:
                continue
            pair_key = f"{a0.name} vs {a1.name}"
            match_results = []
            for m_idx in range(matches_per_pair):
                m_seed = RANDOM_SEED + (i * 1000) + (j * 100) + m_idx
                res = play_match(a0, a1, deck_0, deck_1, match_seed=m_seed)
                match_results.append(res)

            metrics = AgentExperimentMetrics(agent_name=a0.name)
            metrics.compute(match_results, is_player_0=True)
            results_matrix[pair_key] = metrics.to_dict()
            print(f"  {pair_key:<36} -> Win Rate: {metrics.win_rate * 100:.1f}% | Avg Prize Diff: {metrics.avg_prize_differential:+.2f}")

    # Aggregated performance per agent against all baselines
    for a in agents:
        agent_matches = []
        for pair_key, data in results_matrix.items():
            if pair_key.startswith(f"{a.name} vs"):
                agent_matches.append(data["win_rate"])
        avg_wr = sum(agent_matches) / max(1, len(agent_matches))
        metrics_summary[a.name] = {
            "overall_win_rate": round(avg_wr, 3),
            "pairings": {k: v for k, v in results_matrix.items() if k.startswith(f"{a.name} vs")}
        }

    os.makedirs("reports", exist_ok=True)
    report_path = "reports/tournament_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)

    print(f"\n[OK] Benchmark completed. Saved full results to {report_path}")
    return metrics_summary

if __name__ == "__main__":
    run_tournament(matches_per_pair=15)
