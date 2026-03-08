ITEM_EXTRACTION_PROMPT = """
You are analyzing a Diablo 2 Resurrected item tooltip screenshot.

Extract ALL visible item information and return ONLY valid JSON.
No explanation, no markdown, no code blocks. Raw JSON only.

Return this exact structure:
{
  "name": "item name or null if magic/rare with no name",
  "base_type": "e.g. Amulet, Ring, Monarch, Archon Plate",
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

Rules:
- Extract EVERY stat line visible, even if you don't recognize it
- is_ethereal is true if the word "Ethereal" appears
- If a value is not visible or not applicable, use null
"""

EVALUATION_PROMPT = """
You are an 2026 expert Diablo 2 Resurrected player with deep knowledge 
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
