"""
Unit Tests for PokéStrategist Forward Simulation Planner & Evaluator.
"""

import unittest
from src.card_database import CardDatabase
from src.features.card_features import CardFeatureExtractor
from src.schema import GameState, Action, ActionType, InPlayPokemon, PlayerState, VisibleOpponentState, Card, CardCategory, PokemonStage, Attack
from src.strategy.board_evaluator import BoardEvaluator
from src.planning.monte_carlo import MonteCarloPlanner
from src.strategy.risk_model import RiskModel

class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.evaluator = BoardEvaluator()
        self.planner = MonteCarloPlanner(self.evaluator, default_simulations=10)
        self.risk_model = RiskModel()

        # Dummy cards
        self.active_pkmn = Card(
            id="P-01",
            name="Charmander",
            expansion="TST",
            collection_number="1",
            category=CardCategory.POKEMON,
            stage=PokemonStage.BASIC,
            hp=70,
            attacks=[Attack(name="Ember", energy_cost_str="[Fire]", total_energy_cost=1, energy_types=["Fire"], damage=30)]
        )
        self.opp_pkmn = Card(
            id="P-02",
            name="Squirtle",
            expansion="TST",
            collection_number="2",
            category=CardCategory.POKEMON,
            stage=PokemonStage.BASIC,
            hp=60,
            attacks=[Attack(name="Water Gun", energy_cost_str="[Water]", total_energy_cost=1, energy_types=["Water"], damage=20)]
        )
        self.fire_energy = Card(
            id="E-01",
            name="Fire Energy",
            expansion="TST",
            collection_number="3",
            category=CardCategory.ENERGY
        )

        self.state = GameState(
            turn=1,
            active_player=0,
            own_state=PlayerState(
                active=InPlayPokemon(card=self.active_pkmn, current_hp=70),
                bench=[],
                hand=[self.fire_energy],
                deck_count=40,
                discard_pile=[],
                prizes_remaining=6
            ),
            opponent_visible_state=VisibleOpponentState(
                active=InPlayPokemon(card=self.opp_pkmn, current_hp=60),
                bench=[],
                hand_count=5,
                deck_count=40,
                discard_pile=[],
                prizes_remaining=6
            )
        )

    def test_board_evaluator_scoring(self):
        score = self.evaluator.score(self.state)
        self.assertIsInstance(score, (int, float))

    def test_monte_carlo_planner(self):
        candidate_actions = [
            Action(action_type=ActionType.ATTACH_ENERGY, target_index=-1, energy_card=self.fire_energy),
            Action(action_type=ActionType.PASS_TURN)
        ]
        results = self.planner.plan(self.state, candidate_actions, num_simulations=10)
        self.assertEqual(len(results), 2)
        self.assertIn("expected_utility", results[0])
        self.assertGreaterEqual(results[0]["expected_utility"], results[1]["expected_utility"])

    def test_risk_model_calculation(self):
        breakdown = self.risk_model.compute_risk_adjusted_score(
            expected_utility=150.0,
            state=self.state,
            action=Action(action_type=ActionType.PASS_TURN),
            opp_threat_prob=0.8
        )
        self.assertIn("final_score", breakdown)
        self.assertIn("risk_penalty", breakdown)
        self.assertIn("future_value_bonus", breakdown)

if __name__ == "__main__":
    unittest.main()
