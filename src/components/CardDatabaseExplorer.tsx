import React, { useState, useMemo } from "react";
import { SAMPLE_COMPETITIVE_CARDS, CardUI } from "../data/competitiveCards";
import { Search, Filter, Layers, Zap, Shield, Sparkles, SlidersHorizontal, Info, Award } from "lucide-react";

export const CardDatabaseExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<string>("All");
  const [energyFilter, setEnergyFilter] = useState<string>("All");
  const [selectedCard, setSelectedCard] = useState<CardUI>(SAMPLE_COMPETITIVE_CARDS[0]);

  const filteredCards = useMemo(() => {
    return SAMPLE_COMPETITIVE_CARDS.filter(card => {
      const matchSearch = card.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          card.expansion.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (card.synergyTag && card.synergyTag.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchCat = categoryFilter === "All" || card.category === categoryFilter;
      const matchEnergy = energyFilter === "All" || card.energyType === energyFilter;
      return matchSearch && matchCat && matchEnergy;
    });
  }, [searchTerm, categoryFilter, energyFilter]);

  return (
    <div id="card-db-root" className="flex flex-col gap-6">
      {/* Search & Filter Header */}
      <div className="p-4 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative w-full md:w-72">
            <Search className="w-4 h-4 text-neutral-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              id="card-search-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by card name, set, or synergy..."
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-neutral-50 border border-neutral-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white transition-all"
            />
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {/* Category */}
          <div className="flex items-center gap-1 text-xs">
            <span className="text-neutral-500">Category:</span>
            {["All", "Pokemon", "Trainer", "Energy"].map((cat) => (
              <button
                key={`cat-filter-${cat}`}
                onClick={() => setCategoryFilter(cat)}
                className={`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                  categoryFilter === cat
                    ? "bg-neutral-900 text-white"
                    : "bg-neutral-100 text-neutral-700 hover:bg-neutral-200"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Energy */}
          <div className="flex items-center gap-1 text-xs ml-2">
            <span className="text-neutral-500">Energy:</span>
            <select
              value={energyFilter}
              onChange={(e) => setEnergyFilter(e.target.value)}
              className="px-2 py-1 bg-neutral-100 border border-neutral-200 rounded-md text-xs font-medium text-neutral-700 focus:outline-none"
            >
              <option value="All">All Types</option>
              <option value="Fire">Fire</option>
              <option value="Water">Water</option>
              <option value="Lightning">Lightning</option>
              <option value="Psychic">Psychic</option>
              <option value="Darkness">Darkness</option>
              <option value="Colorless">Colorless</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Grid: Card Grid & Selected Card Inspection */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 7 Cols: Card List */}
        <div className="lg:col-span-7 flex flex-col gap-3">
          <div className="flex items-center justify-between text-xs text-neutral-500">
            <span>Showing {filteredCards.length} Standard Legal Cards</span>
            <span>Click any card to inspect derived intelligence metrics</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-[600px] overflow-y-auto pr-1">
            {filteredCards.map((card) => {
              const isSelected = card.id === selectedCard.id;
              return (
                <div
                  key={card.id}
                  onClick={() => setSelectedCard(card)}
                  className={`p-3 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                    isSelected
                      ? "border-blue-500 bg-blue-50/30 shadow-xs ring-1 ring-blue-400"
                      : "border-neutral-200 bg-white hover:border-neutral-300"
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                        card.category === "Pokemon" ? "bg-amber-100 text-amber-800" :
                        card.category === "Trainer" ? "bg-purple-100 text-purple-800" : "bg-red-100 text-red-800"
                      }`}>
                        {card.stage || card.trainerType || card.category}
                      </span>
                      {card.isRuleBox && (
                        <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                          RULE BOX
                        </span>
                      )}
                    </div>

                    <h4 className="font-semibold text-xs text-neutral-900 truncate">{card.name}</h4>
                    <span className="text-[11px] text-neutral-500">{card.expansion} • {card.collectionNumber}</span>
                  </div>

                  {card.category === "Pokemon" && (
                    <div className="mt-3 pt-2 border-t border-neutral-100 flex items-center justify-between text-xs">
                      <span className="font-bold text-neutral-800">{card.hp} HP</span>
                      <span className="text-[11px] text-neutral-500">
                        {card.attacks?.[0] ? `${card.attacks[0].name} (${card.attacks[0].damage} DMG)` : "Ability Engine"}
                      </span>
                    </div>
                  )}

                  {card.synergyTag && (
                    <div className="mt-2 text-[10px] text-neutral-500 bg-neutral-50 p-1 rounded truncate">
                      {card.synergyTag}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Right 5 Cols: Deep Feature Inspection */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          <div className="p-5 rounded-xl border border-neutral-200 bg-white shadow-xs flex flex-col gap-4 sticky top-4">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wide">Card Intelligence Profile</span>
                <h3 className="text-base font-bold text-neutral-900 mt-0.5">{selectedCard.name}</h3>
                <p className="text-xs text-neutral-500">{selectedCard.expansion} • #{selectedCard.collectionNumber}</p>
              </div>

              {selectedCard.hp && (
                <div className="text-right">
                  <div className="text-base font-extrabold text-neutral-900">{selectedCard.hp} HP</div>
                  <span className="text-xs text-neutral-500">{selectedCard.energyType}</span>
                </div>
              )}
            </div>

            {/* Strategic Feature Radar / Metrics */}
            {selectedCard.category === "Pokemon" && (
              <div className="grid grid-cols-3 gap-2 text-center text-xs">
                <div className="p-2.5 rounded-lg bg-neutral-50 border border-neutral-100">
                  <div className="text-[10px] text-neutral-400">Attack Eff.</div>
                  <div className="font-bold text-blue-600 mt-0.5">{selectedCard.attackEfficiency?.toFixed(1) || "N/A"}</div>
                  <div className="text-[9px] text-neutral-400">DMG / Energy</div>
                </div>

                <div className="p-2.5 rounded-lg bg-neutral-50 border border-neutral-100">
                  <div className="text-[10px] text-neutral-400">Survivability</div>
                  <div className="font-bold text-emerald-600 mt-0.5">{selectedCard.survivabilityIndex?.toFixed(1) || "N/A"}</div>
                  <div className="text-[9px] text-neutral-400">HP / Prize</div>
                </div>

                <div className="p-2.5 rounded-lg bg-neutral-50 border border-neutral-100">
                  <div className="text-[10px] text-neutral-400">Tempo Score</div>
                  <div className="font-bold text-purple-600 mt-0.5">{selectedCard.tempoScore?.toFixed(2) || "N/A"}</div>
                  <div className="text-[9px] text-neutral-400">0.0 - 1.0</div>
                </div>
              </div>
            )}

            {/* Abilities */}
            {selectedCard.ability && (
              <div className="p-3 rounded-lg bg-amber-50/50 border border-amber-200 text-xs">
                <div className="font-bold text-amber-900 mb-1 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                  Ability: {selectedCard.ability.name}
                </div>
                <p className="text-[11px] text-neutral-700 leading-relaxed">{selectedCard.ability.effect}</p>
              </div>
            )}

            {/* Attacks */}
            {selectedCard.attacks && selectedCard.attacks.length > 0 && (
              <div className="space-y-2">
                <span className="text-xs font-semibold text-neutral-800">Attacks</span>
                {selectedCard.attacks.map((atk, idx) => (
                  <div key={`atk-${idx}`} className="p-3 rounded-lg bg-neutral-50 border border-neutral-200 text-xs">
                    <div className="flex items-center justify-between font-semibold text-neutral-900 mb-1">
                      <div className="flex items-center gap-1.5">
                        <span className="font-bold">{atk.name}</span>
                        <div className="flex gap-0.5">
                          {atk.cost.map((c, i) => (
                            <span key={i} className="text-[9px] px-1 bg-neutral-200 rounded font-medium">{c}</span>
                          ))}
                        </div>
                      </div>
                      <span className="text-red-600 font-bold">{atk.damage} DMG</span>
                    </div>
                    {atk.effect && <p className="text-[11px] text-neutral-600 mt-1">{atk.effect}</p>}
                  </div>
                ))}
              </div>
            )}

            {/* Tactical Archetype Synergy */}
            <div className="p-3 rounded-lg bg-neutral-50 border border-neutral-200 text-xs">
              <div className="font-semibold text-neutral-800 mb-1 flex items-center gap-1.5">
                <Award className="w-3.5 h-3.5 text-neutral-500" />
                Archetype Synergy & Role:
              </div>
              <p className="text-[11px] text-neutral-600 leading-relaxed">
                {selectedCard.synergyTag || "Standard baseline component supporting generic deck consistency and resource cycling."}
              </p>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
};
