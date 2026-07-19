"""
Skin Tone & Dress Color Recommendation Engine

Provides color palette classification and dress/clothing color suggestions based on
the user's skin tone and undertone.
"""

import os
import json
from typing import Dict, List, Optional
import pandas as pd

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COLOR_RULES_PATH = os.path.join(MODULE_DIR, "color_rules.json")

_COLOR_RULES_CACHE: Optional[Dict] = None


def load_color_rules(filepath: Optional[str] = None) -> Dict:
    """
    Loads and caches skin tone color rules from JSON file.
    """
    global _COLOR_RULES_CACHE
    target_path = filepath if filepath else DEFAULT_COLOR_RULES_PATH

    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Color rules file not found at: {target_path}")

    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _COLOR_RULES_CACHE = data
    return data


def normalize_skin_tone(skin_tone: str) -> str:
    """
    Normalizes skin tone input strings to rule keys:
    'warm', 'cool', 'neutral', 'deep', 'fair', 'medium_olive'.
    """
    if not skin_tone:
        return "neutral"

    st = str(skin_tone).strip().lower()
    
    if "warm" in st or "golden" in st or "peach" in st:
        return "warm"
    if "cool" in st or "pink" in st or "rosy" in st:
        return "cool"
    if "deep" in st or "dark" in st or "black" in st:
        return "deep"
    if "fair" in st or "light" in st or "pale" in st:
        return "fair"
    if "medium" in st or "olive" in st or "tan" in st:
        return "medium_olive"
    if "neutral" in st:
        return "neutral"

    return "neutral"


def get_color_palette(skin_tone: str) -> Dict:
    """
    Retrieves recommended colors, neutral colors, and colors to avoid for a skin tone.
    
    Parameters:
    - skin_tone: Skin tone category ("warm", "cool", "neutral", "deep", "fair", "medium_olive").
    
    Returns:
    - Dict with color recommendations and descriptions.
    """
    rules = load_color_rules() if _COLOR_RULES_CACHE is None else _COLOR_RULES_CACHE
    key = normalize_skin_tone(skin_tone)
    return rules.get(key, rules.get("neutral", {}))


def filter_catalog_by_color(df: pd.DataFrame, skin_tone: str) -> pd.DataFrame:
    """
    Filters catalog DataFrame items matching the user's skin tone.
    
    Parameters:
    - df: Catalog DataFrame.
    - skin_tone: Skin tone category.
    
    Returns:
    - Filtered pd.DataFrame matching skin tone.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    if "ideal_skin_tones" not in df.columns:
        return df

    target_tone = normalize_skin_tone(skin_tone)

    def matches_skin_tone(row):
        tones_raw = str(row.get("ideal_skin_tones", "all"))
        tones = [t.strip().lower() for t in tones_raw.split("|")]
        return target_tone in tones or "all" in tones

    mask = [matches_skin_tone(row) for _, row in df.iterrows()]
    return df[mask].copy()


def recommend_colors_for_user(
    skin_tone: str,
    shape: Optional[str] = None,
    gender: str = "female"
) -> Dict:
    """
    Generates a skin-tone based color recommendation profile for a user.
    """
    palette = get_color_palette(skin_tone)
    norm_tone = normalize_skin_tone(skin_tone)

    return {
        "user_skin_tone_input": skin_tone,
        "normalized_skin_tone": norm_tone,
        "palette_name": palette.get("name", ""),
        "description": palette.get("description", ""),
        "recommended_colors": palette.get("recommended_colors", []),
        "neutral_colors": palette.get("neutral_colors", []),
        "colors_to_avoid": palette.get("colors_to_avoid", [])
    }
