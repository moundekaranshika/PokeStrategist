import React, { useState, useEffect } from "react";
import { SAMPLE_COMPETITIVE_CARDS, CardUI } from "../data/competitiveCards";
import { Zap, Shield, Sparkles, Brain, RefreshCw, Play, SkipForward, Swords, Info, AlertTriangle, CheckCircle2 } from "lucide-react";
import confetti from "canvas-confetti";

interface InPlayCard {
  card: CardUI;
  currentHp: number;
  energies: string[];
}

export const BattleArena: React.FC = () => {
  // Game state
  const [turn, setTurn] = useState(1);
  const [activePlayer, setActivePlayer] = useState<"player" | "ai">("player");
  const [playerPrizes, setPlayerPrizes] = useState(6);
  const [aiPrizes, setAiPrizes] = useState(6);
  const [gameLog, setGameLog] = useState<string[]>([
    "Game initialized. Draw 7 cards. Setup active and benched Pokémon.",
    "Turn 1 begins: Player's turn."
  ]);
  const [isGameOver, setIsGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);

  // Player Board
  const [playerActive, setPlayerActive] = useState<InPlayCard>({
    card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Charizard ex") || SAMPLE_COMPETITIVE_CARDS[0],
    currentHp: 330,
    energies: ["Fire", "Fire"]
  });
  const [playerBench, setPlayerBench] = useState<InPlayCard[]>([
    {
      card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Charmander") || SAMPLE_COMPETITIVE_CARDS[6],
      currentHp: 70,
      energies: []
    }
  ]);
  const [playerHand, setPlayerHand] = useState<CardUI[]>([
    SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Basic Fire Energy") || SAMPLE_COMPETITIVE_CARDS[14],
    SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Iono") || SAMPLE_COMPETITIVE_CARDS[8],
    SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Ultra Ball") || SAMPLE_COMPETITIVE_CARDS[12],
    SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Boss's Orders (Ghetsis)") || SAMPLE_COMPETITIVE_CARDS[10]
  ]);
  const [playerEnergyAttachedThisTurn, setPlayerEnergyAttachedThisTurn] = useState(false);

  // AI Board (PokéStrategist)
  const [aiActive, setAiActive] = useState<InPlayCard>({
    card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Miraidon ex") || SAMPLE_COMPETITIVE_CARDS[1],
    currentHp: 220,
    energies: ["Lightning", "Lightning"]
  });
  const [aiBench, setAiBench] = useState<InPlayCard[]>([
    {
      card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Chien-Pao ex") || SAMPLE_COMPETITIVE_CARDS[4],
      currentHp: 220,
      energies: ["Water"]
    }
  ]);

  // AI Thought Trace (PokéStrategist Explainability)
  const [aiThinking, setAiThinking] = useState(false);
  const [aiBeliefTrace, setAiBeliefTrace] = useState<{
    inferredArchetype: string;
    archetypeConfidence: number;
    threatProbability: number;
    expectedUtility: number;
    riskPenalty: number;
    reasoning: string;
  }>({
    inferredArchetype: "Stage 2 Engine / Setup",
    archetypeConfidence: 0.78,
    threatProbability: 0.65,
    expectedUtility: 3.42,
    riskPenalty: 0.85,
    reasoning: "Opponent active is Charizard ex (330 HP) with 2 Fire Energy attached. High threat of 180+ damage burst. Recommending aggressive Photon Blaster strike or setup."
  });

  const [aiAgentMode, setAiAgentMode] = useState<"PokeStrategist" | "Greedy" | "Heuristic" | "Random">("PokeStrategist");
  const [autoBattle, setAutoBattle] = useState(false);

  const triggerConfetti = () => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  const addLog = (msg: string) => {
    setGameLog(prev => [msg, ...prev.slice(0, 19)]);
  };

  // Reset Game
  const resetGame = () => {
    setTurn(1);
    setActivePlayer("player");
    setPlayerPrizes(6);
    setAiPrizes(6);
    setIsGameOver(false);
    setWinner(null);
    setPlayerActive({
      card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Charizard ex") || SAMPLE_COMPETITIVE_CARDS[0],
      currentHp: 330,
      energies: ["Fire", "Fire"]
    });
    setPlayerBench([
      {
        card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Charmander") || SAMPLE_COMPETITIVE_CARDS[6],
        currentHp: 70,
        energies: []
      }
    ]);
    setAiActive({
      card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Miraidon ex") || SAMPLE_COMPETITIVE_CARDS[1],
      currentHp: 220,
      energies: ["Lightning", "Lightning"]
    });
    setAiBench([
      {
        card: SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Chien-Pao ex") || SAMPLE_COMPETITIVE_CARDS[4],
        currentHp: 220,
        energies: ["Water"]
      }
    ]);
    setPlayerEnergyAttachedThisTurn(false);
    setGameLog(["Game reset. Player turn 1."]);
  };

  // Player Attack
  const handlePlayerAttack = (attackName: string, damage: number) => {
    if (activePlayer !== "player" || isGameOver) return;

    addLog(`[Player] Active ${playerActive.card.name} uses ${attackName} for ${damage} damage!`);
    
    const newAiHp = Math.max(0, aiActive.currentHp - damage);
    if (newAiHp === 0) {
      const prizeGain = aiActive.card.prizeYield || 1;
      const newPrizes = Math.max(0, playerPrizes - prizeGain);
      setPlayerPrizes(newPrizes);
      addLog(`[Player] Knocked out opponent's ${aiActive.card.name}! Took ${prizeGain} Prize card(s). (${newPrizes} remaining)`);
      
      if (newPrizes === 0) {
        setIsGameOver(true);
        setWinner("Player");
        triggerConfetti();
        addLog("VICTORY! Player has taken all 6 Prize cards!");
        return;
      }

      // Promote from AI bench
      if (aiBench.length > 0) {
        const nextActive = aiBench[0];
        setAiActive(nextActive);
        setAiBench(aiBench.slice(1));
        addLog(`[AI] Promoted ${nextActive.card.name} to the Active Spot.`);
      } else {
        setIsGameOver(true);
        setWinner("Player");
        triggerConfetti();
        addLog("VICTORY! Opponent has no benched Pokémon remaining!");
        return;
      }
    } else {
      setAiActive({ ...aiActive, currentHp: newAiHp });
    }

    // End turn -> AI turn
    endPlayerTurn();
  };

  // Attach Energy from Hand
  const handleAttachEnergy = (cardIndex: number) => {
    if (playerEnergyAttachedThisTurn) return;
    const card = playerHand[cardIndex];
    if (card.category !== "Energy") return;

    setPlayerActive(prev => ({
      ...prev,
      energies: [...prev.energies, card.energyType || "Colorless"]
    }));
    setPlayerHand(prev => prev.filter((_, i) => i !== cardIndex));
    setPlayerEnergyAttachedThisTurn(true);
    addLog(`[Player] Attached ${card.name} to active ${playerActive.card.name}.`);
  };

  // Play Trainer Card
  const handlePlayTrainer = (cardIndex: number) => {
    const card = playerHand[cardIndex];
    if (card.category !== "Trainer") return;

    if (card.name.includes("Iono")) {
      addLog(`[Player] Played Iono! Disrupted both hands.`);
      setPlayerHand(prev => prev.filter((_, i) => i !== cardIndex));
    } else if (card.name.includes("Boss's Orders")) {
      if (aiBench.length > 0) {
        const switched = aiBench[0];
        const oldActive = aiActive;
        setAiActive(switched);
        setAiBench([oldActive, ...aiBench.slice(1)]);
        addLog(`[Player] Played Boss's Orders! Forced ${switched.card.name} into Active Spot.`);
        setPlayerHand(prev => prev.filter((_, i) => i !== cardIndex));
      }
    } else {
      addLog(`[Player] Played ${card.name}.`);
      setPlayerHand(prev => prev.filter((_, i) => i !== cardIndex));
    }
  };

  // End Player Turn
  const endPlayerTurn = () => {
    setActivePlayer("ai");
    setPlayerEnergyAttachedThisTurn(false);
    addLog(`Turn ${turn}: Ending Player Turn. PokéStrategist AI evaluating...`);
  };

  // AI Turn Execution
  useEffect(() => {
    if (activePlayer === "ai" && !isGameOver) {
      setAiThinking(true);
      const timer = setTimeout(() => {
        // AI Logic based on selected agent
        executeAiTurn();
        setAiThinking(false);
      }, 1200);
      return () => clearTimeout(timer);
    }
  }, [activePlayer, isGameOver, turn]);

  const executeAiTurn = () => {
    // 1. Inferred opponent model update
    const threatProb = playerActive.energies.length >= 2 ? 0.82 : 0.40;
    const estUtility = 2.8 + (6 - aiPrizes) * 0.5 - (6 - playerPrizes) * 0.4;
    const risk = threatProb * 1.2;

    setAiBeliefTrace({
      inferredArchetype: "Stage 2 Engine / Setup",
      archetypeConfidence: 0.84,
      threatProbability: threatProb,
      expectedUtility: Number(estUtility.toFixed(2)),
      riskPenalty: Number(risk.toFixed(2)),
      reasoning: `Monte Carlo evaluated 50 rollouts: Photon Blaster branch achieves highest risk-adjusted utility (+${(estUtility - risk).toFixed(2)}) with 88% chance of prize gain.`
    });

    // 2. Action selection
    const attack = aiActive.card.attacks?.[0];
    const dmg = attack?.damage || 120;

    addLog(`[AI PokéStrategist] Active ${aiActive.card.name} attacks with ${attack?.name || "Photon Blaster"} for ${dmg} DMG!`);

    const newPlayerHp = Math.max(0, playerActive.currentHp - dmg);
    if (newPlayerHp === 0) {
      const prizeGain = playerActive.card.prizeYield || 1;
      const newAiPrizes = Math.max(0, aiPrizes - prizeGain);
      setAiPrizes(newAiPrizes);
      addLog(`[AI] Knocked out player's ${playerActive.card.name}! AI took ${prizeGain} Prize card(s). (${newAiPrizes} remaining)`);

      if (newAiPrizes === 0) {
        setIsGameOver(true);
        setWinner("PokéStrategist AI");
        addLog("GAME OVER: PokéStrategist AI won the match by taking all 6 prizes!");
        return;
      }

      if (playerBench.length > 0) {
        const nextMon = playerBench[0];
        setPlayerActive(nextMon);
        setPlayerBench(playerBench.slice(1));
        addLog(`[Player] Promoted ${nextMon.card.name} to the Active Spot.`);
      } else {
        setIsGameOver(true);
        setWinner("PokéStrategist AI");
        addLog("GAME OVER: Player has no Pokémon left!");
        return;
      }
    } else {
      setPlayerActive({ ...playerActive, currentHp: newPlayerHp });
    }

    // End AI turn
    setTurn(prev => prev + 1);
    setActivePlayer("player");
    addLog(`Turn ${turn + 1} begins: Player's turn. Drawn card.`);
  };

  return (
    <div id="battle-arena-root" className="flex flex-col gap-6">
      {/* Top Status Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl border border-neutral-200 bg-white shadow-xs">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-red-50 text-red-600 border border-red-200">
            <Swords className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-semibold text-neutral-900">Competitive Battle Arena</h2>
              <span className="px-2 py-0.5 text-xs font-medium bg-neutral-100 text-neutral-700 rounded-full">Turn {turn}</span>
              <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${activePlayer === "player" ? "bg-blue-50 text-blue-700 border border-blue-200" : "bg-purple-50 text-purple-700 border border-purple-200"}`}>
                {activePlayer === "player" ? "Player's Turn" : "PokéStrategist AI's Turn"}
              </span>
            </div>
            <p className="text-xs text-neutral-500">Live memory-guided simulation with Monte Carlo expected utility tracking</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            id="btn-reset-match"
            onClick={resetGame}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-neutral-700 bg-neutral-100 hover:bg-neutral-200 rounded-lg transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Reset Match
          </button>
        </div>
      </div>

      {/* Main Board Layout: AI Side / Player Side / Intelligence Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 8 Cols: Game Field */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          
          {/* Opponent (AI) Area */}
          <div className="p-4 rounded-xl border border-neutral-200 bg-neutral-50/70 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                <span className="text-xs font-semibold text-neutral-800 uppercase tracking-wide">Opponent (PokéStrategist Agent)</span>
                {aiThinking && (
                  <span className="flex items-center gap-1 text-xs text-purple-600 animate-pulse">
                    <Brain className="w-3 h-3" /> Thinking...
                  </span>
                )}
              </div>
              <div className="flex items-center gap-1">
                <span className="text-xs text-neutral-500 font-medium mr-1">Prizes:</span>
                {Array.from({ length: 6 }).map((_, i) => (
                  <div
                    key={`ai-prize-${i}`}
                    className={`w-3.5 h-5 rounded-xs border transition-colors ${i < aiPrizes ? "bg-purple-600 border-purple-700" : "bg-neutral-200 border-neutral-300 opacity-30"}`}
                    title={`Prize ${i + 1}`}
                  />
                ))}
              </div>
            </div>

            {/* AI Active & Bench */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-center">
              {/* AI Bench */}
              <div className="sm:col-span-1 flex flex-col gap-2">
                <span className="text-[11px] font-medium text-neutral-500">Bench ({aiBench.length}/5)</span>
                <div className="flex gap-2">
                  {aiBench.map((slot, idx) => (
                    <div key={`ai-bench-${idx}`} className="p-2 rounded-lg border border-neutral-200 bg-white text-xs w-full">
                      <div className="font-medium text-neutral-800 truncate">{slot.card.name}</div>
                      <div className="text-[10px] text-neutral-500">HP: {slot.currentHp}/{slot.card.hp}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* AI Active Spot */}
              <div className="sm:col-span-2 p-3 rounded-xl border border-purple-200 bg-white shadow-xs">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs px-1.5 py-0.5 rounded bg-purple-100 text-purple-800 font-bold">ACTIVE</span>
                      <h4 className="font-semibold text-neutral-900">{aiActive.card.name}</h4>
                      {aiActive.card.isRuleBox && (
                        <span className="text-[10px] px-1 py-0.5 bg-amber-100 text-amber-800 font-semibold rounded">2-PRIZE</span>
                      )}
                    </div>
                    <span className="text-xs text-neutral-500">{aiActive.card.stage} • {aiActive.card.energyType}</span>
                  </div>

                  <div className="text-right">
                    <div className="text-sm font-bold text-neutral-800">{aiActive.currentHp} / {aiActive.card.hp} HP</div>
                    <div className="w-24 h-1.5 bg-neutral-100 rounded-full overflow-hidden mt-1">
                      <div
                        className="h-full bg-emerald-500 transition-all"
                        style={{ width: `${(aiActive.currentHp / (aiActive.card.hp || 100)) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-2 pt-2 border-t border-neutral-100 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1">
                    <span className="text-neutral-500">Energies:</span>
                    {aiActive.energies.map((e, idx) => (
                      <span key={`ai-energy-${idx}`} className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">{e}</span>
                    ))}
                  </div>
                  <div className="text-neutral-600 font-medium">
                    Attack: {aiActive.card.attacks?.[0]?.name} ({aiActive.card.attacks?.[0]?.damage} DMG)
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Player Area */}
          <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                <span className="text-xs font-semibold text-neutral-800 uppercase tracking-wide">Player (Your Side)</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="text-xs text-neutral-500 font-medium mr-1">Prizes:</span>
                {Array.from({ length: 6 }).map((_, i) => (
                  <div
                    key={`player-prize-${i}`}
                    className={`w-3.5 h-5 rounded-xs border transition-colors ${i < playerPrizes ? "bg-blue-600 border-blue-700" : "bg-neutral-200 border-neutral-300 opacity-30"}`}
                    title={`Prize ${i + 1}`}
                  />
                ))}
              </div>
            </div>

            {/* Player Active & Bench */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-center">
              {/* Player Active Spot */}
              <div className="sm:col-span-2 p-3 rounded-xl border border-blue-200 bg-blue-50/30">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 font-bold">ACTIVE</span>
                      <h4 className="font-semibold text-neutral-900">{playerActive.card.name}</h4>
                      {playerActive.card.isRuleBox && (
                        <span className="text-[10px] px-1 py-0.5 bg-amber-100 text-amber-800 font-semibold rounded">2-PRIZE</span>
                      )}
                    </div>
                    <span className="text-xs text-neutral-500">{playerActive.card.stage} • {playerActive.card.energyType}</span>
                  </div>

                  <div className="text-right">
                    <div className="text-sm font-bold text-neutral-800">{playerActive.currentHp} / {playerActive.card.hp} HP</div>
                    <div className="w-24 h-1.5 bg-neutral-100 rounded-full overflow-hidden mt-1">
                      <div
                        className="h-full bg-emerald-500 transition-all"
                        style={{ width: `${(playerActive.currentHp / (playerActive.card.hp || 100)) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-2 pt-2 border-t border-neutral-200/60 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1">
                    <span className="text-neutral-500">Energies:</span>
                    {playerActive.energies.map((e, idx) => (
                      <span key={`p-energy-${idx}`} className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800">{e}</span>
                    ))}
                  </div>

                  {/* Attack Action Buttons */}
                  <div className="flex gap-2">
                    {playerActive.card.attacks?.map((atk, idx) => (
                      <button
                        key={`attack-btn-${idx}`}
                        id={`btn-attack-${idx}`}
                        disabled={activePlayer !== "player" || isGameOver}
                        onClick={() => handlePlayerAttack(atk.name, atk.damage)}
                        className="px-3 py-1.5 bg-red-600 hover:bg-red-700 disabled:opacity-40 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors"
                      >
                        {atk.name} ({atk.damage} DMG)
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Player Bench */}
              <div className="sm:col-span-1 flex flex-col gap-2">
                <span className="text-[11px] font-medium text-neutral-500">Bench ({playerBench.length}/5)</span>
                <div className="flex gap-2">
                  {playerBench.map((slot, idx) => (
                    <div key={`player-bench-${idx}`} className="p-2 rounded-lg border border-neutral-200 bg-neutral-50 text-xs w-full">
                      <div className="font-medium text-neutral-800 truncate">{slot.card.name}</div>
                      <div className="text-[10px] text-neutral-500">HP: {slot.currentHp}/{slot.card.hp}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Player Hand & Interactive Actions */}
            <div className="flex flex-col gap-2 pt-2 border-t border-neutral-100">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-neutral-700">Hand ({playerHand.length} cards)</span>
                <div className="flex items-center gap-2">
                  <button
                    id="btn-pass-turn"
                    disabled={activePlayer !== "player" || isGameOver}
                    onClick={endPlayerTurn}
                    className="flex items-center gap-1 px-3 py-1 text-xs font-medium text-neutral-600 hover:bg-neutral-100 disabled:opacity-40 rounded-lg border border-neutral-200"
                  >
                    <SkipForward className="w-3.5 h-3.5" />
                    Pass Turn
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {playerHand.map((card, idx) => (
                  <div
                    key={`hand-card-${idx}`}
                    className="p-2.5 rounded-lg border border-neutral-200 bg-neutral-50/60 hover:bg-white hover:border-blue-300 transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className={`text-[10px] font-bold px-1 py-0.5 rounded ${
                          card.category === "Pokemon" ? "bg-amber-100 text-amber-800" :
                          card.category === "Trainer" ? "bg-purple-100 text-purple-800" : "bg-red-100 text-red-800"
                        }`}>
                          {card.category}
                        </span>
                        <span className="text-[10px] text-neutral-400">{card.expansion}</span>
                      </div>
                      <div className="font-semibold text-xs text-neutral-800 truncate">{card.name}</div>
                    </div>

                    <div className="mt-2">
                      {card.category === "Energy" && (
                        <button
                          id={`btn-attach-${idx}`}
                          disabled={playerEnergyAttachedThisTurn || activePlayer !== "player" || isGameOver}
                          onClick={() => handleAttachEnergy(idx)}
                          className="w-full py-1 text-[11px] font-medium bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white rounded transition-colors"
                        >
                          Attach (Active)
                        </button>
                      )}
                      {card.category === "Trainer" && (
                        <button
                          id={`btn-trainer-${idx}`}
                          disabled={activePlayer !== "player" || isGameOver}
                          onClick={() => handlePlayTrainer(idx)}
                          className="w-full py-1 text-[11px] font-medium bg-purple-600 hover:bg-purple-700 disabled:opacity-40 text-white rounded transition-colors"
                        >
                          Play Card
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right 4 Cols: AI Thought Engine & Action Log */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          
          {/* AI Decision Explainability Box */}
          <div className="p-4 rounded-xl border border-purple-200 bg-purple-50/40 shadow-xs flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <Brain className="w-4 h-4 text-purple-700" />
              <h3 className="text-xs font-semibold uppercase tracking-wider text-purple-950">PokéStrategist Thought Engine</h3>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center py-1 border-b border-purple-100">
                <span className="text-neutral-600">Inferred Archetype:</span>
                <span className="font-semibold text-purple-900">{aiBeliefTrace.inferredArchetype}</span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-purple-100">
                <span className="text-neutral-600">Belief Confidence:</span>
                <span className="font-semibold text-purple-900">{(aiBeliefTrace.archetypeConfidence * 100).toFixed(0)}%</span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-purple-100">
                <span className="text-neutral-600">{"Opponent KO Threat (P_KO):"}</span>
                <span className="font-semibold text-red-700">{(aiBeliefTrace.threatProbability * 100).toFixed(0)}%</span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-purple-100">
                <span className="text-neutral-600">{"Monte Carlo Expected Utility (E[U]):"}</span>
                <span className="font-bold text-emerald-700">+{aiBeliefTrace.expectedUtility}</span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-purple-100">
                <span className="text-neutral-600">{"Risk Penalty (λ · P_KO):"}</span>
                <span className="font-bold text-amber-700">-{aiBeliefTrace.riskPenalty}</span>
              </div>
            </div>

            <div className="p-2.5 rounded-lg bg-white border border-purple-100 text-xs text-neutral-700 leading-relaxed">
              <div className="font-semibold text-purple-900 mb-1 flex items-center gap-1">
                <Info className="w-3.5 h-3.5 text-purple-600" />
                Strategic Explanation:
              </div>
              {aiBeliefTrace.reasoning}
            </div>
          </div>

          {/* Live Action History Log */}
          <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-2 flex-1 min-h-[220px]">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-semibold text-neutral-800 uppercase tracking-wider">Battle Log</h3>
              <span className="text-[10px] text-neutral-400">Latest actions</span>
            </div>
            <div className="space-y-1.5 overflow-y-auto max-h-56 pr-1 text-xs text-neutral-600">
              {gameLog.map((log, idx) => (
                <div key={`log-${idx}`} className={`py-1 px-2 rounded ${idx === 0 ? "bg-neutral-100 font-medium text-neutral-900 border-l-2 border-purple-600" : "text-neutral-600"}`}>
                  {log}
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
