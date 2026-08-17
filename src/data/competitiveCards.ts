export interface AttackUI {
  name: string;
  cost: string[];
  damage: number;
  effect?: string;
}

export interface CardUI {
  id: string;
  name: string;
  expansion: string;
  collectionNumber: string;
  category: "Pokemon" | "Trainer" | "Energy";
  stage?: "Basic" | "Stage 1" | "Stage 2";
  hp?: number;
  energyType?: string;
  trainerType?: "Item" | "Supporter" | "Stadium" | "Tool";
  attacks?: AttackUI[];
  ability?: { name: string; effect: string };
  retreatCost?: number;
  weakness?: string;
  resistance?: string;
  isRuleBox?: boolean;
  prizeYield?: number;
  synergyTag?: string;
  imageColor?: string;
  // Derived metrics
  durability?: number;
  attackEfficiency?: number;
  tempoScore?: number;
  survivabilityIndex?: number;
}

export const SAMPLE_COMPETITIVE_CARDS: CardUI[] = [
  {
    id: "OBF-125",
    name: "Charizard ex",
    expansion: "Obsidian Flames",
    collectionNumber: "125/197",
    category: "Pokemon",
    stage: "Stage 2",
    hp: 330,
    energyType: "Darkness",
    weakness: "Grass x2",
    resistance: "None",
    retreatCost: 2,
    isRuleBox: true,
    prizeYield: 2,
    synergyTag: "Meta Flagship / Late-Game Burst",
    imageColor: "from-amber-600 to-red-800",
    durability: 330,
    attackEfficiency: 90.0,
    tempoScore: 0.85,
    survivabilityIndex: 110.0,
    ability: {
      name: "Infernal Reign",
      effect: "When you play this Pokémon from your hand to evolve 1 of your Pokémon during your turn, you may search your deck for up to 3 Basic Fire Energy and attach them to your Pokémon in any way you like."
    },
    attacks: [
      {
        name: "Burning Darkness",
        cost: ["Fire", "Fire"],
        damage: 180,
        effect: "This attack does 30 more damage for each Prize card your opponent has taken."
      }
    ]
  },
  {
    id: "SVI-081",
    name: "Miraidon ex",
    expansion: "Scarlet & Violet",
    collectionNumber: "081/198",
    category: "Pokemon",
    stage: "Basic",
    hp: 220,
    energyType: "Lightning",
    weakness: "Fighting x2",
    resistance: "None",
    retreatCost: 1,
    isRuleBox: true,
    prizeYield: 2,
    synergyTag: "Turbo Setup / Aggressive Engine",
    imageColor: "from-yellow-500 to-purple-800",
    durability: 220,
    attackEfficiency: 73.3,
    tempoScore: 0.95,
    survivabilityIndex: 88.0,
    ability: {
      name: "Tandem Unit",
      effect: "Once during your turn, you may search your deck for up to 2 Basic Lightning Pokémon and put them onto your Bench."
    },
    attacks: [
      {
        name: "Photon Blaster",
        cost: ["Lightning", "Lightning", "Colorless"],
        damage: 220,
        effect: "During your next turn, this Pokémon can't attack."
      }
    ]
  },
  {
    id: "SVI-086",
    name: "Gardevoir ex",
    expansion: "Scarlet & Violet",
    collectionNumber: "086/198",
    category: "Pokemon",
    stage: "Stage 2",
    hp: 310,
    energyType: "Psychic",
    weakness: "Darkness x2",
    resistance: "Fighting -30",
    retreatCost: 2,
    isRuleBox: true,
    prizeYield: 2,
    synergyTag: "Energy Acceleration Engine",
    imageColor: "from-emerald-500 to-teal-800",
    durability: 310,
    attackEfficiency: 63.3,
    tempoScore: 0.88,
    survivabilityIndex: 103.3,
    ability: {
      name: "Psychic Embrace",
      effect: "As often as you like during your turn, you may attach a Basic Psychic Energy from your discard pile to 1 of your Psychic Pokémon. If you do, put 2 damage counters on that Pokémon."
    },
    attacks: [
      {
        name: "Miracle Force",
        cost: ["Psychic", "Psychic", "Colorless"],
        damage: 190,
        effect: "This Pokémon recovers from all Special Conditions."
      }
    ]
  },
  {
    id: "PAR-124",
    name: "Roaring Moon ex",
    expansion: "Paradox Rift",
    collectionNumber: "124/182",
    category: "Pokemon",
    stage: "Basic",
    hp: 230,
    energyType: "Darkness",
    weakness: "Grass x2",
    resistance: "None",
    retreatCost: 2,
    isRuleBox: true,
    prizeYield: 2,
    synergyTag: "Instant One-Hit KO Striker",
    imageColor: "from-purple-700 to-slate-900",
    durability: 230,
    attackEfficiency: 73.3,
    tempoScore: 0.90,
    survivabilityIndex: 76.7,
    attacks: [
      {
        name: "Frenzied Gouging",
        cost: ["Darkness", "Darkness", "Colorless"],
        damage: 999,
        effect: "Knock Out your opponent's Active Pokémon. If your opponent's Active Pokémon is Knocked Out in this way, this Pokémon does 200 damage to itself."
      },
      {
        name: "Calamity Storm",
        cost: ["Darkness", "Darkness", "Colorless"],
        damage: 100,
        effect: "You may discard a Stadium in play. If you do, this attack does 120 more damage."
      }
    ]
  },
  {
    id: "PAL-061",
    name: "Chien-Pao ex",
    expansion: "Paldea Evolved",
    collectionNumber: "061/193",
    category: "Pokemon",
    stage: "Basic",
    hp: 220,
    energyType: "Water",
    weakness: "Metal x2",
    resistance: "None",
    retreatCost: 2,
    isRuleBox: true,
    prizeYield: 2,
    synergyTag: "Dynamic Multi-Energy Burst",
    imageColor: "from-cyan-500 to-blue-800",
    durability: 220,
    attackEfficiency: 120.0,
    tempoScore: 0.92,
    survivabilityIndex: 73.3,
    ability: {
      name: "Shiver Mountain",
      effect: "Once during your turn, if this Pokémon is in the Active Spot, you may search your deck for up to 2 Basic Water Energy cards, reveal them, and put them into your hand."
    },
    attacks: [
      {
        name: "Hail Blade",
        cost: ["Water", "Water"],
        damage: 60,
        effect: "You may discard any amount of Water Energy from your Pokémon. This attack does 60 damage for each card discarded this way."
      }
    ]
  },
  {
    id: "SIT-139",
    name: "Lugia VSTAR",
    expansion: "Silver Tempest",
    collectionNumber: "139/195",
    category: "Pokemon",
    stage: "Stage 1",
    hp: 280,
    energyType: "Colorless",
    weakness: "Lightning x2",
    resistance: "Fighting -30",
    retreatCost: 2,
    isRuleBox: true,
    prizeYield: 2,
    synergyTag: "Special Energy Assembly",
    imageColor: "from-sky-300 to-indigo-900",
    durability: 280,
    attackEfficiency: 55.0,
    tempoScore: 0.94,
    survivabilityIndex: 93.3,
    ability: {
      name: "VSTAR Power: Summoning Star",
      effect: "During your turn, you may put up to 2 Colorless Pokémon that don't have a Rule Box from your discard pile onto your Bench."
    },
    attacks: [
      {
        name: "Tempest Dive",
        cost: ["Colorless", "Colorless", "Colorless", "Colorless"],
        damage: 220,
        effect: "You may discard a Stadium in play."
      }
    ]
  },
  {
    id: "SVI-025",
    name: "Charmander",
    expansion: "Scarlet & Violet",
    collectionNumber: "025/198",
    category: "Pokemon",
    stage: "Basic",
    hp: 70,
    energyType: "Fire",
    weakness: "Water x2",
    resistance: "None",
    retreatCost: 1,
    isRuleBox: false,
    prizeYield: 1,
    synergyTag: "Basic Starter",
    imageColor: "from-orange-500 to-amber-700",
    durability: 70,
    attackEfficiency: 30.0,
    tempoScore: 0.60,
    survivabilityIndex: 46.7,
    attacks: [
      {
        name: "Ember",
        cost: ["Fire"],
        damage: 30,
        effect: "Discard an Energy attached to this Pokémon."
      }
    ]
  },
  {
    id: "SVI-026",
    name: "Charmeleon",
    expansion: "Scarlet & Violet",
    collectionNumber: "026/198",
    category: "Pokemon",
    stage: "Stage 1",
    hp: 90,
    energyType: "Fire",
    weakness: "Water x2",
    resistance: "None",
    retreatCost: 2,
    isRuleBox: false,
    prizeYield: 1,
    synergyTag: "Evolution Bridge",
    imageColor: "from-orange-600 to-red-700",
    durability: 90,
    attackEfficiency: 35.0,
    tempoScore: 0.65,
    survivabilityIndex: 45.0,
    attacks: [
      {
        name: "Slash",
        cost: ["Fire", "Colorless"],
        damage: 50
      }
    ]
  },
  {
    id: "SVI-185",
    name: "Iono",
    expansion: "Paldea Evolved",
    collectionNumber: "185/193",
    category: "Trainer",
    trainerType: "Supporter",
    synergyTag: "Disruption & Hand Refresh",
    imageColor: "from-pink-400 to-amber-400",
    isRuleBox: false,
    prizeYield: 0,
    ability: {
      name: "Supporter Effect",
      effect: "Each player shuffles their hand and puts it on the bottom of their deck. If either player put any cards on the bottom of their deck in this way, each player draws a card for each of their remaining Prize cards."
    }
  },
  {
    id: "SVI-189",
    name: "Professor's Research",
    expansion: "Scarlet & Violet",
    collectionNumber: "189/198",
    category: "Trainer",
    trainerType: "Supporter",
    synergyTag: "Maximum Velocity Draw",
    imageColor: "from-blue-600 to-indigo-800",
    isRuleBox: false,
    prizeYield: 0,
    ability: {
      name: "Supporter Effect",
      effect: "Discard your hand and draw 7 cards."
    }
  },
  {
    id: "PAL-172",
    name: "Boss's Orders (Ghetsis)",
    expansion: "Paldea Evolved",
    collectionNumber: "172/193",
    category: "Trainer",
    trainerType: "Supporter",
    synergyTag: "Gust / Bench Targeting",
    imageColor: "from-red-700 to-slate-900",
    isRuleBox: false,
    prizeYield: 0,
    ability: {
      name: "Supporter Effect",
      effect: "Switch in 1 of your opponent's Benched Pokémon to the Active Spot."
    }
  },
  {
    id: "TEF-157",
    name: "Prime Catcher",
    expansion: "Temporal Forces",
    collectionNumber: "157/162",
    category: "Trainer",
    trainerType: "Item",
    synergyTag: "ACE SPEC / Double Gust Pivot",
    imageColor: "from-rose-600 to-purple-900",
    isRuleBox: true,
    prizeYield: 0,
    ability: {
      name: "ACE SPEC Item",
      effect: "Switch in 1 of your opponent's Benched Pokémon to the Active Spot. If you do, switch your Active Pokémon with 1 of your Benched Pokémon."
    }
  },
  {
    id: "SVI-196",
    name: "Ultra Ball",
    expansion: "Scarlet & Violet",
    collectionNumber: "196/198",
    category: "Trainer",
    trainerType: "Item",
    synergyTag: "Universal Pokémon Tutor",
    imageColor: "from-neutral-700 to-amber-600",
    isRuleBox: false,
    prizeYield: 0,
    ability: {
      name: "Item Effect",
      effect: "You can use this card only if you discard 2 other cards from your hand. Search your deck for a Pokémon, reveal it, and put it into your hand. Then, shuffle your deck."
    }
  },
  {
    id: "SVI-181",
    name: "Nest Ball",
    expansion: "Scarlet & Violet",
    collectionNumber: "181/198",
    category: "Trainer",
    trainerType: "Item",
    synergyTag: "Basic Bench Setup",
    imageColor: "from-emerald-600 to-teal-700",
    isRuleBox: false,
    prizeYield: 0,
    ability: {
      name: "Item Effect",
      effect: "Search your deck for a Basic Pokémon and put it onto your Bench. Then, shuffle your deck."
    }
  },
  {
    id: "SVI-E01",
    name: "Basic Fire Energy",
    expansion: "Scarlet & Violet",
    collectionNumber: "Energy",
    category: "Energy",
    energyType: "Fire",
    synergyTag: "Energy Fuel",
    imageColor: "from-red-500 to-orange-600",
    isRuleBox: false,
    prizeYield: 0
  },
  {
    id: "SVI-E02",
    name: "Basic Water Energy",
    expansion: "Scarlet & Violet",
    collectionNumber: "Energy",
    category: "Energy",
    energyType: "Water",
    synergyTag: "Energy Fuel",
    imageColor: "from-blue-400 to-cyan-600",
    isRuleBox: false,
    prizeYield: 0
  },
  {
    id: "SVI-E03",
    name: "Basic Lightning Energy",
    expansion: "Scarlet & Violet",
    collectionNumber: "Energy",
    category: "Energy",
    energyType: "Lightning",
    synergyTag: "Energy Fuel",
    imageColor: "from-yellow-400 to-amber-500",
    isRuleBox: false,
    prizeYield: 0
  },
  {
    id: "SVI-E04",
    name: "Basic Darkness Energy",
    expansion: "Scarlet & Violet",
    collectionNumber: "Energy",
    category: "Energy",
    energyType: "Darkness",
    synergyTag: "Energy Fuel",
    imageColor: "from-slate-700 to-purple-950",
    isRuleBox: false,
    prizeYield: 0
  }
];

