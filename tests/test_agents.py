"""
Unit Tests for PokéStrategist Baseline Agents and Flagship System.
"""

import unittest
from src.card_database import CardDatabase
from src.features.card_features import CardFeatureExtractor
from src.schema import GameState, Action, ActionType, InPlayPokemon, PlayerState, VisibleOpponentState, Card, CardCategory, PokemonStage, Attack
from src.agents.random_agent import RandomAgent
from src.agents.greedy_agent import GreedyAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.agents.probabilistic_agent import ProbabilisticAgent
from src.agents.pokestrategist import PokeStrategistAgent

class TestAgents(unittest.TestCase):
    def setUp(self):
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
                active=InPlayPokemon(card=self.active_pkmn, current_hp=70, attached_energies=[self.fire_energy]),
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

    def test_random_agent_selects_action(self):
        agent = RandomAgent(seed=42)
        action = agent.select_action(self.state)
        self.assertIsInstance(action, Action)

    def test_greedy_agent_selects_attack_when_charged(self):
        agent = GreedyAgent()
        action = agent.select_action(self.state)
        self.assertIsInstance(action, Action)
        # Greedy agent should select attack since active pokemon has sufficient energy
        self.assertEqual(action.action_type, ActionType.ATTACK)

    def test_heuristic_agent_selects_action(self):
        agent = HeuristicAgent()
        action = agent.select_action(self.state)
        self.assertIsInstance(action, Action)

    def test_probabilistic_agent_selects_action(self):
        agent = ProbabilisticAgent()
        action = agent.select_action(self.state)
        self.assertIsInstance(action, Action)

    def test_pokestrategist_agent_selects_and_explains(self):
        agent = PokeStrategistAgent(simulations=5)
        action = agent.select_action(self.state)
        self.assertIsInstance(action, Action)
        self.assertIsNotNone(agent.last_decision_trace)
        explanation = agent.get_last_decision_explanation()
        self.assertIn("PokéStrategist Decision Explanation", explanation)

if __name__ == "__main__":
    unittest.main()
