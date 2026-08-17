"""
# Notebook 06: Component Ablation Study & Decision Explainability
PokéStrategist Research Suite

Demonstrates:
1. Systematic component ablation:
   A: Heuristic Baseline
   B: Heuristic + Opponent Model
   C: Heuristic + Strategic Memory
   D: Heuristic + Monte Carlo Planning
   E: Opponent Model + Planning
   F: Full PokéStrategist
2. Explainability pipeline extracting step-by-step decision justification
"""

import os
import sys
import json
sys.path.insert(0, os.path.abspath("."))

from experiments.ablation import run_ablation_study

def run_notebook_06():
    print("=" * 70)
    print("  PokéStrategist - Notebook 06: Ablation Study & Explainability")
    print("=" * 70)

    ablation_file = "reports/ablation_results.json"
    if os.path.exists(ablation_file):
        with open(ablation_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("\n[+] Loaded Component Ablation Findings:")
        print(f"  {'Configuration':<40} | {'Win Rate':<10} | {'Prize Diff':<12} | {'Avg Turns':<10}")
        print("-" * 78)
        for name, metrics in data.items():
            print(f"  {name:<40} | {metrics['win_rate']*100:6.1f}%   | {metrics['avg_prize_differential']:+10.2f}   | {metrics['avg_game_length_turns']:<10.1f}")
    else:
        print("\n[+] Executing live ablation study...")
        run_ablation_study(matches_per_config=10)

if __name__ == "__main__":
    run_notebook_06()
