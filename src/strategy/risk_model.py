"""
PokéStrategist - Risk-Aware Decision Model
Implements dynamic risk-sensitive scoring:
FinalScore = ExpectedUtility - λ * Risk + μ * FutureValue
Adjusts λ and μ adaptively based on prize margin and game phase.
"""

from typing import Dict, Any
from src.schema import GameState, Action, ActionType

class RiskModel:
    def __init__(self, base_lambda: float = 1.2, base_mu: float = 0.8):
        self.base_lambda = base_lambda # Risk aversion weight
        self.base_mu = base_mu         # Future value / setup weight

    def calculate_risk(self, state: GameState, action: Action, opp_threat_prob: float = 0.3) -> float:
        """
        Quantifies the downside risk of a candidate action.
        Risk factors:
        1. Leaving Active in KO range of opponent's likely attack.
        2. Discarding precious resources (Ultra Ball, Research).
        3. Energy commitment on fragile attacker.
        """
        risk_score = 0.0
        own = state.own_state
        opp = state.opponent_visible_state

        # Factor 1: Active KO Vulnerability
        if own.active and opp.active:
            # Check if active will have low HP left
            if own.active.current_hp <= 90:
                risk_score += 150.0 * opp_threat_prob
            if (own.active.card.features and own.active.card.features.is_rule_box) and own.active.current_hp <= 140:
                # 2-prize liability risk
                risk_score += 250.0 * opp_threat_prob

        # Factor 2: Resource Discard Risk
        if action.action_type == ActionType.PLAY_SUPPORTER and action.card:
            if "research" in action.card.name.lower():
                # Discarding hand has risk if hand has > 3 cards
                risk_score += max(0, (len(own.hand) - 2) * 20.0)

        # Factor 3: Over-extension without bench backup
        if len(own.bench) == 0:
            risk_score += 180.0 # Sudden game-over risk if active is KO'd

        return risk_score

    def calculate_future_value(self, state: GameState, action: Action) -> float:
        """
        Quantifies long-term strategic setup and engine development.
        """
        future_val = 0.0
        own = state.own_state

        # Value 1: Bench development & engine establishment
        if action.action_type == ActionType.BENCH_BASIC:
            future_val += 45.0
        elif action.action_type == ActionType.EVOLVE:
            future_val += 90.0
        elif action.action_type == ActionType.ATTACH_ENERGY:
            # Energy attached to bench attacker builds future turn viability
            if action.target_index != -1:
                future_val += 60.0
            else:
                future_val += 30.0

        # Value 2: Hand expansion
        if action.action_type == ActionType.PLAY_SUPPORTER:
            future_val += 50.0

        return future_val

    def adjust_parameters(self, own_prizes_left: int, opp_prizes_left: int) -> tuple[float, float]:
        """
        Dynamically tunes λ and μ based on prize board state:
        - When leading (e.g. own_prizes = 2, opp_prizes = 5): Increase λ (play safe, protect lead)
        - When trailing (e.g. own_prizes = 5, opp_prizes = 2): Decrease λ (take calculated risks for comeback)
        """
        prize_lead = opp_prizes_left - own_prizes_left # Positive = Leading, Negative = Trailing

        if prize_lead > 0:
            # Ahead: protect board state, penalize risky lines
            dyn_lambda = self.base_lambda * (1.0 + 0.25 * prize_lead)
            dyn_mu = self.base_mu * 0.9
        elif prize_lead < 0:
            # Behind: accept risk in pursuit of high-upside lines
            dyn_lambda = max(0.2, self.base_lambda * (1.0 + 0.20 * prize_lead))
            dyn_mu = self.base_mu * 1.3
        else:
            dyn_lambda = self.base_lambda
            dyn_mu = self.base_mu

        return round(dyn_lambda, 3), round(dyn_mu, 3)

    def compute_risk_adjusted_score(
        self,
        expected_utility: float,
        state: GameState,
        action: Action,
        opp_threat_prob: float = 0.3
    ) -> Dict[str, Any]:
        """
        Computes the final risk-adjusted decision score with component breakdown.
        """
        own_prizes = state.own_state.prizes_remaining
        opp_prizes = state.opponent_visible_state.prizes_remaining

        dyn_lambda, dyn_mu = self.adjust_parameters(own_prizes, opp_prizes)
        risk = self.calculate_risk(state, action, opp_threat_prob)
        future_val = self.calculate_future_value(state, action)

        final_score = expected_utility - (dyn_lambda * risk) + (dyn_mu * future_val)

        return {
            "final_score": round(final_score, 2),
            "expected_utility": round(expected_utility, 2),
            "risk_penalty": round(dyn_lambda * risk, 2),
            "future_value_bonus": round(dyn_mu * future_val, 2),
            "lambda": dyn_lambda,
            "mu": dyn_mu,
            "raw_risk": round(risk, 2),
            "raw_future_val": round(future_val, 2)
        }
