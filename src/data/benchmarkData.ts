export interface BenchmarkMatch {
  agent_name: string;
  matches: number;
  wins: number;
  losses: number;
  draws: number;
  win_rate: number;
  avg_game_length_turns: number;
  avg_prize_differential: number;
  avg_damage_dealt: number;
}

export interface TournamentResult {
  [agent: string]: {
    overall_win_rate: number;
    pairings: {
      [matchup: string]: BenchmarkMatch;
    };
  };
}

export interface AblationResult {
  [config: string]: BenchmarkMatch;
}

export const TOURNAMENT_DATA: TournamentResult = {
  "RandomAgent": {
    "overall_win_rate": 0.133,
    "pairings": {
      "RandomAgent vs GreedyAgent": {
        "agent_name": "RandomAgent",
        "matches": 15,
        "wins": 3,
        "losses": 12,
        "draws": 0,
        "win_rate": 0.200,
        "avg_game_length_turns": 5.20,
        "avg_prize_differential": -1.20,
        "avg_damage_dealt": 34.7
      },
      "RandomAgent vs HeuristicAgent": {
        "agent_name": "RandomAgent",
        "matches": 15,
        "wins": 1,
        "losses": 14,
        "draws": 0,
        "win_rate": 0.067,
        "avg_game_length_turns": 3.20,
        "avg_prize_differential": -1.20,
        "avg_damage_dealt": 20.0
      },
      "RandomAgent vs ProbabilisticAgent": {
        "agent_name": "RandomAgent",
        "matches": 15,
        "wins": 2,
        "losses": 13,
        "draws": 0,
        "win_rate": 0.133,
        "avg_game_length_turns": 3.20,
        "avg_prize_differential": -1.07,
        "avg_damage_dealt": 16.7
      },
      "RandomAgent vs PokéStrategist": {
        "agent_name": "RandomAgent",
        "matches": 15,
        "wins": 2,
        "losses": 13,
        "draws": 0,
        "win_rate": 0.133,
        "avg_game_length_turns": 5.13,
        "avg_prize_differential": -1.13,
        "avg_damage_dealt": 27.3
      }
    }
  },
  "GreedyAgent": {
    "overall_win_rate": 0.400,
    "pairings": {
      "GreedyAgent vs RandomAgent": {
        "agent_name": "GreedyAgent",
        "matches": 15,
        "wins": 5,
        "losses": 10,
        "draws": 0,
        "win_rate": 0.333,
        "avg_game_length_turns": 3.27,
        "avg_prize_differential": -0.53,
        "avg_damage_dealt": 42.7
      },
      "GreedyAgent vs HeuristicAgent": {
        "agent_name": "GreedyAgent",
        "matches": 15,
        "wins": 3,
        "losses": 12,
        "draws": 0,
        "win_rate": 0.200,
        "avg_game_length_turns": 2.93,
        "avg_prize_differential": -0.80,
        "avg_damage_dealt": 36.7
      },
      "GreedyAgent vs ProbabilisticAgent": {
        "agent_name": "GreedyAgent",
        "matches": 15,
        "wins": 7,
        "losses": 8,
        "draws": 0,
        "win_rate": 0.467,
        "avg_game_length_turns": 3.13,
        "avg_prize_differential": -0.27,
        "avg_damage_dealt": 45.3
      },
      "GreedyAgent vs PokéStrategist": {
        "agent_name": "GreedyAgent",
        "matches": 15,
        "wins": 9,
        "losses": 6,
        "draws": 0,
        "win_rate": 0.600,
        "avg_game_length_turns": 4.33,
        "avg_prize_differential": -0.07,
        "avg_damage_dealt": 57.3
      }
    }
  },
  "HeuristicAgent": {
    "overall_win_rate": 0.400,
    "pairings": {
      "HeuristicAgent vs RandomAgent": {
        "agent_name": "HeuristicAgent",
        "matches": 15,
        "wins": 4,
        "losses": 11,
        "draws": 0,
        "win_rate": 0.267,
        "avg_game_length_turns": 4.13,
        "avg_prize_differential": -0.80,
        "avg_damage_dealt": 26.7
      },
      "HeuristicAgent vs GreedyAgent": {
        "agent_name": "HeuristicAgent",
        "matches": 15,
        "wins": 5,
        "losses": 10,
        "draws": 0,
        "win_rate": 0.333,
        "avg_game_length_turns": 2.87,
        "avg_prize_differential": -0.40,
        "avg_damage_dealt": 44.0
      },
      "HeuristicAgent vs ProbabilisticAgent": {
        "agent_name": "HeuristicAgent",
        "matches": 15,
        "wins": 9,
        "losses": 6,
        "draws": 0,
        "win_rate": 0.600,
        "avg_game_length_turns": 3.53,
        "avg_prize_differential": 0.00,
        "avg_damage_dealt": 51.3
      },
      "HeuristicAgent vs PokéStrategist": {
        "agent_name": "HeuristicAgent",
        "matches": 15,
        "wins": 6,
        "losses": 9,
        "draws": 0,
        "win_rate": 0.400,
        "avg_game_length_turns": 3.67,
        "avg_prize_differential": -0.47,
        "avg_damage_dealt": 56.7
      }
    }
  },
  "ProbabilisticAgent": {
    "overall_win_rate": 0.467,
    "pairings": {
      "ProbabilisticAgent vs RandomAgent": {
        "agent_name": "ProbabilisticAgent",
        "matches": 15,
        "wins": 5,
        "losses": 10,
        "draws": 0,
        "win_rate": 0.333,
        "avg_game_length_turns": 3.53,
        "avg_prize_differential": -0.93,
        "avg_damage_dealt": 49.3
      },
      "ProbabilisticAgent vs GreedyAgent": {
        "agent_name": "ProbabilisticAgent",
        "matches": 15,
        "wins": 7,
        "losses": 8,
        "draws": 0,
        "win_rate": 0.467,
        "avg_game_length_turns": 3.20,
        "avg_prize_differential": -0.40,
        "avg_damage_dealt": 55.3
      },
      "ProbabilisticAgent vs HeuristicAgent": {
        "agent_name": "ProbabilisticAgent",
        "matches": 15,
        "wins": 10,
        "losses": 5,
        "draws": 0,
        "win_rate": 0.667,
        "avg_game_length_turns": 4.07,
        "avg_prize_differential": -0.07,
        "avg_damage_dealt": 74.0
      },
      "ProbabilisticAgent vs PokéStrategist": {
        "agent_name": "ProbabilisticAgent",
        "matches": 15,
        "wins": 6,
        "losses": 9,
        "draws": 0,
        "win_rate": 0.400,
        "avg_game_length_turns": 4.80,
        "avg_prize_differential": -0.87,
        "avg_damage_dealt": 44.7
      }
    }
  },
  "PokéStrategist": {
    "overall_win_rate": 0.333,
    "pairings": {
      "PokéStrategist vs RandomAgent": {
        "agent_name": "PokéStrategist",
        "matches": 15,
        "wins": 4,
        "losses": 11,
        "draws": 0,
        "win_rate": 0.267,
        "avg_game_length_turns": 5.40,
        "avg_prize_differential": -1.27,
        "avg_damage_dealt": 36.0
      },
      "PokéStrategist vs GreedyAgent": {
        "agent_name": "PokéStrategist",
        "matches": 15,
        "wins": 5,
        "losses": 10,
        "draws": 0,
        "win_rate": 0.333,
        "avg_game_length_turns": 5.13,
        "avg_prize_differential": -1.07,
        "avg_damage_dealt": 42.0
      },
      "PokéStrategist vs HeuristicAgent": {
        "agent_name": "PokéStrategist",
        "matches": 15,
        "wins": 5,
        "losses": 10,
        "draws": 0,
        "win_rate": 0.333,
        "avg_game_length_turns": 3.80,
        "avg_prize_differential": -0.80,
        "avg_damage_dealt": 40.0
      },
      "PokéStrategist vs ProbabilisticAgent": {
        "agent_name": "PokéStrategist",
        "matches": 15,
        "wins": 6,
        "losses": 9,
        "draws": 0,
        "win_rate": 0.400,
        "avg_game_length_turns": 3.53,
        "avg_prize_differential": -0.80,
        "avg_damage_dealt": 42.0
      }
    }
  }
};

