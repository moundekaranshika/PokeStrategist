import React, { useState } from "react";
import { GitBranch, Shield, Zap, TrendingUp, HelpCircle, Check, ArrowRight, BarChart3, AlertCircle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from "recharts";

interface ActionBranch {
  id: string;
  name: string;
  category: "Attack" | "Energy" | "Trainer" | "Pass";
  expectedUtility: number;
  stdDev: number;
  riskPenalty: number;
  futureValueBonus: number;
  finalScore: number;
  simulations: number;
  winRateBranch: number;
  reasoning: string;
  rollouts: { step: number; utility: number }[];
}

export const MonteCarloTree: React.FC = () => {
  const [selectedBranchId, setSelectedBranchId] = useState<string>("branch-1");
  const [simCount, setSimCount] = useState<number>(50);

  const branches: ActionBranch[] = [
    {
      id: "branch-1",
      name: "Attack: Photon Blaster (220 DMG)",
      category: "Attack",
      expectedUtility: 4.85,
      stdDev: 0.42,
      riskPenalty: 0.65,
      futureValueBonus: 0.90,
      finalScore: 5.10,
      simulations: simCount,
      winRateBranch: 0.86,
      reasoning: "Achieves an immediate 2-Prize Knockout on opponent's active Pokémon. Establishes significant prize lead (4-6) while leaving bench secure.",
      rollouts: [
        { step: 1, utility: 3.2 },
        { step: 2, utility: 4.1 },
        { step: 3, utility: 4.9 },
        { step: 4, utility: 5.2 },
        { step: 5, utility: 5.1 }
      ]
    },
    {
      id: "branch-2",
      name: "Attach Energy to Benched Chien-Pao ex",
      category: "Energy",
      expectedUtility: 3.20,
      stdDev: 0.88,
      riskPenalty: 1.10,
      futureValueBonus: 1.40,
      finalScore: 3.50,
      simulations: simCount,
      winRateBranch: 0.62,
      reasoning: "Prepares secondary attacker on bench, but concedes active tempo. Opponent can retaliate with high-damage attack next turn without active KO threat.",
      rollouts: [
        { step: 1, utility: 2.0 },
        { step: 2, utility: 2.8 },
        { step: 3, utility: 3.1 },
        { step: 4, utility: 3.4 },
        { step: 5, utility: 3.5 }
      ]
    },
    {
      id: "branch-3",
      name: "Play Iono (Disruption Supporter)",
      category: "Trainer",
      expectedUtility: 3.90,
      stdDev: 0.65,
      riskPenalty: 0.50,
      futureValueBonus: 0.80,
      finalScore: 4.20,
      simulations: simCount,
      winRateBranch: 0.74,
      reasoning: "Reduces opponent hand size from 6 to 4, disrupting setup lines. Excellent supplementary branch before attacking.",
      rollouts: [
        { step: 1, utility: 3.0 },
        { step: 2, utility: 3.6 },
        { step: 3, utility: 4.0 },
        { step: 4, utility: 4.3 },
        { step: 5, utility: 4.2 }
      ]
    },
    {
      id: "branch-4",
      name: "Pass Turn Without Action",
      category: "Pass",
      expectedUtility: 0.80,
      stdDev: 1.25,
      riskPenalty: 2.40,
      futureValueBonus: 0.10,
      finalScore: -1.50,
      simulations: simCount,
      winRateBranch: 0.18,
      reasoning: "High-risk pass gives full tempo and uninhibited attack opportunity to opponent. Strongly penalized under risk model.",
      rollouts: [
        { step: 1, utility: 0.5 },
        { step: 2, utility: 0.2 },
        { step: 3, utility: -0.4 },
        { step: 4, utility: -1.1 },
        { step: 5, utility: -1.5 }
      ]
    }
  ];

  const selectedBranch = branches.find(b => b.id === selectedBranchId) || branches[0];

  return (
    <div id="monte-carlo-tree-root" className="flex flex-col gap-6">
      {/* Header */}
      <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-200">
            <GitBranch className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-neutral-900">Monte Carlo Forward Rollout Planner</h2>
            <p className="text-xs text-neutral-500">{"Risk-adjusted utility optimization: U_adj(a) = E[U(s')] - λ P(KO) + μ V_future"}</p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="text-neutral-500 font-medium">Simulations per Branch:</span>
          {[25, 50, 100].map(cnt => (
            <button
              key={`sim-cnt-${cnt}`}
              onClick={() => setSimCount(cnt)}
              className={`px-2.5 py-1 rounded-lg border font-medium transition-colors ${simCount === cnt ? "bg-emerald-600 text-white border-emerald-600" : "bg-neutral-50 text-neutral-700 border-neutral-200 hover:bg-neutral-100"}`}
            >
              N = {cnt}
            </button>
          ))}
        </div>
      </div>

      {/* Grid: Action Branches & Rollout Utility Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 6 Cols: Candidate Action Branches */}
        <div className="lg:col-span-6 flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Candidate Action Tree</h3>
            <span className="text-xs text-neutral-500">Ranked by Composite Score</span>
          </div>

          <div className="space-y-3">
            {branches.map((b, idx) => {
              const isSelected = b.id === selectedBranchId;
              const isTop = idx === 0;
              return (
                <div
                  key={b.id}
                  onClick={() => setSelectedBranchId(b.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? "border-emerald-500 bg-emerald-50/40 shadow-xs ring-1 ring-emerald-400"
                      : "border-neutral-200 bg-white hover:border-neutral-300"
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        {isTop && (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                            BEST ACTION
                          </span>
                        )}
                        <span className="text-xs font-semibold text-neutral-900">{b.name}</span>
                      </div>
                      <span className="text-[11px] text-neutral-500">{b.category} Action Branch • {b.simulations} Rollouts</span>
                    </div>

                    <div className="text-right">
                      <div className={`text-sm font-bold ${b.finalScore >= 0 ? "text-emerald-700" : "text-red-600"}`}>
                        {b.finalScore >= 0 ? `+${b.finalScore.toFixed(2)}` : b.finalScore.toFixed(2)}
                      </div>
                      <div className="text-[10px] text-neutral-400">Composite Score</div>
                    </div>
                  </div>

                  {/* Micro Progress Metrics */}
                  <div className="mt-3 pt-2.5 border-t border-neutral-100 grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-neutral-50 p-1 rounded">
                      <div className="text-[10px] text-neutral-500">Expected Utility</div>
                      <div className="font-semibold text-neutral-800">+{b.expectedUtility.toFixed(2)}</div>
                    </div>
                    <div className="bg-neutral-50 p-1 rounded">
                      <div className="text-[10px] text-neutral-500">Risk Penalty</div>
                      <div className="font-semibold text-amber-700">-{b.riskPenalty.toFixed(2)}</div>
                    </div>
                    <div className="bg-neutral-50 p-1 rounded">
                      <div className="text-[10px] text-neutral-500">Branch Win Rate</div>
                      <div className="font-semibold text-emerald-700">{(b.winRateBranch * 100).toFixed(0)}%</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right 6 Cols: Selected Branch Deep Dive & Rollout Chart */}
        <div className="lg:col-span-6 flex flex-col gap-4">
          <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Branch Rollout Trajectory</h3>
                <p className="text-xs text-neutral-500">{selectedBranch.name}</p>
              </div>
              <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-1 rounded border border-emerald-200">
                Score: {selectedBranch.finalScore.toFixed(2)}
              </span>
            </div>

            {/* Utility Progression Chart */}
            <div className="h-52 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={selectedBranch.rollouts} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                  <XAxis dataKey="step" tick={{ fontSize: 11 }} tickFormatter={(s) => `Depth ${s}`} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip
                    formatter={(val: number) => [val.toFixed(2), "Projected Board Utility"]}
                    labelFormatter={(label) => `Rollout Depth Step ${label}`}
                    contentStyle={{ fontSize: "12px", borderRadius: "8px", border: "1px solid #e5e5e5" }}
                  />
                  <Bar dataKey="utility" fill="#059669" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Detailed Component Breakdown */}
            <div className="p-3 rounded-lg bg-neutral-50 border border-neutral-200 space-y-2 text-xs">
              <div className="font-semibold text-neutral-800 flex items-center gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-neutral-500" />
                Formulaic Term Dissection:
              </div>
              <div className="grid grid-cols-2 gap-2 text-[11px] text-neutral-600">
                <div>• {"E[U]"} (Expected Utility): <span className="font-semibold text-neutral-900">+{selectedBranch.expectedUtility.toFixed(2)}</span></div>
                <div>• {"σ"} (Std Dev Uncertainty): <span className="font-semibold text-neutral-900">±{selectedBranch.stdDev.toFixed(2)}</span></div>
                <div>• {"-λ P(KO)"} (Threat Penalty): <span className="font-semibold text-amber-700">-{selectedBranch.riskPenalty.toFixed(2)}</span></div>
                <div>• {"+μ V_future"} (Setup Bonus): <span className="font-semibold text-emerald-700">+{selectedBranch.futureValueBonus.toFixed(2)}</span></div>
              </div>
            </div>

            {/* Natural Language Explanation */}
            <div className="p-3 rounded-lg bg-emerald-50/60 border border-emerald-200 text-xs text-neutral-700 leading-relaxed">
              <div className="font-semibold text-emerald-950 mb-1">Algorithmic Decision Justification:</div>
              {selectedBranch.reasoning}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
