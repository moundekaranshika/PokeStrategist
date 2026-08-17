"""
PokéStrategist - Memory-Guided Probabilistic Strategic Planning Agent
The flagship system integrating Card Intelligence, Bayesian Opponent Belief Modeling,
Strategic Memory, Monte Carlo Forward Simulation, and Risk-Aware Utility Optimization.
"""

from typing import List, Dict, Any, Optional
from src.schema import GameState, Action, ActionType
from src.strategy.action_generator import ActionGenerator
from src.strategy.board_evaluator import BoardEvaluator
from src.opponent.opponent_model import OpponentModel
from src.memory.game_memory import GameMemory
from src.memory.strategic_memory import StrategicMemory
from src.planning.monte_carlo import MonteCarloPlanner
from src.strategy.risk_model import RiskModel

class PokeStrategistAgent:
    def __init__(
        self,
        simulations: int = 50,
        board_evaluator: Optional[BoardEvaluator] = None,
        risk_model: Optional[RiskModel] = None,
        strategic_memory: Optional[StrategicMemory] = None
    ):
        self.name = "PokéStrategist"
        self.simulations = simulations
        self.evaluator = board_evaluator or BoardEvaluator()
        self.opponent_model = OpponentModel()
        self.game_memory = GameMemory()
        self.strategic_memory = strategic_memory or StrategicMemory()
        self.planner = MonteCarloPlanner(self.evaluator, default_simulations=simulations)
        self.risk_model = risk_model or RiskModel()
        self.last_decision_trace: Optional[Dict[str, Any]] = None

    def reset_game(self):
        """Resets intra-game state while preserving long-term strategic memory."""
        self.opponent_model.reset()
        self.game_memory = GameMemory()
        self.last_decision_trace = None

    def select_action(self, state: GameState) -> Action:
        """
        Executes the complete PokéStrategist decision pipeline:
        1. Action generation
        2. Monte Carlo expected utility simulation under opponent belief distribution
        3. Risk-aware utility scoring (Risk penalty & Future value bonus)
        4. Explainable ranking and action selection
        """
        candidate_actions = ActionGenerator.generate_legal_actions(state)
        if not candidate_actions:
            return Action(action_type=ActionType.PASS_TURN)

        if len(candidate_actions) == 1:
            return candidate_actions[0]

        # 1. Forward Monte Carlo simulation under opponent belief model
        plan_results = self.planner.plan(
            state=state,
            candidate_actions=candidate_actions,
            belief=self.opponent_model.belief,
            num_simulations=self.simulations
        )

        # 2. Risk-aware utility evaluation
        scored_actions = []
        opp_threat = self.opponent_model.belief.estimated_ko_threat_prob

        for res in plan_results:
            action = res["action"]
            eu = res["expected_utility"]
            risk_breakdown = self.risk_model.compute_risk_adjusted_score(
                expected_utility=eu,
                state=state,
                action=action,
                opp_threat_prob=opp_threat
            )

            scored_actions.append({
                "action": action,
                "description": res["description"],
                "expected_utility": eu,
                "risk_breakdown": risk_breakdown,
                "final_score": risk_breakdown["final_score"],
                "std_dev": res["std_dev"],
                "min_utility": res["min_utility"],
                "max_utility": res["max_utility"]
            })

        # Rank by final risk-adjusted score
        scored_actions.sort(key=lambda x: x["final_score"], reverse=True)
        best_candidate = scored_actions[0]

        # Store complete decision trace for explainability and inspection
        self.last_decision_trace = {
            "turn": state.turn,
            "chosen_action": best_candidate["description"],
            "final_score": best_candidate["final_score"],
            "expected_utility": best_candidate["expected_utility"],
            "risk_penalty": best_candidate["risk_breakdown"]["risk_penalty"],
            "future_value_bonus": best_candidate["risk_breakdown"]["future_value_bonus"],
            "inferred_opponent_archetype": self.opponent_model.belief.get_most_likely_archetype(),
            "archetype_entropy": self.opponent_model.belief.get_archetype_entropy(),
            "candidate_rankings": [
                {
                    "description": sc["description"],
                    "final_score": sc["final_score"],
                    "eu": sc["expected_utility"],
                    "risk": sc["risk_breakdown"]["risk_penalty"]
                }
                for sc in scored_actions[:5]
            ]
        }

        return best_candidate["action"]

    def get_last_decision_explanation(self) -> str:
        """Generates a human-readable explanation of the last decision."""
        if not self.last_decision_trace:
            return "No decision trace available."
        
        t = self.last_decision_trace
        lines = [
            f"=== PokéStrategist Decision Explanation (Turn {t['turn']}) ===",
            f"Selected Action: {t['chosen_action']}",
            f"Composite Score: {t['final_score']} (EU: {t['expected_utility']} | Risk Penalty: -{t['risk_penalty']} | Future Bonus: +{t['future_value_bonus']})",
            f"Opponent Belief: {t['inferred_opponent_archetype']} (Uncertainty Entropy: {t['archetype_entropy']})",
            "Alternative Rankings:"
        ]
        for rank, alt in enumerate(t["candidate_rankings"], 1):
            lines.append(f"  {rank}. {alt['description']} -> Score: {alt['final_score']} (EU: {alt['eu']}, Risk: {alt['risk']})")
        return "\n".join(lines)
