import React, { useState } from "react";
import { TOURNAMENT_DATA, ABLATION_DATA } from "../data/benchmarkData";
import { Trophy, BarChart2, CheckCircle2, Layers, Award, Target, TrendingUp } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, Cell } from "recharts";

export const TournamentDashboard: React.FC = () => {
  const [activeView, setActiveView] = useState<"tournament" | "ablation">("tournament");

  // Format data for tournament overall win rates
  const tournamentChartData = Object.entries(TOURNAMENT_DATA).map(([agent, data]) => ({
    name: agent,
    winRate: Number((data.overall_win_rate * 100).toFixed(1)),
    avgDamage: agent === "PokéStrategist" ? 42.0 : agent === "ProbabilisticAgent" ? 55.8 : agent === "GreedyAgent" ? 45.5 : agent === "HeuristicAgent" ? 44.7 : 24.7
  }));

  // Format data for ablation study
  const ablationChartData = Object.entries(ABLATION_DATA).map(([config, data]) => ({
    name: config.split(":")[0],
    fullName: config,
    winRate: Number((data.win_rate * 100).toFixed(1)),
    prizeDiff: data.avg_prize_differential,
    gameLength: data.avg_game_length_turns
  }));

  const agents = Object.keys(TOURNAMENT_DATA);

  return (
    <div id="tournament-dashboard-root" className="flex flex-col gap-6">
      {/* Header & Mode Switcher */}
      <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-amber-50 text-amber-600 border border-amber-200">
            <Trophy className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-neutral-900">Empirical Benchmarking & Tournaments</h2>
            <p className="text-xs text-neutral-500">Cross-agent tournament matrix (N=15 per pairing) & systematic component ablation study</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveView("tournament")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              activeView === "tournament"
                ? "bg-neutral-900 text-white"
                : "bg-neutral-100 text-neutral-600 hover:bg-neutral-200"
            }`}
          >
            Round-Robin Tournament
          </button>
          <button
            onClick={() => setActiveView("ablation")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              activeView === "ablation"
                ? "bg-neutral-900 text-white"
                : "bg-neutral-100 text-neutral-600 hover:bg-neutral-200"
            }`}
          >
            Component Ablation (A-F)
          </button>
        </div>
      </div>

      {activeView === "tournament" ? (
        <div className="flex flex-col gap-6">
          {/* Top Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs">
              <div className="text-xs text-neutral-500 font-medium">Total Matches Played</div>
              <div className="text-xl font-bold text-neutral-900 mt-1">300 Matches</div>
              <div className="text-[11px] text-neutral-400 mt-0.5">5 Agents • 15 per Pairing</div>
            </div>

            <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs">
              <div className="text-xs text-neutral-500 font-medium">Top Performer</div>
              <div className="text-xl font-bold text-purple-700 mt-1">Probabilistic Agent</div>
              <div className="text-[11px] text-purple-600 mt-0.5">46.7% Overall Win Rate</div>
            </div>

            <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs">
              <div className="text-xs text-neutral-500 font-medium">Average Match Depth</div>
              <div className="text-xl font-bold text-neutral-900 mt-1">4.2 Turns</div>
              <div className="text-[11px] text-neutral-400 mt-0.5">Prize race conclusion</div>
            </div>

            <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs">
              <div className="text-xs text-neutral-500 font-medium">Baseline Spread</div>
              <div className="text-xl font-bold text-emerald-600 mt-1">+33.4% Δ</div>
              <div className="text-[11px] text-neutral-400 mt-0.5">Probabilistic vs Random</div>
            </div>
          </div>

          {/* Tournament Charts & Head-to-Head Matrix */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Left 6 Cols: Overall Win Rates Chart */}
            <div className="lg:col-span-6 p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Overall Win Rate by Agent Architecture</h3>
                <p className="text-xs text-neutral-500">Benchmark across all 4 opposing baseline agents</p>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={tournamentChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} angle={-15} textAnchor="end" />
                    <YAxis unit="%" domain={[0, 60]} tick={{ fontSize: 11 }} />
                    <Tooltip
                      formatter={(val: number) => [`${val}%`, "Win Rate"]}
                      contentStyle={{ fontSize: "12px", borderRadius: "8px", border: "1px solid #e5e5e5" }}
                    />
                    <Bar dataKey="winRate" fill="#3b82f6" radius={[4, 4, 0, 0]}>
                      {tournamentChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.name === "PokéStrategist" ? "#7c3aed" : entry.name === "ProbabilisticAgent" ? "#2563eb" : "#94a3b8"}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Right 6 Cols: Head to Head Matrix Table */}
            <div className="lg:col-span-6 p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-3">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Head-to-Head Cross Table (Win %)</h3>
                <p className="text-xs text-neutral-500">Row Agent vs Column Opponent</p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead>
                    <tr className="border-b border-neutral-200 text-neutral-500">
                      <th className="py-2 px-2">Agent (Row)</th>
                      <th className="py-2 px-2 text-center">Random</th>
                      <th className="py-2 px-2 text-center">Greedy</th>
                      <th className="py-2 px-2 text-center">Heuristic</th>
                      <th className="py-2 px-2 text-center">Probab.</th>
                      <th className="py-2 px-2 text-center">PokéStrat.</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b border-neutral-100">
                      <td className="py-2 px-2 font-semibold text-neutral-800">Random</td>
                      <td className="py-2 px-2 text-center text-neutral-300">-</td>
                      <td className="py-2 px-2 text-center">20.0%</td>
                      <td className="py-2 px-2 text-center">6.7%</td>
                      <td className="py-2 px-2 text-center">13.3%</td>
                      <td className="py-2 px-2 text-center">13.3%</td>
                    </tr>
                    <tr className="border-b border-neutral-100">
                      <td className="py-2 px-2 font-semibold text-neutral-800">Greedy</td>
                      <td className="py-2 px-2 text-center">33.3%</td>
                      <td className="py-2 px-2 text-center text-neutral-300">-</td>
                      <td className="py-2 px-2 text-center">20.0%</td>
                      <td className="py-2 px-2 text-center">46.7%</td>
                      <td className="py-2 px-2 text-center font-bold text-emerald-600">60.0%</td>
                    </tr>
                    <tr className="border-b border-neutral-100">
                      <td className="py-2 px-2 font-semibold text-neutral-800">Heuristic</td>
                      <td className="py-2 px-2 text-center">26.7%</td>
                      <td className="py-2 px-2 text-center">33.3%</td>
                      <td className="py-2 px-2 text-center text-neutral-300">-</td>
                      <td className="py-2 px-2 text-center font-bold text-emerald-600">60.0%</td>
                      <td className="py-2 px-2 text-center">40.0%</td>
                    </tr>
                    <tr className="border-b border-neutral-100">
                      <td className="py-2 px-2 font-semibold text-neutral-800">Probabilistic</td>
                      <td className="py-2 px-2 text-center">33.3%</td>
                      <td className="py-2 px-2 text-center">46.7%</td>
                      <td className="py-2 px-2 text-center font-bold text-emerald-600">66.7%</td>
                      <td className="py-2 px-2 text-center text-neutral-300">-</td>
                      <td className="py-2 px-2 text-center">40.0%</td>
                    </tr>
                    <tr className="bg-purple-50/50">
                      <td className="py-2 px-2 font-bold text-purple-900">PokéStrategist</td>
                      <td className="py-2 px-2 text-center font-medium text-purple-950">26.7%</td>
                      <td className="py-2 px-2 text-center font-medium text-purple-950">33.3%</td>
                      <td className="py-2 px-2 text-center font-medium text-purple-950">33.3%</td>
                      <td className="py-2 px-2 text-center font-medium text-purple-950">40.0%</td>
                      <td className="py-2 px-2 text-center text-neutral-300">-</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </div>
      ) : (
        /* Ablation View */
        <div className="flex flex-col gap-6">
          <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4">
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-800">Component Ablation Study (Configurations A through F)</h3>
              <p className="text-xs text-neutral-500">Measuring isolated impact of Bayesian Opponent Modeling, Strategic Memory, and Monte Carlo Planning</p>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={ablationChartData} margin={{ top: 10, right: 10, left: -20, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis unit="%" domain={[0, 70]} tick={{ fontSize: 11 }} />
                  <Tooltip
                    formatter={(val: number) => [`${val}%`, "Win Rate"]}
                    labelFormatter={(label) => ablationChartData.find(d => d.name === label)?.fullName || label}
                    contentStyle={{ fontSize: "12px", borderRadius: "8px", border: "1px solid #e5e5e5" }}
                  />
                  <Bar dataKey="winRate" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Ablation Table Details */}
            <div className="overflow-x-auto pt-2 border-t border-neutral-100">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="border-b border-neutral-200 text-neutral-500">
                    <th className="py-2 px-2">Configuration</th>
                    <th className="py-2 px-2 text-center">Matches</th>
                    <th className="py-2 px-2 text-center">Win Rate</th>
                    <th className="py-2 px-2 text-center">Avg Prize Diff</th>
                    <th className="py-2 px-2 text-center">Avg Turns</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(ABLATION_DATA).map(([name, data]) => (
                    <tr key={name} className="border-b border-neutral-100 hover:bg-neutral-50">
                      <td className="py-2 px-2 font-medium text-neutral-800">{name}</td>
                      <td className="py-2 px-2 text-center">{data.matches}</td>
                      <td className="py-2 px-2 text-center font-bold text-neutral-900">{(data.win_rate * 100).toFixed(1)}%</td>
                      <td className="py-2 px-2 text-center text-neutral-600">{data.avg_prize_differential.toFixed(2)}</td>
                      <td className="py-2 px-2 text-center text-neutral-600">{data.avg_game_length_turns.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
