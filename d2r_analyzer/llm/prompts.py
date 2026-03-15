ITEM_EXTRACTION_PROMPT = """
You are analyzing a Diablo 2 Resurrected item tooltip screenshot.

Extract ALL visible item information and return ONLY valid JSON.
No explanation, no markdown, no code blocks. Raw JSON only.

Be super accurate about the quality can be normal, magic, rare, set, unique, or crafted:
─── QUALITY DETECTION — USE ALL 3 SIGNALS ───────────────────────────────────

Signal 1 — TEXT COLOR of the item name at the top:
  White/grey text   → normal
  Blue text         → magic
  Yellow text       → rare
  Green text        → set
  Brown text   → unique
  Orange text       → crafted

Signal 2 — NUMBER OF AFFIXES (most reliable signal):
  1-2 affixes total → almost certainly magic (blue)
  3-6 affixes total → almost certainly rare (yellow)
  Fixed known stats → unique or set

Signal 3 — ITEM NAME STRUCTURE:
  Single generic word ("Ring", "Amulet")              → normal or magic
  Two random fantasy words ("Cruel Noose")             → rare
  A known D2 unique name ("Nagelring", "Stone of Jordan") → unique
  Has a set label below name                           → set

PRIORITY: If signals conflict, trust Signal 2 (affix count) over color.
A magic item can NEVER have more than 2 affixes.
A rare item always has between 3 and 6 affixes.

The "base_type" field MUST be one of these exact values (lowercase):
  grand charm, small charm, large charm, amulet, ring, helmet, armor,
  shield, weapon, gloves, boots, belt

The "affixes/stat" field MUST be one of these exact values (lowercase):
  all_resistances, fire_resist, cold_resist, lightning_resist, poison_resist,
  life, mana, strength, lightning_skills, fire_skills, cold_skills, martial_arts, 
  warcries, traps, elemental_skills, summoning_skills, javelin_and_spear_skills, 
  faster_hit_recovery, attack_rating, better_chance_of_getting_magic_items, faster_cast_rate, 
  faster_run_walk, fire_damage, enhanced_defense, defense, regenerate_mana, all_skills, all_attributes, 
  physical_damage_received_reduction, increase_maximum_mana, lightning_damage, poison_damage, poison_nova,
  blood_golem, damage_reduced, combat_skills, maximum_damage, damage_to_undead, enhanced_damage,
  cold_damage, life_stolen_per_hit, repair_durability, increased_attack_speed, damage_to_demons, attack_rating_against_demons

Stat mapping examples (use these exact keys):
  "+X to All Skills"               → all_skills
  "+X to All Attributes"           → all_attributes
  "+X% to All Resistances"         → all_resistances
  "+X% Faster Cast Rate"           → faster_cast_rate
  "+X% Increased Attack Speed"     → increased_attack_speed
  "+X% Faster Hit Recovery"        → faster_hit_recovery
  "+X% Faster Run/Walk"            → faster_run_walk
  "+X% Better Chance of Magic"     → better_chance_of_getting_magic_items
  "+X to Lightning Skills"         → lightning_skills
  "+X to Fire Skills"              → fire_skills
  "+X to Cold Skills"              → cold_skills
  "+X to Martial Arts"             → martial_arts
  "+X to Warcries"                 → warcries
  "Adds X-Y Poison Damage"         → poison_damage (use average of range for value)
  "+X% Life Stolen Per Hit"        → life_stolen_per_hit
  "Repairs X Durability"           → repair_durability
If the item's base type is not in this list, pick the closest match.

Return this exact structure:
{
  "name": "item name or null if magic/rare with no name",
  "name_color": "white | grey | blue | yellow | green | brown | orange",
  "base_type": "must be one of the allowed values listed above",
  "quality": "normal | magic | rare | set | unique | crafted",
  "item_level": 85,
  "required_level": 60,
  "affixes": [
    {
      "raw_text": "+10% Faster Cast Rate",
      "stat": "faster_cast_rate",
      "value": 10,
      "unit": "%"
    }
  ],
  "sockets": 0,
  "is_ethereal": false,
  "defense": null,
  "damage": null
}

name_color mapping:
  white or grey → normal
  blue          → magic
  yellow        → rare
  green         → set
  brown         → unique
  orange        → crafted

Rules:
- Extract EVERY stat line visible, even if you don't recognize it
- is_ethereal is true if the word "Ethereal" appears
- If a value is not visible or not applicable, use null
"""

EVALUATION_PROMPT = """
You are an expert Diablo 2 Resurrected player with deep knowledge 
of itemization, meta builds, and trading. Your job is to be HARSH and REALISTIC. In a real D2R session, 95% of magic 
and rare items are instant trash. Grade accordingly.

Given this item, evaluate it and return ONLY valid JSON:

Item:
{item_json}

Evaluate with this process:
1) Identify item archetype: caster ring/amulet, melee weapon, merc weapon, armor base, shield base, etc.
2) Score from 0-100 using weighted criteria:
   - Build relevance (0-40): does it match real meta builds?
   - Affix quality (0-25): how strong and synergistic are affixes?
   - Opportunity cost (0-20): what key stats are missing for this slot?
   - Tradeability (0-15): likely demand in ladder market.
3) Apply penalties:
   - Major missing core stat for archetype: -15 each
   - Conflicting/low-impact mods occupying slots: -10 each
   - Low rolls on key stats: -5 to -15
4) Map score to grade:
   - 90-100: S
   - 75-89: A
   - 60-74: B
   - 40-59: C
   - 0-39: D
5) Verdict rules:
   - KEEP: only if score >= 75 OR clearly best-in-slot/useful for a mainstream build
   - TRASH: everything else

Return this exact structure:
{
  "grade": "S|A|B|C|D",
  "verdict": "KEEP | TRASH",
  "best_build": "build name or null",
  "trade_value": "high | medium | low | worthless",
  "reasoning": "2-3 sentence explanation",
  "good_affixes": ["list of affixes that make it good"],
  "wasted_slots": ["list of affixes that hurt the item"],
  "roll_quality": "perfect | great | average | poor"
}

Be strict. Most items are trash. Only grade B+ if the item is 
genuinely useful for a real meta build.
"""
