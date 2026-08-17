"""
# Notebook 02: Bayesian Opponent Modeling & Belief Updates
PokéStrategist Research Suite

Demonstrates:
1. Dynamic Bayesian prior over 8 competitive archetypes
2. Step-by-step likelihood updates upon observing opponent cards
3. KO threat estimation & entropy tracking
"""

import os
import sys
sys.path.insert(0, os.path.abspath("."))

from src.opponent.opponent_model import OpponentModel
from src.schema import Card, CardCategory, PokemonStage
from src.deck.archetypes import ArchetypeCategory

def run_notebook_02():
    print("=" * 70)
    print("  PokéStrategist - Notebook 02: Bayesian Opponent Modeling")
    print("=" * 70)

    model = OpponentModel()
    print("\n[Step 0: Initial Uniform Belief Prior]")
    print(f"  Entropy: {model.belief.get_archetype_entropy():.3f} nats")
    for arch, prob in model.belief.archetype_probabilities.items():
        print(f"  • {arch:<26}: {prob*100:5.1f}%")

    # Step 1: Opponent drops Miraidon ex
    print("\n[Step 1: Opponent Plays 'Miraidon ex' (Aggressive / Turbo indicator)]")
    card1 = Card(
        id="SVI-081",
        name="Miraidon ex",
        expansion="SVI",
        collection_number="081",
        category=CardCategory.POKEMON,
        stage=PokemonStage.BASIC,
        hp=220,
        rule_box_text="ex rule: 2 prize cards"
    )
    model.observe_card_played(card1)
    print(f"  Entropy: {model.belief.get_archetype_entropy():.3f} nats")
    print(f"  Most Likely Archetype: {model.belief.get_most_likely_archetype()}")
    for arch, prob in sorted(model.belief.archetype_probabilities.items(), key=lambda x: x[1], reverse=True)[:4]:
        print(f"  • {arch:<26}: {prob*100:5.1f}%")

    # Step 2: Opponent attaches Lightning Energy & passes
    print("\n[Step 2: Opponent Attaches Lightning Energy & Plays Prime Catcher]")
    card2 = Card(id="TEF-157", name="Prime Catcher", expansion="TEF", collection_number="157", category=CardCategory.TRAINER)
    model.observe_card_played(card2)
    model.update_from_visible_state(hand_size=6, bench_size=3, active_energy_count=2, prizes_remaining=6, turn=2)
    print(f"  Estimated KO Threat Probability: {model.belief.estimated_ko_threat_prob * 100:.1f}%")
    print(f"  Most Likely Archetype: {model.belief.get_most_likely_archetype()}")
    for arch, prob in sorted(model.belief.archetype_probabilities.items(), key=lambda x: x[1], reverse=True)[:4]:
        print(f"  • {arch:<26}: {prob*100:5.1f}%")

if __name__ == "__main__":
    run_notebook_02()