export const ARCHETYPE_INFO = [
  {
    id: "Aggressive / Turbo",
    title: "Aggressive / Turbo",
    icon: "Zap",
    color: "text-amber-600 bg-amber-50 border-amber-200",
    description: "High early velocity, aiming for Turn 1/2 Prize knockouts with high damage basic rule-box attackers.",
    keyCards: ["Miraidon ex", "Roaring Moon ex", "Prime Catcher", "Professor's Research"],
    expectedTurnToAttack: 1,
    riskTolerance: 0.85
  },
  {
    id: "Stage 2 Engine / Setup",
    title: "Stage 2 Engine / Setup",
    icon: "Layers",
    color: "text-red-600 bg-red-50 border-red-200",
    description: "Sacrifices early momentum to search Rare Candies & evolution lines for massive mid/late game dominance.",
    keyCards: ["Charizard ex", "Gardevoir ex", "Rare Candy", "Ultra Ball", "Arven"],
    expectedTurnToAttack: 3,
    riskTolerance: 0.45
  },
  {
    id: "Control / Disruption",
    title: "Control / Disruption",
    icon: "ShieldAlert",
    color: "text-purple-600 bg-purple-50 border-purple-200",
    description: "Locks abilities, discards opponent energies, attacks hand size with Iono & Path to Peak.",
    keyCards: ["Iono", "Crushing Hammer", "Miss Fortune Sisters", "Ericka's Invitation"],
    expectedTurnToAttack: 4,
    riskTolerance: 0.20
  },
  {
    id: "Single-Target Burst",
    title: "Single-Target Burst",
    icon: "Target",
    color: "text-blue-600 bg-blue-50 border-blue-200",
    description: "Multiplies damage output based on discarded energy or damage counters to eliminate 300+ HP Pokémon in one turn.",
    keyCards: ["Chien-Pao ex", "Baxcalibur", "Superior Energy Retrieval"],
    expectedTurnToAttack: 2,
    riskTolerance: 0.65
  },
  {
    id: "Spread / Bench Snipe",
    title: "Spread / Bench Snipe",
    icon: "Crosshair",
    color: "text-teal-600 bg-teal-50 border-teal-200",
    description: "Bypasses the active Pokémon to place damage counters on vulnerable benched support Pokémon.",
    keyCards: ["Sableye", "Radiant Greninja", "Lost Vacuum", "Colress's Experiment"],
    expectedTurnToAttack: 3,
    riskTolerance: 0.50
  },
  {
    id: "Defensive / Tank",
    title: "Defensive / Tank",
    icon: "Shield",
    color: "text-emerald-600 bg-emerald-50 border-emerald-200",
    description: "Maximizes HP, attaches damage-reduction tools (Hero's Cape, Rigid Band), and loops healing Supporters.",
    keyCards: ["Goodra VSTAR", "Blissey ex", "Hero's Cape", "Cheren's Care"],
    expectedTurnToAttack: 2,
    riskTolerance: 0.35
  },
  {
    id: "Energy Acceleration",
    title: "Energy Acceleration",
    icon: "Sparkles",
    color: "text-cyan-600 bg-cyan-50 border-cyan-200",
    description: "Attaches multiple energies per turn directly from discard pile or deck to out-tempo the normal 1-energy-per-turn cap.",
    keyCards: ["Archeops", "Lugia VSTAR", "Dark Patch", "Electric Generator"],
    expectedTurnToAttack: 2,
    riskTolerance: 0.60
  },
  {
    id: "Balanced / Midrange",
    title: "Balanced / Midrange",
    icon: "Scale",
    color: "text-indigo-600 bg-indigo-50 border-indigo-200",
    description: "Flexible game plan adapting between aggressive tempo and defensive prize management based on matchup.",
    keyCards: ["Pidgeot ex", "Rotom V", "Boss's Orders", "Super Rod"],
    expectedTurnToAttack: 2,
    riskTolerance: 0.50
  }
];
