"""
PokéStrategist - Core Data Schema
Defines type-safe dataclasses for cards, attacks, abilities, game state,
actions, and belief representations for Pokémon TCG AI strategic planning.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Union

class CardCategory(str, Enum):
    POKEMON = "Pokemon"
    TRAINER = "Trainer"
    ENERGY = "Energy"
    UNKNOWN = "Unknown"

class PokemonStage(str, Enum):
    BASIC = "Basic"
    STAGE_1 = "Stage 1"
    STAGE_2 = "Stage 2"
    VSTAR = "VSTAR"
    VMAX = "VMAX"
    EX = "ex"
    NONE = "None"

class EnergyType(str, Enum):
    GRASS = "Grass"
    FIRE = "Fire"
    WATER = "Water"
    LIGHTNING = "Lightning"
    PSYCHIC = "Psychic"
    FIGHTING = "Fighting"
    DARKNESS = "Darkness"
    METAL = "Metal"
    DRAGON = "Dragon"
    COLORLESS = "Colorless"
    RAINBOW = "Rainbow"
    NONE = "None"

class TrainerType(str, Enum):
    SUPPORTER = "Supporter"
    ITEM = "Item"
    POKEMON_TOOL = "Pokemon Tool"
    STADIUM = "Stadium"
    NONE = "None"

class ActionType(str, Enum):
    ATTACK = "ATTACK"
    ATTACH_ENERGY = "ATTACH_ENERGY"
    EVOLVE = "EVOLVE"
    BENCH_BASIC = "BENCH_BASIC"
    PLAY_ITEM = "PLAY_ITEM"
    PLAY_SUPPORTER = "PLAY_SUPPORTER"
    ATTACH_TOOL = "ATTACH_TOOL"
    PLAY_STADIUM = "PLAY_STADIUM"
    USE_ABILITY = "USE_ABILITY"
    RETREAT = "RETREAT"
    PASS_TURN = "PASS_TURN"

@dataclass
class Attack:
    name: str
    energy_cost_str: str
    total_energy_cost: int
    energy_types: List[str]
    damage: int
    raw_damage_str: str = ""
    effect_text: str = ""
    has_secondary_effect: bool = False
    is_spread: bool = False
    is_bench_sniping: bool = False
    discards_energy: bool = False

@dataclass
class Ability:
    name: str
    effect_text: str
    is_once_per_turn: bool = True
    ability_type: str = "Engine" # Draw, Energy Accel, Search, Disruption, Passive

@dataclass
class StrategicFeatures:
    hp: int = 0
    max_damage: int = 0
    min_energy_cost: int = 0
    attack_efficiency: float = 0.0 # damage / energy
    survivability_index: float = 0.0 # hp / (retreat + 1)
    offensive_potential: float = 0.0 # max_damage * efficiency
    defensive_potential: float = 0.0 # hp - (retreat * 10)
    setup_requirement_score: int = 0 # 0 for Basic, 1 for Stage 1, 2 for Stage 2
    tempo_score: float = 0.0
    is_rule_box: bool = False
    prize_yield: int = 1 # 2 for ex/V, 1 for single-prize
    is_draw_supporter: bool = False

    @property
    def max_attack_damage(self) -> int:
        return self.max_damage

    @property
    def damage_to_cost_ratio(self) -> float:
        return self.attack_efficiency

    @property
    def durability_score(self) -> float:
        return float(self.hp)

@dataclass
class Card:
    id: str
    name: str
    expansion: str
    collection_number: str
    category: CardCategory
    stage: PokemonStage = PokemonStage.NONE
    previous_stage: Optional[str] = None
    hp: int = 0
    energy_type: EnergyType = EnergyType.NONE
    trainer_type: TrainerType = TrainerType.NONE
    rule_box_text: str = ""
    weakness_type: EnergyType = EnergyType.NONE
    weakness_multiplier: int = 2
    resistance_type: EnergyType = EnergyType.NONE
    resistance_value: int = 0
    retreat_cost: int = 0
    attacks: List[Attack] = field(default_factory=list)
    ability: Optional[Ability] = None
    synergy_tag: str = ""
    effect: str = ""
    features: Optional[StrategicFeatures] = None
    raw_dict: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_pokemon(self) -> bool:
        return self.category == CardCategory.POKEMON

    @property
    def is_trainer(self) -> bool:
        return self.category == CardCategory.TRAINER

    @property
    def is_energy(self) -> bool:
        return self.category == CardCategory.ENERGY

    @property
    def is_basic_pokemon(self) -> bool:
        return self.is_pokemon and (self.stage == PokemonStage.BASIC or self.stage == PokemonStage.NONE and not self.previous_stage)

@dataclass
class InPlayPokemon:
    card: Card
    current_hp: int
    attached_energies: List[Card] = field(default_factory=list)
    attached_tool: Optional[Card] = None
    damage_counters: int = 0
    status_conditions: List[str] = field(default_factory=list)
    turns_in_play: int = 0
    evolved_from: List[Card] = field(default_factory=list)

    @property
    def total_energy_count(self) -> int:
        count = 0
        for e in self.attached_energies:
            if "Double" in e.name or "Reversal" in e.name:
                count += 2
            else:
                count += 1
        return count

    @property
    def is_knocked_out(self) -> bool:
        return self.damage_counters * 10 >= self.card.hp or self.current_hp <= 0

@dataclass
class VisibleOpponentState:
    active: Optional[InPlayPokemon] = None
    bench: List[InPlayPokemon] = field(default_factory=list)
    hand_size: int = 7
    prizes_remaining: int = 6
    discard_pile: List[Card] = field(default_factory=list)
    lost_zone: List[Card] = field(default_factory=list)
    revealed_cards: List[Card] = field(default_factory=list)
    known_energy_count: int = 0
    supporter_played_this_turn: bool = False
    deck_count: int = 40
    hand_count: Optional[int] = None

    def __post_init__(self):
        if self.hand_count is not None:
            self.hand_size = self.hand_count

@dataclass
class PlayerState:
    active: Optional[InPlayPokemon] = None
    bench: List[InPlayPokemon] = field(default_factory=list)
    hand: List[Card] = field(default_factory=list)
    deck_count: int = 40
    discard_pile: List[Card] = field(default_factory=list)
    lost_zone: List[Card] = field(default_factory=list)
    prizes_remaining: int = 6
    supporter_played_this_turn: bool = False
    energy_attached_this_turn: bool = False
    stadium_in_play: Optional[Card] = None

@dataclass
class GameState:
    turn: int = 1
    active_player_index: int = 0 # 0: Self, 1: Opponent
    own_state: PlayerState = field(default_factory=PlayerState)
    opponent_visible_state: VisibleOpponentState = field(default_factory=VisibleOpponentState)
    game_phase: str = "MAIN" # SETUP, MAIN, ATTACK, BETWEEN_TURNS, TERMINAL
    legal_actions: List['Action'] = field(default_factory=list)
    action_history: List[str] = field(default_factory=list)
    is_terminal: bool = False
    winner: Optional[int] = None
    active_player: Optional[int] = None

    def __post_init__(self):
        if self.active_player is not None:
            self.active_player_index = self.active_player

@dataclass
class Action:
    action_type: ActionType
    card: Optional[Card] = None
    target_index: Optional[int] = None # Bench slot or target
    attack: Optional[Attack] = None
    energy_card: Optional[Card] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def describe(self) -> str:
        if self.action_type == ActionType.ATTACK and self.attack:
            return f"Attack with {self.attack.name} ({self.attack.damage} DMG)"
        elif self.action_type == ActionType.ATTACH_ENERGY and self.energy_card:
            return f"Attach {self.energy_card.name} to slot {self.target_index}"
        elif self.action_type == ActionType.EVOLVE and self.card:
            return f"Evolve slot {self.target_index} into {self.card.name}"
        elif self.action_type == ActionType.BENCH_BASIC and self.card:
            return f"Bench Basic {self.card.name}"
        elif self.action_type == ActionType.PLAY_SUPPORTER and self.card:
            return f"Play Supporter: {self.card.name}"
        elif self.action_type == ActionType.PLAY_ITEM and self.card:
            return f"Play Item: {self.card.name}"
        elif self.action_type == ActionType.RETREAT:
            return f"Retreat Active to bench slot {self.target_index}"
        elif self.action_type == ActionType.PASS_TURN:
            return "Pass Turn"
        return f"{self.action_type.value}"
