import React from "react";
import { BookOpen, Cpu, Database, Network, ShieldCheck, Terminal, Compass, Layers } from "lucide-react";

export const ResearchArchitecture: React.FC = () => {
  return (
    <div id="research-architecture-root" className="flex flex-col gap-6">
      {/* Header */}
      <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-blue-50 text-blue-600 border border-blue-200">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-neutral-900">System Architecture & Theoretical Formulation</h2>
            <p className="text-xs text-neutral-500">PokéStrategist mathematical model, episodic memory graphs, and Bayesian update mechanics</p>
          </div>
        </div>
      </div>

      {/* Grid: 3 Main Architectural Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Pillar 1 */}
        <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-3">
          <div className="flex items-center gap-2 text-purple-700">
            <Database className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider">1. Card & Deck Intelligence</h3>
          </div>
          <p className="text-xs text-neutral-600 leading-relaxed">
            Parses 2,000+ standard-legal Pokémon TCG cards into typed schema entities with derived mathematical features:
          </p>
          <ul className="text-xs text-neutral-600 space-y-1.5 list-disc list-inside">
            <li><span className="font-semibold text-neutral-800">Attack Efficiency:</span> {"Eff(c) = Max_Damage / max(1, Total_Cost)"}</li>
            <li><span className="font-semibold text-neutral-800">Survivability Index:</span> {"Surv(c) = HP / (Prize_Yield · (1 + 0.5 · Retreat))"}</li>
            <li><span className="font-semibold text-neutral-800">Archetype Clustering:</span> 8 competitive archetype priors (Turbo, Setup, Control, Burst, Snipe, Tank, Accel, Midrange).</li>
          </ul>
        </div>

        {/* Pillar 2 */}
        <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-3">
          <div className="flex items-center gap-2 text-blue-700">
            <Network className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider">2. Bayesian Opponent Modeling</h3>
          </div>
          <p className="text-xs text-neutral-600 leading-relaxed">
            {"Maintains recursive belief distribution over opponent archetype A_i ∈ A under partial observability:"}
          </p>
          <div className="p-2.5 rounded-lg bg-neutral-50 border border-neutral-200 text-xs font-mono text-neutral-800">
            {"P(A_i | x_{1:t}) ∝ P(A_i) · ∏ P(x_k | A_i)"}
          </div>
          <p className="text-xs text-neutral-600 leading-relaxed">
            {"Computes Shannon Entropy H(X) to quantify uncertainty and derive instant opponent KO threat P_KO(s)."}
          </p>
        </div>

        {/* Pillar 3 */}
        <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-3">
          <div className="flex items-center gap-2 text-emerald-700">
            <Cpu className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider">3. Monte Carlo Risk Planner</h3>
          </div>
          <p className="text-xs text-neutral-600 leading-relaxed">
            Rolls forward stochastic action branches with dynamic risk penalty and future value potential:
          </p>
          <div className="p-2.5 rounded-lg bg-neutral-50 border border-neutral-200 text-xs font-mono text-neutral-800">
            {"U_adj(a) = E[U(s')] - λ · P_KO(s') + μ · V_future(s')"}
          </div>
          <p className="text-xs text-neutral-600 leading-relaxed">
            Balances aggressive prize acceleration against board wipe vulnerability and prize race tempo.
          </p>
        </div>
      </div>

      {/* Code & Notebooks Overview */}
      <div className="p-5 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4">
        <div>
          <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Research Codebase & Interactive Notebooks</h3>
          <p className="text-xs text-neutral-500">Standalone runnable modules in the repository</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 rounded-lg border border-neutral-200 bg-neutral-50">
            <div className="font-semibold text-neutral-900">notebooks/01_eda_and_card_intelligence.py</div>
            <p className="text-neutral-500 text-[11px] mt-1">2,000+ card EDA, feature distributions, durability rankings.</p>
          </div>

          <div className="p-3 rounded-lg border border-neutral-200 bg-neutral-50">
            <div className="font-semibold text-neutral-900">notebooks/02_archetype_and_belief_modeling.py</div>
            <p className="text-neutral-500 text-[11px] mt-1">Step-by-step Bayesian prior updates & entropy convergence.</p>
          </div>

          <div className="p-3 rounded-lg border border-neutral-200 bg-neutral-50">
            <div className="font-semibold text-neutral-900">notebooks/03_strategic_memory_and_evaluation.py</div>
            <p className="text-neutral-500 text-[11px] mt-1">Episodic memory transitions and composite board evaluator.</p>
          </div>

          <div className="p-3 rounded-lg border border-neutral-200 bg-neutral-50">
            <div className="font-semibold text-neutral-900">notebooks/04_monte_carlo_and_risk_planning.py</div>
            <p className="text-neutral-500 text-[11px] mt-1">Stochastic action branch simulation and utility rankings.</p>
          </div>

          <div className="p-3 rounded-lg border border-neutral-200 bg-neutral-50">
            <div className="font-semibold text-neutral-900">notebooks/05_tournament_and_benchmarking.py</div>
            <p className="text-neutral-500 text-[11px] mt-1">Round-robin agent matrix evaluation across 5 baseline bots.</p>
          </div>

          <div className="p-3 rounded-lg border border-neutral-200 bg-neutral-50">
            <div className="font-semibold text-neutral-900">notebooks/06_ablation_and_explainability.py</div>
            <p className="text-neutral-500 text-[11px] mt-1">Systematic component ablation study (Configs A through F).</p>
          </div>
        </div>
      </div>
    </div>
  );
};