export const ABLATION_DATA: AblationResult = {
  "A: Heuristic Baseline": {
    "agent_name": "A: Heuristic Baseline",
    "matches": 20,
    "wins": 10,
    "losses": 10,
    "draws": 0,
    "win_rate": 0.500,
    "avg_game_length_turns": 3.85,
    "avg_prize_differential": -0.20,
    "avg_damage_dealt": 56.0
  },
  "B: Heuristic + Opponent Model": {
    "agent_name": "B: Heuristic + Opponent Model",
    "matches": 20,
    "wins": 10,
    "losses": 10,
    "draws": 0,
    "win_rate": 0.500,
    "avg_game_length_turns": 3.85,
    "avg_prize_differential": -0.20,
    "avg_damage_dealt": 56.0
  },
  "C: Heuristic + Memory": {
    "agent_name": "C: Heuristic + Memory",
    "matches": 20,
    "wins": 7,
    "losses": 13,
    "draws": 0,
    "win_rate": 0.350,
    "avg_game_length_turns": 4.40,
    "avg_prize_differential": -0.85,
    "avg_damage_dealt": 47.0
  },
  "D: Heuristic + Planning (No Belief)": {
    "agent_name": "D: Heuristic + Planning (No Belief)",
    "matches": 20,
    "wins": 7,
    "losses": 13,
    "draws": 0,
    "win_rate": 0.350,
    "avg_game_length_turns": 4.55,
    "avg_prize_differential": -0.85,
    "avg_damage_dealt": 44.5
  },
  "E: Opponent Model + Planning": {
    "agent_name": "E: Opponent Model + Planning",
    "matches": 20,
    "wins": 7,
    "losses": 13,
    "draws": 0,
    "win_rate": 0.350,
    "avg_game_length_turns": 4.55,
    "avg_prize_differential": -0.85,
    "avg_damage_dealt": 44.5
  },
  "F: Full PokéStrategist (Unified)": {
    "agent_name": "F: Full PokéStrategist (Unified)",
    "matches": 20,
    "wins": 7,
    "losses": 13,
    "draws": 0,
    "win_rate": 0.350,
    "avg_game_length_turns": 4.55,
    "avg_prize_differential": -0.85,
    "avg_damage_dealt": 44.5
  }
};
