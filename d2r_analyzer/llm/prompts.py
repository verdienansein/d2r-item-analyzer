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
- For magic/rare items with no proper name, set name to null
- is_ethereal is true if the word "Ethereal" appears
- If a value is not visible or not applicable, use null
"""
