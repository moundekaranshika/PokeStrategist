"""
PokéStrategist - Data Loader & Inspection Engine
Loads, diagnoses, normalizes, and validates Pokémon TCG card CSVs.
Robust against differing column header naming conventions and missing values.
"""

import csv
import logging
import os
import re
from typing import Dict, List, Optional, Tuple, Any

from src.schema import Card, Attack, Ability, CardCategory, PokemonStage, EnergyType, TrainerType

logger = logging.getLogger("PokéStrategist.DataLoader")

COLUMN_SYNONYMS = {
    "id": ["card id", "id", "card_id", "number", "cardnumber", "card_no"],
    "name": ["card name", "name", "card_name", "pokemon name", "title"],
    "expansion": ["expansion", "set", "set name", "set_name", "series"],
    "collection_number": ["collection number", "card number", "number in set", "num"],
    "category": ["category", "supertype", "card type", "type_of_card"],
    "stage": ["pokemon stage", "stage", "evolution stage", "sub_type", "subtype"],
    "previous_stage": ["previous stage", "evolves from", "evolves_from", "pre_evolution"],
    "hp": ["hp", "hit points", "health", "max hp"],
    "energy_type": ["energy type", "type", "element", "color", "pokemon type"],
    "trainer_type": ["trainer type", "sub type", "trainer category", "item type"],
    "rule": ["rule", "rule box", "rules", "special rule", "card rule"],
    "weakness": ["weakness", "weak", "weakness type"],
    "resistance": ["resistance", "resist", "resistance type"],
    "retreat_cost": ["retreat cost", "retreat", "retreat energy", "retreat_cost"],
    "m1_name": ["move 1 name", "move 1", "attack 1", "attack 1 name", "m1 name", "attack name 1"],
    "m1_cost": ["move 1 energy cost", "move 1 cost", "attack 1 cost", "attack 1 energy", "m1 cost"],
    "m1_dmg": ["move 1 damage", "move 1 dmg", "attack 1 damage", "attack 1 dmg", "m1 dmg"],
    "m1_eff": ["move 1 effect", "move 1 text", "attack 1 effect", "attack 1 description", "m1 effect"],
    "m2_name": ["move 2 name", "move 2", "attack 2", "attack 2 name", "m2 name", "attack name 2"],
    "m2_cost": ["move 2 energy cost", "move 2 cost", "attack 2 cost", "attack 2 energy", "m2 cost"],
    "m2_dmg": ["move 2 damage", "move 2 dmg", "attack 2 damage", "attack 2 dmg", "m2 dmg"],
    "m2_eff": ["move 2 effect", "move 2 text", "attack 2 effect", "attack 2 description", "m2 effect"],
    "ability_name": ["ability name", "ability", "poke-power", "poke-body", "vstar power"],
    "ability_eff": ["ability effect", "ability text", "ability description"],
    "synergy_tag": ["explanation / synergy tag", "explanation", "synergy", "notes", "tags"]
}

