"""
# Notebook 05: Head-to-Head Tournament & Multi-Agent Benchmarking
PokéStrategist Research Suite

Demonstrates:
1. Tournament matrix execution across Random, Greedy, Heuristic, Probabilistic, and PokéStrategist
2. Match analytics, win rates, game length in turns, and prize differentials
"""

import os
import sys
import json
sys.path.insert(0, os.path.abspath("."))

from experiments.run_experiments import run_tournament

def run_notebook_05():
    print("=" * 70)
    print("  PokéStrategist - Notebook 05: Tournament Benchmarking")
    print("=" * 70)

    # Check if results already exist or run quick demo
    results_path = "reports/tournament_results.json"
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("\n[+] Loaded Existing Tournament Results:")
        for agent, summary in data.items():
            print(f"\n  === {agent} (Overall Win Rate: {summary['overall_win_rate']*100:.1f}%) ===")
            for pair, metrics in summary["pairings"].items():
                print(f"    vs {metrics['agent_name']}: WR {metrics['win_rate']*100:5.1f}% | Avg Prize Diff: {metrics['avg_prize_differential']:+.2f} | Avg Turns: {metrics['avg_game_length_turns']}")
    else:
        print("\n[+] Running live tournament benchmark...")
        run_tournament(matches_per_pair=5)

if __name__ == "__main__":
    run_notebook_05()
