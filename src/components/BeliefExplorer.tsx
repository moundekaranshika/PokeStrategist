import React, { useState } from "react";
import { ARCHETYPE_INFO, SAMPLE_COMPETITIVE_CARDS, CardUI } from "../data/competitiveCards";
import { Brain, Activity, ShieldAlert, Sparkles, Plus, Trash2, ArrowRight, CheckCircle2 } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

export const BeliefExplorer: React.FC = () => {
  const [observedCards, setObservedCards] = useState<CardUI[]>([
    SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Miraidon ex") || SAMPLE_COMPETITIVE_CARDS[1],
    SAMPLE_COMPETITIVE_CARDS.find(c => c.name === "Prime Catcher") || SAMPLE_COMPETITIVE_CARDS[11]
  ]);

  // Bayesian Posterior Distribution
  const calculatePosterior = (cards: CardUI[]) => {
    // Initial uniform prior
    let weights: { [key: string]: number } = {
      "Aggressive / Turbo": 1.0,
      "Stage 2 Engine / Setup": 1.0,
      "Control / Disruption": 1.0,
      "Single-Target Burst": 1.0,
      "Spread / Bench Snipe": 1.0,
      "Defensive / Tank": 1.0,
      "Energy Acceleration": 1.0,
      "Balanced / Midrange": 1.0
    };

    cards.forEach(c => {
      if (c.name.includes("Miraidon") || c.name.includes("Roaring Moon")) {
        weights["Aggressive / Turbo"] *= 5.0;
        weights["Energy Acceleration"] *= 2.5;
      }
      if (c.name.includes("Prime Catcher")) {
        weights["Aggressive / Turbo"] *= 2.5;
        weights["Single-Target Burst"] *= 2.0;
      }
      if (c.name.includes("Charizard") || c.name.includes("Charmander") || c.name.includes("Gardevoir")) {
        weights["Stage 2 Engine / Setup"] *= 6.0;
        weights["Balanced / Midrange"] *= 2.0;
      }
      if (c.name.includes("Iono")) {
        weights["Control / Disruption"] *= 3.0;
        weights["Stage 2 Engine / Setup"] *= 1.8;
      }
      if (c.name.includes("Chien-Pao")) {
        weights["Single-Target Burst"] *= 5.5;
        weights["Energy Acceleration"] *= 3.0;
      }
      if (c.name.includes("Lugia")) {
        weights["Energy Acceleration"] *= 6.0;
      }
    });

    const sum = Object.values(weights).reduce((a, b) => a + b, 0);
    const normalized = Object.entries(weights).map(([arch, w]) => ({
      archetype: arch,
      probability: w / sum,
      percentage: Number(((w / sum) * 100).toFixed(1))
    }));

    // Sort descending
    normalized.sort((a, b) => b.probability - a.probability);

    // Compute Shannon Entropy H(X) = -sum(p * ln(p))
    const entropy = -normalized.reduce((acc, curr) => {
      return curr.probability > 0 ? acc + curr.probability * Math.log(curr.probability) : acc;
    }, 0);

    // Estimated KO threat
    const topArch = normalized[0].archetype;
    const isAggro = topArch === "Aggressive / Turbo" || topArch === "Single-Target Burst";
    const koThreat = isAggro ? 0.85 : topArch === "Stage 2 Engine / Setup" ? 0.60 : 0.35;

    return { distribution: normalized, entropy, topArch, koThreat };
  };

  const { distribution, entropy, topArch, koThreat } = calculatePosterior(observedCards);

  const addObservedCard = (card: CardUI) => {
    setObservedCards(prev => [...prev, card]);
  };

  const removeCard = (index: number) => {
    setObservedCards(prev => prev.filter((_, i) => i !== index));
  };

  const resetObservations = () => {
    setObservedCards([]);
  };

  return (
    <div id="belief-explorer-root" className="flex flex-col gap-6">
      {/* Header Info */}
      <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-purple-50 text-purple-600 border border-purple-200">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-neutral-900">Bayesian Opponent Belief Modeler</h2>
            <p className="text-xs text-neutral-500">{"Recursive likelihood updates P(A_i | x_{1:t}) ∝ P(A_i) ∏ P(x_k | A_i)"}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-neutral-500">Belief Entropy</div>
            <div className="text-sm font-bold text-neutral-900">{entropy.toFixed(3)} nats</div>
          </div>
          <div className="h-8 w-px bg-neutral-200" />
          <div className="text-right">
            <div className="text-xs text-neutral-500">Est. KO Threat</div>
            <div className="text-sm font-bold text-red-600">{(koThreat * 100).toFixed(0)}%</div>
          </div>
        </div>
      </div>

      {/* Main Grid: Card Reveal Input & Posterior Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 5 Cols: Card Observations */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Observed Opponent Cards</h3>
              <button
                id="btn-clear-observations"
                onClick={resetObservations}
                className="text-xs text-red-600 hover:text-red-700 font-medium"
              >
                Clear All
              </button>
            </div>

            {observedCards.length === 0 ? (
              <div className="p-6 text-center border-2 border-dashed border-neutral-200 rounded-xl text-neutral-400 text-xs">
                No opponent cards observed yet. Add cards below to start updating the Bayesian prior.
              </div>
            ) : (
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {observedCards.map((card, idx) => (
                  <div
                    key={`obs-${idx}`}
                    className="p-2.5 rounded-lg border border-neutral-200 bg-neutral-50 flex items-center justify-between text-xs"
                  >
                    <div className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
                      <div>
                        <span className="font-semibold text-neutral-800">{card.name}</span>
                        <span className="ml-2 text-[10px] text-neutral-500">({card.category}{card.stage ? ` • ${card.stage}` : ""})</span>
                      </div>
                    </div>
                    <button
                      onClick={() => removeCard(idx)}
                      className="p-1 text-neutral-400 hover:text-red-600 transition-colors"
                      title="Remove card"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Quick-Add Card Palette */}
            <div className="pt-2 border-t border-neutral-100 flex flex-col gap-2">
              <span className="text-[11px] font-medium text-neutral-500">Click to add opponent observation:</span>
              <div className="grid grid-cols-2 gap-1.5 max-h-48 overflow-y-auto">
                {SAMPLE_COMPETITIVE_CARDS.slice(0, 10).map((card, idx) => (
                  <button
                    key={`quick-${idx}`}
                    onClick={() => addObservedCard(card)}
                    className="p-2 text-left rounded-lg border border-neutral-200 hover:border-purple-300 bg-white hover:bg-purple-50/50 text-xs transition-colors flex items-center justify-between"
                  >
                    <span className="truncate font-medium text-neutral-700">{card.name}</span>
                    <Plus className="w-3 h-3 text-neutral-400" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right 7 Cols: Posterior Archetype Distribution */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">{"Posterior Probability Distribution P(Archetype | Obs)"}</h3>
                <p className="text-xs text-neutral-500">Dynamic 8-class competitive archetype classification</p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-800 border border-purple-200">
                Most Likely: {topArch}
              </span>
            </div>

            {/* Bar Chart of Probabilities */}
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={distribution} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                  <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 11 }} />
                  <YAxis type="category" dataKey="archetype" tick={{ fontSize: 11, fill: "#404040" }} width={140} />
                  <Tooltip
                    formatter={(val: number) => [`${val}%`, "Posterior Probability"]}
                    contentStyle={{ fontSize: "12px", borderRadius: "8px", border: "1px solid #e5e5e5" }}
                  />
                  <Bar dataKey="percentage" radius={[0, 4, 4, 0]}>
                    {distribution.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={index === 0 ? "#7c3aed" : index === 1 ? "#9333ea" : "#c084fc"}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Archetype Profile Breakdown */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-neutral-100">
              {ARCHETYPE_INFO.slice(0, 4).map((arch, idx) => (
                <div key={`arch-${idx}`} className={`p-3 rounded-lg border text-xs ${arch.color}`}>
                  <div className="flex items-center justify-between font-semibold mb-1">
                    <span>{arch.title}</span>
                    <span>T{arch.expectedTurnToAttack} Attack</span>
                  </div>
                  <p className="text-[11px] opacity-80 leading-snug">{arch.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
