#  PokéStrategist

### Probabilistic Planning for Pokémon TCG

> A strategic AI framework that combines card intelligence, game-state reasoning, opponent modeling, memory, and risk-aware probabilistic planning.

---

##  Overview

Pokémon TCG is more than choosing the attack that deals the most damage.

A good decision can depend on:

- Current HP and board position
- Available Energy
- Prize progression
- Evolution opportunities
- Retreat options
- Resource management
- The opponent's previous actions
- Hidden information
- Possible future game states

This makes Pokémon TCG an interesting decision-making problem for AI.

**PokéStrategist** explores whether an agent can make better strategic decisions by explicitly reasoning about these factors instead of relying only on immediate rewards or simple heuristics.

The central idea is:

```text
Game State
     ↓
Candidate Actions
     ↓
Opponent Beliefs
     ↓
Future Scenarios
     ↓
Expected Utility
     ↓
Risk Adjustment
     ↓
Final Action
