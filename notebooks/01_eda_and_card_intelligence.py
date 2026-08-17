"""
# Notebook 01: Exploratory Data Analysis & Card Intelligence Pipeline
PokéStrategist Research Suite

Demonstrates:
1. Loading the 1,500+ standard-legal Pokémon TCG dataset
2. Distribution of card categories, stages, energy types, and retreat costs
3. Extraction of derived features (survivability, damage efficiency, offensive potential, tempo)
"""

import os
import sys
sys.path.insert(0, os.path.abspath("."))

from src.card_database import CardDatabase
from src.features.card_features import CardFeatureExtractor
from src.schema import CardCategory, EnergyType, PokemonStage

def run_notebook_01():
    print("=" * 70)
    print("  PokéStrategist - Notebook 01: EDA & Card Intelligence")
    print("=" * 70)

    # 1. Load Dataset
    db = CardDatabase("data/raw/EN_Card_Data.csv").load()
    print(f"\n[+] Total Cards Loaded: {len(db)}")

    # 2. Extract Strategic Features
    features_dict = CardFeatureExtractor.process_all_cards(db.cards)
    print(f"[+] Feature Extraction Complete for {len(features_dict)} Cards")

    # 3. Categorical Distributions
    pokemon_cards = db.search(category=CardCategory.POKEMON)
    trainer_cards = db.search(category=CardCategory.TRAINER)
    energy_cards = db.search(category=CardCategory.ENERGY)
    basics = db.get_basic_pokemon()

    print("\n--- Card Category Breakdown ---")
    print(f"  • Pokémon Cards: {len(pokemon_cards)} ({len(pokemon_cards)/len(db)*100:.1f}%)")
    print(f"  • Trainer Cards: {len(trainer_cards)} ({len(trainer_cards)/len(db)*100:.1f}%)")
    print(f"  • Energy Cards:  {len(energy_cards)} ({len(energy_cards)/len(db)*100:.1f}%)")
    print(f"  • Basic Pokémon: {len(basics)}")

    # 4. Top Attack Efficiency Rankings
    print("\n--- Top 5 Energy-Efficient Attackers ---")
    scored_pokemon = [p for p in pokemon_cards if p.features and p.features.max_damage > 0]
    scored_pokemon.sort(key=lambda p: p.features.attack_efficiency if p.features else 0, reverse=True)
    
    for rank, p in enumerate(scored_pokemon[:5], 1):
        f = p.features
        print(f"  {rank}. {p.name:<24} | Max DMG: {f.max_damage:<3} | Eff: {f.attack_efficiency:<5.1f} | HP: {p.hp:<3} | RuleBox: {f.is_rule_box}")

    # 5. Top Durability / Survivability Rankings
    print("\n--- Top 5 Survivability Index (HP vs Retreat vs Prize) ---")
    scored_pokemon.sort(key=lambda p: p.features.survivability_index if p.features else 0, reverse=True)
    for rank, p in enumerate(scored_pokemon[:5], 1):
        f = p.features
        print(f"  {rank}. {p.name:<24} | HP: {p.hp:<3} | Retreat: {p.retreat_cost} | Prize Yield: {f.prize_yield} | Survivability: {f.survivability_index}")

if __name__ == "__main__":
    run_notebook_01()