class DataLoader:
    def __init__(self, data_path: str = "data/raw/EN_Card_Data.csv"):
        self.data_path = data_path
        self.raw_rows: List[Dict[str, str]] = []
        self.column_map: Dict[str, str] = {}
        self.inspection_report: Dict[str, Any] = {}

    def inspect_csv(self) -> Dict[str, Any]:
        """
        Inspects the CSV file, checking shape, column names, missing values,
        and suitability for strategic feature extraction.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Card dataset not found at path: {self.data_path}")

        with open(self.data_path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            raw_columns = reader.fieldnames or []
            rows = list(reader)

        self.raw_rows = rows
        total_rows = len(rows)
        total_cols = len(raw_columns)

        # Identify column mapping
        col_map = {}
        lowered_cols = {col.strip().lower(): col for col in raw_columns}
        for canonical_key, synonyms in COLUMN_SYNONYMS.items():
            for syn in synonyms:
                if syn in lowered_cols:
                    col_map[canonical_key] = lowered_cols[syn]
                    break
        self.column_map = col_map

        # Calculate missing values per column
        missing_counts = {}
        for col in raw_columns:
            empty_count = sum(1 for r in rows if not r.get(col) or str(r.get(col)).strip() in ["", "nan", "None", "null", "N/A"])
            missing_counts[col] = {
                "missing_count": empty_count,
                "missing_percentage": round((empty_count / max(1, total_rows)) * 100, 2)
            }

        # Check strategic feature extraction viability
        has_hp = "hp" in col_map
        has_attacks = "m1_name" in col_map or "m1_dmg" in col_map
        has_energy_cost = "m1_cost" in col_map
        has_category = "category" in col_map or "stage" in col_map

        strategic_suitability = {
            "can_extract_hp": has_hp,
            "can_extract_damage": has_attacks,
            "can_extract_energy_efficiency": has_attacks and has_energy_cost,
            "can_extract_evolution_tree": "previous_stage" in col_map or "stage" in col_map,
            "can_extract_trainers": "category" in col_map or "trainer_type" in col_map,
            "can_extract_weakness_resistance": "weakness" in col_map and "resistance" in col_map,
            "overall_strategic_grade": "HIGH (Full Competitive Modeling Ready)" if (has_hp and has_attacks and has_energy_cost) else "PARTIAL"
        }

        self.inspection_report = {
            "file_path": self.data_path,
            "shape": (total_rows, total_cols),
            "columns": raw_columns,
            "detected_mappings": col_map,
            "missing_values": missing_counts,
            "representative_sample_10": rows[:10],
            "strategic_suitability": strategic_suitability
        }
        return self.inspection_report

    def load_cards(self) -> List[Card]:
        """Loads and normalizes rows into structured Card instances."""
        if not self.raw_rows:
            self.inspect_csv()

        cards: List[Card] = []
        for row in self.raw_rows:
            card = self._parse_card_row(row)
            if card:
                cards.append(card)
        return cards

    def _parse_card_row(self, row: Dict[str, str]) -> Optional[Card]:
        def get_val(canonical: str, default: str = "") -> str:
            col_name = self.column_map.get(canonical)
            if col_name and col_name in row:
                v = row[col_name]
                return str(v).strip() if v is not None else default
            return default

        name = get_val("name")
        if not name:
            return None

        card_id = get_val("id", f"CRD-{abs(hash(name)) % 1000000}")
        expansion = get_val("expansion", "Standard Set")
        coll_num = get_val("collection_number", "001/100")
        
        # Category normalization
        raw_cat = get_val("category", "").lower()
        if "pokemon" in raw_cat or "pokémon" in raw_cat:
            cat = CardCategory.POKEMON
        elif "trainer" in raw_cat:
            cat = CardCategory.TRAINER
        elif "energy" in raw_cat:
            cat = CardCategory.ENERGY
        else:
            # Fallback deduction
            if get_val("hp") or get_val("stage") or get_val("m1_name"):
                cat = CardCategory.POKEMON
            elif "energy" in name.lower():
                cat = CardCategory.ENERGY
            else:
                cat = CardCategory.TRAINER

        # Stage normalization
        raw_stage = get_val("stage", "").lower()
        if "basic" in raw_stage:
            stage = PokemonStage.BASIC
        elif "stage 1" in raw_stage or "stage-1" in raw_stage:
            stage = PokemonStage.STAGE_1
        elif "stage 2" in raw_stage or "stage-2" in raw_stage:
            stage = PokemonStage.STAGE_2
        elif "vstar" in raw_stage or "vstar" in name.lower():
            stage = PokemonStage.VSTAR
        elif "vmax" in raw_stage or "vmax" in name.lower():
            stage = PokemonStage.VMAX
        elif "ex" in raw_stage or " ex" in name.lower():
            stage = PokemonStage.EX
        else:
            stage = PokemonStage.BASIC if cat == CardCategory.POKEMON else PokemonStage.NONE

        # HP parsing
        raw_hp = get_val("hp", "0")
        try:
            hp_num = int(re.sub(r"[^\d]", "", raw_hp)) if raw_hp else 0
        except ValueError:
            hp_num = 0

        # Energy Type parsing
        raw_type = get_val("energy_type", "Colorless").capitalize()
        try:
            energy_type = EnergyType(raw_type)
        except ValueError:
            energy_type = EnergyType.COLORLESS

        # Trainer Type parsing
        raw_trainer_type = get_val("trainer_type", "").lower()
        if "supporter" in raw_trainer_type:
            trainer_type = TrainerType.SUPPORTER
        elif "tool" in raw_trainer_type:
            trainer_type = TrainerType.POKEMON_TOOL
        elif "stadium" in raw_trainer_type:
            trainer_type = TrainerType.STADIUM
        elif "item" in raw_trainer_type or cat == CardCategory.TRAINER:
            trainer_type = TrainerType.ITEM
        else:
            trainer_type = TrainerType.NONE

        # Weakness / Resistance
        raw_weak = get_val("weakness", "None")
        weak_type = EnergyType.NONE
        for t in EnergyType:
            if t.value != "None" and t.value.lower() in raw_weak.lower():
                weak_type = t
                break

        raw_res = get_val("resistance", "None")
        res_type = EnergyType.NONE
        res_val = 0
        for t in EnergyType:
            if t.value != "None" and t.value.lower() in raw_res.lower():
                res_type = t
                res_val = -30
                break

        # Retreat Cost
        raw_retreat = get_val("retreat_cost", "0")
        try:
            retreat = int(re.sub(r"[^\d]", "", raw_retreat)) if raw_retreat else 0
        except ValueError:
            retreat = 0

        # Parse attacks
        attacks: List[Attack] = []
        for m_prefix in ["m1", "m2"]:
            m_name = get_val(f"{m_prefix}_name")
            if m_name:
                cost_str = get_val(f"{m_prefix}_cost", "1 C")
                dmg_str = get_val(f"{m_prefix}_dmg", "0")
                eff_str = get_val(f"{m_prefix}_eff", "")

                # Parse damage value
                dmg_digits = re.findall(r"\d+", dmg_str)
                dmg_val = int(dmg_digits[0]) if dmg_digits else 0

                # Count total energy
                cost_digits = re.findall(r"\d+", cost_str)
                total_cost = sum(int(d) for d in cost_digits) if cost_digits else max(1, len(cost_str.split()))

                attacks.append(Attack(
                    name=m_name,
                    energy_cost_str=cost_str,
                    total_energy_cost=total_cost,
                    energy_types=[energy_type.value],
                    damage=dmg_val,
                    raw_damage_str=dmg_str,
                    effect_text=eff_str,
                    has_secondary_effect=bool(eff_str),
                    is_spread="to each of your opponent's" in eff_str.lower(),
                    is_bench_sniping="benched pokemon" in eff_str.lower() or "bench" in eff_str.lower(),
                    discards_energy="discard" in eff_str.lower() and "energy" in eff_str.lower()
                ))

        # Ability
        ability_name = get_val("ability_name")
        ability_eff = get_val("ability_eff")
        ability = Ability(name=ability_name, effect_text=ability_eff) if ability_name else None

        return Card(
            id=card_id,
            name=name,
            expansion=expansion,
            collection_number=coll_num,
            category=cat,
            stage=stage,
            previous_stage=get_val("previous_stage") or None,
            hp=hp_num,
            energy_type=energy_type,
            trainer_type=trainer_type,
            rule_box_text=get_val("rule"),
            weakness_type=weak_type,
            weakness_multiplier=2,
            resistance_type=res_type,
            resistance_value=res_val,
            retreat_cost=retreat,
            attacks=attacks,
            ability=ability,
            synergy_tag=get_val("synergy_tag"),
            raw_dict=row
        )
