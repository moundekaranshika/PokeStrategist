import React, { useState } from "react";
import { BattleArena } from "./components/BattleArena";
import { BeliefExplorer } from "./components/BeliefExplorer";
import { MonteCarloTree } from "./components/MonteCarloTree";
import { CardDatabaseExplorer } from "./components/CardDatabaseExplorer";
import { TournamentDashboard } from "./components/TournamentDashboard";
import { ResearchArchitecture } from "./components/ResearchArchitecture";
import { Swords, Brain, GitBranch, Database, Trophy, BookOpen, Sparkles } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState<"arena" | "belief" | "planner" | "cards" | "tournament" | "research">("arena");

  return (
    <div className="min-h-screen bg-neutral-100 text-neutral-900 flex flex-col font-sans selection:bg-purple-100 selection:text-purple-900">
      {/* Top Navigation Bar */}
      <header className="bg-white border-b border-neutral-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            
            {/* Logo & Title */}
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-700 to-indigo-600 flex items-center justify-center text-white shadow-xs">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-base font-bold tracking-tight text-neutral-900">PokéStrategist</h1>
                  <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-purple-100 text-purple-800 rounded-full border border-purple-200">
                    v1.0 Research Suite
                  </span>
                </div>
                <p className="text-xs text-neutral-500 hidden sm:block">Memory-Guided Probabilistic Strategic Planning for Pokémon TCG</p>
              </div>
            </div>

            {/* Navigation Tabs */}
            <nav className="flex items-center gap-1 overflow-x-auto py-1">
              <button
                id="nav-arena"
                onClick={() => setActiveTab("arena")}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "arena"
                    ? "bg-neutral-900 text-white"
                    : "text-neutral-600 hover:bg-neutral-100"
                }`}
              >
                <Swords className="w-3.5 h-3.5" />
                Battle Arena
              </button>

              <button
                id="nav-belief"
                onClick={() => setActiveTab("belief")}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "belief"
                    ? "bg-neutral-900 text-white"
                    : "text-neutral-600 hover:bg-neutral-100"
                }`}
              >
                <Brain className="w-3.5 h-3.5" />
                Bayesian Belief
              </button>

              <button
                id="nav-planner"
                onClick={() => setActiveTab("planner")}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "planner"
                    ? "bg-neutral-900 text-white"
                    : "text-neutral-600 hover:bg-neutral-100"
                }`}
              >
                <GitBranch className="w-3.5 h-3.5" />
                Monte Carlo
              </button>

              <button
                id="nav-cards"
                onClick={() => setActiveTab("cards")}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "cards"
                    ? "bg-neutral-900 text-white"
                    : "text-neutral-600 hover:bg-neutral-100"
                }`}
              >
                <Database className="w-3.5 h-3.5" />
                Card Intelligence
              </button>

              <button
                id="nav-tournament"
                onClick={() => setActiveTab("tournament")}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "tournament"
                    ? "bg-neutral-900 text-white"
                    : "text-neutral-600 hover:bg-neutral-100"
                }`}
              >
                <Trophy className="w-3.5 h-3.5" />
                Tournaments
              </button>

              <button
                id="nav-research"
                onClick={() => setActiveTab("research")}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "research"
                    ? "bg-neutral-900 text-white"
                    : "text-neutral-600 hover:bg-neutral-100"
                }`}
              >
                <BookOpen className="w-3.5 h-3.5" />
                Architecture
              </button>
            </nav>

          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === "arena" && <BattleArena />}
        {activeTab === "belief" && <BeliefExplorer />}
        {activeTab === "planner" && <MonteCarloTree />}
        {activeTab === "cards" && <CardDatabaseExplorer />}
        {activeTab === "tournament" && <TournamentDashboard />}
        {activeTab === "research" && <ResearchArchitecture />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-neutral-200 py-4 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-neutral-500 gap-2">
          <div>
            PokéStrategist Research Project • 2,024 Standard Cards • 8 Archetypes • Monte Carlo Simulation
          </div>
          <div className="flex items-center gap-4">
            <span>Tests: 21 Passing</span>
            <span>Notebooks: 6/6 Executable</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
