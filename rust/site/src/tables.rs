//! The site's section styles, folder paintings and crests.

/// (key, hue, deep, painted art, tagline)
pub type Style = (&'static str, &'static str, &'static str, &'static str, &'static str);

pub const SECTIONS: &[(&str, Style)] = &[
    (r##"The Magic System"##, (r##"magic"##, r##"#8a5cf0"##, r##"#1a0f2e"##, r##"magic"##, r##"Sixteen Stages, sixty Wellsprings, and the bill for every working."##)),
    (r##"Races & Peoples"##, (r##"peoples"##, r##"#e0a24a"##, r##"#24170a"##, r##"peoples"##, r##"The peoples of the realms: their tongues, their blood, their ways."##)),
    (r##"Factions, Bloodlines & Institutions"##, (r##"factions"##, r##"#d0453a"##, r##"#2a0c0b"##, r##"factions"##, r##"Crowns, guilds, orders and the old blood that owns them."##)),
    (r##"Geography & the Four Quarters"##, (r##"geography"##, r##"#3fb59a"##, r##"#08201b"##, r##"geography"##, r##"Four Quarters, two worlds, and the roads and coin between them."##)),
    (r##"Cosmology & Metaphysics"##, (r##"cosmology"##, r##"#5b8ff0"##, r##"#0a1430"##, r##"cosmology"##, r##"Titans, Archons, the Veil and the ages of the world."##)),
    (r##"The Bestiary"##, (r##"bestiary"##, r##"#c43a5a"##, r##"#250a12"##, r##"bestiary"##, r##"What hunts the dark, and what the Wells spawn into it."##)),
    (r##"Lore & History"##, (r##"lore"##, r##"#d8ab4f"##, r##"#21180a"##, r##"lore"##, r##"The chronicles, the codices, and what the record keeps."##)),
    (r##"Materials, Alchemy & Trade"##, (r##"materials"##, r##"#46c27a"##, r##"#0a2014"##, r##"alchemy"##, r##"Ores, Drafts, prepared tags and the price of everything."##)),
    (r##"The War Cycle"##, (r##"war"##, r##"#e2603a"##, r##"#2a0f06"##, r##"war-cycle"##, r##"How a war is paid for, marched, fought, survived and buried."##)),
];

pub const DEFAULT: Style = (r##"crown"##, r##"#d8ab4f"##, r##"#1c140b"##, r##"hero"##, r##""##);

/// A folder's own painting (wiki/Assets/Paintings/<name>.webp), over its section's.
pub const FOLDER_ART: &[(&str, &str)] = &[
    (r##"The Magic System/First Steps"##, r##"first-steps"##),
    (r##"The Magic System/The Foundations"##, r##"foundations"##),
    (r##"The Magic System/The Soul and the Climb"##, r##"soul-climb"##),
    (r##"The Magic System/Power in Use"##, r##"power-in-use"##),
    (r##"The Magic System/Practice and Institution"##, r##"practice-institution"##),
    (r##"The Magic System/Reference and Craft"##, r##"reference-craft"##),
    (r##"The Magic System/Fracture of Worlds — The Living System"##, r##"fracture-worlds"##),
    (r##"The Magic System/The Foundations/The Eight Families & the Sixty Wellsprings"##, r##"eight-families"##),
    (r##"The Magic System/The Foundations/The Descent of Parun — The Fourteen Hands"##, r##"descent-parun"##),
    (r##"Factions, Bloodlines & Institutions/Powers and Polities"##, r##"powers-polities"##),
    (r##"Factions, Bloodlines & Institutions/Powers and Polities/The Guild Accord"##, r##"guild-accord"##),
    (r##"Factions, Bloodlines & Institutions/Houses and Bloodlines"##, r##"houses-bloodlines"##),
    (r##"Factions, Bloodlines & Institutions/Houses and Bloodlines/The Archaic Bloodlines"##, r##"houses-bloodlines"##),
    (r##"Factions, Bloodlines & Institutions/Houses and Bloodlines/The Archaic Bloodlines/The Moto Bloodline"##, r##"moto"##),
    (r##"Factions, Bloodlines & Institutions/Houses and Bloodlines/The Archaic Bloodlines/The Zettari"##, r##"zettari"##),
    (r##"Factions, Bloodlines & Institutions/Orders, Faiths and Cults"##, r##"orders-faiths"##),
    (r##"Geography & the Four Quarters/The Bearing and the Holding"##, r##"bearing-holding"##),
    (r##"Geography & the Four Quarters/The Bearing and the Holding/The Inner World — The Northern Shield"##, r##"northern-shield"##),
    (r##"Geography & the Four Quarters/Value, Coin and Trade"##, r##"coin-trade"##),
    (r##"Races & Peoples/The Peoples/The Dawi Peoples"##, r##"dawi"##),
    (r##"Races & Peoples/The Peoples/The Elven Peoples"##, r##"elven"##),
    (r##"Races & Peoples/The Peoples/The Beastkin and Demihuman Peoples"##, r##"beastkin"##),
    (r##"Races & Peoples/The Tongues of the Realms"##, r##"tongues"##),
    (r##"Races & Peoples/The Tongues of the Realms/The Grammars"##, r##"tongues"##),
    (r##"Races & Peoples/The Tongues of the Realms/Naming and Usage"##, r##"tongues"##),
    (r##"Factions, Bloodlines & Institutions/Powers and Polities/The Guild Accord/Structure and Rank"##, r##"practice-institution"##),
    (r##"Factions, Bloodlines & Institutions/Powers and Polities/The Guild Accord/Seats and Arms"##, r##"guild-accord"##),
    (r##"Cosmology & Metaphysics/The Making of the World"##, r##"making-world"##),
    (r##"Cosmology & Metaphysics/Faith and the Powers Above"##, r##"archons"##),
    (r##"Cosmology & Metaphysics/Faith and the Powers Above/The Fourteen Archons"##, r##"archons"##),
    (r##"Cosmology & Metaphysics/Faith and the Powers Above/The Fourteen Titans"##, r##"titans"##),
    (r##"Cosmology & Metaphysics/Ages and Reckoning"##, r##"ages-reckoning"##),
    (r##"The Bestiary/The Wild"##, r##"natural-beasts"##),
    (r##"The Bestiary/The Wild/Natural Beasts"##, r##"natural-beasts"##),
    (r##"The Bestiary/The Corrupted and the Risen"##, r##"aberrations"##),
    (r##"The Bestiary/The Corrupted and the Risen/Aberrations"##, r##"aberrations"##),
    (r##"The Bestiary/The Called and the Divine"##, r##"summoned"##),
    (r##"The Bestiary/The Called and the Divine/Summoned and Bound"##, r##"summoned"##),
    (r##"Lore & History/The Alftian Codex"##, r##"alftian"##),
    (r##"Materials, Alchemy & Trade/Materials"##, r##"material-ledger"##),
    (r##"Materials, Alchemy & Trade/Materials/The Master Material Ledger"##, r##"material-ledger"##),
    (r##"Materials, Alchemy & Trade/Alchemy"##, r##"alchemy"##),
    (r##"Materials, Alchemy & Trade/Work, Trade and Measure"##, r##"coin-trade"##),
    (r##"The War Cycle/The Wounded and the Dead"##, r##"wounded-dead"##),
    (r##"The War Cycle/The Army"##, r##"war-cycle"##),
    (r##"The War Cycle/The Fighting"##, r##"war-cycle"##),
];

/// Drawn on a 200x200 box centred at (100,100); stroke-only, painted with currentColor.
pub const CRESTS: &[(&str, &str)] = &[
    (r##"magic"##, r##"
      <circle cx="100" cy="100" r="86"/><circle cx="100" cy="100" r="74" stroke-dasharray="2 5"/>
      <polygon points="100,22 167,139 33,139"/><polygon points="100,178 33,61 167,61"/>
      <circle cx="100" cy="100" r="30"/><polygon points="100,78 119,100 100,122 81,100" fill="currentColor" fill-opacity=".35"/>
      <circle cx="100" cy="22" r="5"/><circle cx="167" cy="139" r="5"/><circle cx="33" cy="139" r="5"/>"##),
    (r##"peoples"##, r##"
      <circle cx="78" cy="84" r="44"/><circle cx="122" cy="84" r="44"/><circle cx="100" cy="122" r="44"/>
      <circle cx="100" cy="97" r="8" fill="currentColor" fill-opacity=".45"/>
      <path d="M30 172 Q100 150 170 172" stroke-dasharray="3 5"/>"##),
    (r##"factions"##, r##"
      <path d="M100 26 L160 46 L160 104 Q160 150 100 178 Q40 150 40 104 L40 46 Z"/>
      <path d="M100 38 L150 54 L150 104 Q150 142 100 166 Q50 142 50 104 L50 54 Z" stroke-opacity=".5"/>
      <path d="M58 118 L100 82 L142 118"/><path d="M58 136 L100 100 L142 136"/>
      <path d="M78 14 L84 26 L92 16 L100 26 L108 16 L116 26 L122 14" />"##),
    (r##"geography"##, r##"
      <circle cx="100" cy="100" r="80"/><circle cx="100" cy="100" r="62" stroke-dasharray="1 4"/>
      <polygon points="100,12 110,90 100,100 90,90" fill="currentColor" fill-opacity=".55"/>
      <polygon points="100,188 110,110 100,100 90,110"/>
      <polygon points="12,100 90,90 100,100 90,110"/><polygon points="188,100 110,110 100,100 110,90" fill="currentColor" fill-opacity=".55"/>
      <polygon points="40,40 96,94 100,100 94,96" /><polygon points="160,160 104,106 100,100 106,104"/>
      <polygon points="160,40 106,96 100,100 104,94"/><polygon points="40,160 94,104 100,100 96,106"/>"##),
    (r##"cosmology"##, r##"
      <circle cx="100" cy="100" r="16" fill="currentColor" fill-opacity=".45"/>
      <ellipse cx="100" cy="100" rx="84" ry="30" transform="rotate(-24 100 100)"/>
      <ellipse cx="100" cy="100" rx="84" ry="30" transform="rotate(36 100 100)"/>
      <ellipse cx="100" cy="100" rx="56" ry="56" stroke-dasharray="2 6"/>
      <circle cx="176" cy="66" r="6" fill="currentColor"/><circle cx="34" cy="62" r="4" fill="currentColor"/>
      <circle cx="129" cy="149" r="5" fill="currentColor"/>"##),
    (r##"bestiary"##, r##"
      <path d="M100 18 L182 100 L100 182 L18 100 Z"/>
      <path d="M40 100 Q100 44 160 100 Q100 156 40 100 Z"/>
      <ellipse cx="100" cy="100" rx="9" ry="30" fill="currentColor" fill-opacity=".6"/>
      <path d="M58 30 Q70 60 62 86"/><path d="M76 22 Q88 54 80 82"/><path d="M142 170 Q130 140 138 114"/><path d="M124 178 Q112 146 120 118"/>"##),
    (r##"lore"##, r##"
      <path d="M100 150 Q70 128 26 134 L26 58 Q70 52 100 74 Q130 52 174 58 L174 134 Q130 128 100 150 Z"/>
      <path d="M100 74 L100 150"/><path d="M40 76 Q66 72 88 84"/><path d="M40 92 Q66 88 88 100"/><path d="M40 108 Q66 104 88 116"/>
      <path d="M160 76 Q134 72 112 84"/><path d="M160 92 Q134 88 112 100"/><path d="M160 108 Q134 104 112 116"/>
      <path d="M100 58 L100 20"/><path d="M78 56 L60 26"/><path d="M122 56 L140 26"/><path d="M58 64 L28 44"/><path d="M142 64 L172 44"/>"##),
    (r##"materials"##, r##"
      <circle cx="100" cy="130" r="48"/><path d="M86 84 L86 30 L114 30 L114 84"/><path d="M78 30 L122 30"/>
      <path d="M58 140 Q100 120 142 140" stroke-opacity=".6"/>
      <polygon points="100,108 120,144 80,144" fill="currentColor" fill-opacity=".35"/>
      <circle cx="132" cy="56" r="5"/><circle cx="146" cy="40" r="3"/><circle cx="66" cy="60" r="4"/>"##),
    (r##"war"##, r##"
      <path d="M40 40 L150 150"/><path d="M160 40 L50 150"/>
      <path d="M32 32 L44 36 L40 48"/><path d="M168 32 L156 36 L160 48"/>
      <path d="M138 162 L162 138"/><path d="M38 138 L62 162"/>
      <polygon points="100,62 116,84 140,84 128,106 136,130 100,118 64,130 72,106 60,84 84,84" fill="currentColor" fill-opacity=".25"/>
      <circle cx="100" cy="100" r="14"/>"##),
    (r##"crown"##, r##"
      <path d="M38 140 L30 66 L68 100 L100 46 L132 100 L170 66 L162 140 Z"/>
      <path d="M38 156 L162 156"/><circle cx="100" cy="46" r="7" fill="currentColor"/><circle cx="30" cy="66" r="5"/><circle cx="170" cy="66" r="5"/>
      <polygon points="100,104 112,120 100,136 88,120" fill="currentColor" fill-opacity=".45"/>"##),
];
