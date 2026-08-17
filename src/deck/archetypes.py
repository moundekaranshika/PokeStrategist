"""
PokéStrategist - Deck Archetypes Definition
Defines strategic archetype profiles and feature weighting rules.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List

class ArchetypeCategory(str, Enum):
    AGGRESSIVE = "Aggressive / Turbo"
    SETUP_EVOLUTION = "Setup / Evolution"
    ENERGY_ACCELERATION = "Energy Acceleration"
    DEFENSIVE = "Defensive / Tank"
    CONTROL_DISRUPTION = "Control / Disruption"
    CONTROL_STALL = "Control / Disruption"
    SINGLE_TARGET_BURST = "Single-Target Burst"
    SPREAD_SNIPER = "Spread / Bench Snipe"
    RESOURCE_DENIAL = "Resource Denial"
    BALANCED = "Balanced Midrange"

@dataclass
class ArchetypeProfile:
    name: ArchetypeCategory
    description: str
    key_indicators: List[str]
    ideal_energy_ratio: float # e.g. 0.20 (12/60)
    ideal_trainer_ratio: float # e.g. 0.55 (33/60)
    ideal_pokemon_ratio: float # e.g. 0.25 (15/60)
    expected_turn_to_attack: int
    risk_tolerance: float # 0.0 (conservative) to 1.0 (aggressive)

ARCHETYPE_PROFILES = {
    ArchetypeCategory.AGGRESSIVE: ArchetypeProfile(
        name=ArchetypeCategory.AGGRESSIVE,
        description="Aims for quick 1-2 turn knockouts using high early tempo and basic multi-prize attackers.",
        key_indicators=["Miraidon", "Iron Hands", "Roaring Moon", "Battle VIP Pass", "Prime Catcher"],
        ideal_energy_ratio=0.22,
        ideal_trainer_ratio=0.53,
        ideal_pokemon_ratio=0.25,
        expected_turn_to_attack=1,
        risk_tolerance=0.8
    ),
    ArchetypeCategory.SETUP_EVOLUTION: ArchetypeProfile(
        name=ArchetypeCategory.SETUP_EVOLUTION,
        description="Sacrifices early prizes to build massive Stage 2 engines (e.g. Charizard ex, Gardevoir ex, Pidgeot ex).",
        key_indicators=["Rare Candy", "Buddy-Buddy Poffin", "Kirlia", "Pidgeot", "Charizard", "Gardevoir"],
        ideal_energy_ratio=0.18,
        ideal_trainer_ratio=0.57,
        ideal_pokemon_ratio=0.25,
        expected_turn_to_attack=2,
        risk_tolerance=0.5
    ),
    ArchetypeCategory.ENERGY_ACCELERATION: ArchetypeProfile(
        name=ArchetypeCategory.ENERGY_ACCELERATION,
        description="Floods the board with energy via abilities (Baxcalibur, Archeops, Dark Patch, Magma Basin).",
        key_indicators=["Baxcalibur", "Dark Patch", "Superior Energy Retrieval", "Earthen Vessel"],
        ideal_energy_ratio=0.25,
        ideal_trainer_ratio=0.55,
        ideal_pokemon_ratio=0.20,
        expected_turn_to_attack=2,
        risk_tolerance=0.6
    ),
    ArchetypeCategory.DEFENSIVE: ArchetypeProfile(
        name=ArchetypeCategory.DEFENSIVE,
        description="High HP tank Pokémon utilizing healing, damage reduction tools, and defensive walls.",
        key_indicators=["Rigid Band", "Full Metal Lab", "Hero's Cape", "Cheren's Care", "Goodra", "Blissey"],
        ideal_energy_ratio=0.22,
        ideal_trainer_ratio=0.58,
        ideal_pokemon_ratio=0.20,
        expected_turn_to_attack=2,
        risk_tolerance=0.35
    ),
    ArchetypeCategory.CONTROL_DISRUPTION: ArchetypeProfile(
        name=ArchetypeCategory.CONTROL_DISRUPTION,
        description="Deprives opponent of resources, locks abilities, and controls hand size (Iono, Path to Peak).",
        key_indicators=["Iono", "Judge", "Path to the Peak", "Counter Catcher", "Technical Machine: Devolution"],
        ideal_energy_ratio=0.15,
        ideal_trainer_ratio=0.65,
        ideal_pokemon_ratio=0.20,
        expected_turn_to_attack=3,
        risk_tolerance=0.3
    ),
    ArchetypeCategory.SINGLE_TARGET_BURST: ArchetypeProfile(
        name=ArchetypeCategory.SINGLE_TARGET_BURST,
        description="Focuses on 280-330 damage one-hit knockouts against active multi-prize Pokémon.",
        key_indicators=["Maximum Belt", "Choice Belt", "Giratina", "Charizard ex", "Gholdengo"],
        ideal_energy_ratio=0.20,
        ideal_trainer_ratio=0.55,
        ideal_pokemon_ratio=0.25,
        expected_turn_to_attack=2,
        risk_tolerance=0.65
    ),
    ArchetypeCategory.SPREAD_SNIPER: ArchetypeProfile(
        name=ArchetypeCategory.SPREAD_SNIPER,
        description="Distributes damage counters across benched support Pokémon (Comfey, Sableye, Greninja).",
        key_indicators=["Comfey", "Sableye", "Radiant Greninja", "Colress", "Mirage Gate"],
        ideal_energy_ratio=0.18,
        ideal_trainer_ratio=0.62,
        ideal_pokemon_ratio=0.20,
        expected_turn_to_attack=2,
        risk_tolerance=0.55
    ),
    ArchetypeCategory.RESOURCE_DENIAL: ArchetypeProfile(
        name=ArchetypeCategory.RESOURCE_DENIAL,
        description="Stalls until opponent runs out of cards or energy, preventing attacks through immunities.",
        key_indicators=["Snorlax", "Penny", "Neutral Center", "Collapsed Stadium", "Super Rod"],
        ideal_energy_ratio=0.10,
        ideal_trainer_ratio=0.70,
        ideal_pokemon_ratio=0.20,
        expected_turn_to_attack=4,
        risk_tolerance=0.2
    ),
    ArchetypeCategory.BALANCED: ArchetypeProfile(
        name=ArchetypeCategory.BALANCED,
        description="Standard tournament midrange build with flexible search engines, consistent draw, and resilient attackers.",
        key_indicators=["Ultra Ball", "Nest Ball", "Professor's Research", "Boss's Orders", "Super Rod"],
        ideal_energy_ratio=0.20,
        ideal_trainer_ratio=0.55,
        ideal_pokemon_ratio=0.25,
        expected_turn_to_attack=2,
        risk_tolerance=0.5
    )
}
