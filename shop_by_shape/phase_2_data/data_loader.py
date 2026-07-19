"""
Catalog Data Loader & Outfit Recommendation Engine

Responsible for loading outfit styling rules (from shape_rules.json),
catalog items (from mock_catalog.csv), and providing filtering and
outfit suggestion functionality for women and men body shapes.
"""

import json
import os
from typing import Dict, List, Optional, Union
import pandas as pd

# Default paths relative to this file
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES_PATH = os.path.join(MODULE_DIR, "shape_rules.json")
DEFAULT_CATALOG_PATH = os.path.join(MODULE_DIR, "mock_catalog.csv")

# Global cache for rules
_SHAPE_RULES_CACHE: Optional[Dict] = None


def load_shape_rules(filepath: Optional[str] = None) -> Dict:
    """
    Loads and caches shape rules from JSON file.
    
    Parameters:
    - filepath: Absolute or relative path to shape_rules.json.
    
    Returns:
    - Dict containing full dataset of rules for women and men.
    """
    global _SHAPE_RULES_CACHE
    target_path = filepath if filepath else DEFAULT_RULES_PATH
    
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Shape rules JSON file not found at: {target_path}")
        
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    _SHAPE_RULES_CACHE = data
    return data


def _is_male_gender(gender: str) -> bool:
    """Helper to detect if gender string represents male."""
    if not gender:
        return False
    g = str(gender).strip().lower()
    return g in ["male", "man", "men", "m", "boy"]


def normalize_shape_name(shape: str) -> str:
    """
    Normalizes shape names to snake_case keys matching shape_rules.json keys.
    e.g. "Inverted Triangle" -> "inverted_triangle", "Pear" -> "pear"
    """
    if not shape:
        return ""
    s = str(shape).strip().lower().replace("-", " ").replace("_", " ")
    words = s.split()
    return "_".join(words)


def get_shape_profile(shape: str, gender: str = "female") -> Dict:
    """
    Retrieves the styling profile, traits, goals, recommended garment types,
    and occasion notes for a specified body shape and gender.
    
    Parameters:
    - shape: Body shape name (e.g., "Pear", "Inverted Triangle", "trapezoid", "oval").
    - gender: Gender string ("female"/"women" or "male"/"men").
    
    Returns:
    - Dict of shape profile details, or empty dict if not found.
    """
    rules = load_shape_rules() if _SHAPE_RULES_CACHE is None else _SHAPE_RULES_CACHE
    gender_key = "men" if _is_male_gender(gender) else "women"
    shape_key = normalize_shape_name(shape)
    
    gender_rules = rules.get(gender_key, {})
    return gender_rules.get(shape_key, {})


def load_catalog(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads mock catalog CSV into a Pandas DataFrame.
    
    Parameters:
    - filepath: Path to catalog CSV. Uses default mock_catalog.csv if None.
    
    Returns:
    - pd.DataFrame containing product items.
    """
    target_path = filepath if filepath else DEFAULT_CATALOG_PATH
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Catalog CSV file not found at: {target_path}")
        
    df = pd.read_csv(target_path)
    # Ensure standard string cleaning
    df["gender"] = df["gender"].astype(str).str.strip().str.lower()
    df["category"] = df["category"].astype(str).str.strip().str.lower()
    df["occasion"] = df["occasion"].astype(str).str.strip().str.lower()
    return df


def filter_catalog(
    df: pd.DataFrame,
    shape: str,
    gender: str = "female",
    category: Optional[str] = None,
    occasion: Optional[str] = None,
    skin_tone: Optional[str] = None
) -> pd.DataFrame:
    """
    Filters clothing items matching user's body shape, gender, and optional category/occasion/skin_tone.
    
    Parameters:
    - df: Catalog DataFrame.
    - shape: Standardized body shape name (e.g. "Pear", "Inverted Triangle", "Trapezoid").
    - gender: Gender string ("female" or "male").
    - category: Optional category filter ("tops", "bottoms", "dresses", "outerwear", "suits").
    - occasion: Optional occasion filter ("casual", "formal", "party").
    - skin_tone: Optional skin tone category ("warm", "cool", "neutral", "deep", "fair", "medium_olive").
    
    Returns:
    - Filtered pd.DataFrame.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=df.columns if df is not None else [])

    if _is_male_gender(gender):
        gender_mask = df["gender"].astype(str).str.strip().str.lower().isin(["male", "man", "men", "m"])
    else:
        gender_mask = df["gender"].astype(str).str.strip().str.lower().isin(["female", "woman", "women", "w"])
        
    filtered = df[gender_mask].copy()
    if filtered.empty:
        return filtered

    shape_key = normalize_shape_name(shape)

    # 2. Filter by ideal shape inclusion and avoid shape exclusion
    def matches_shape(row):
        ideal_raw = str(row.get("ideal_shapes", ""))
        avoid_raw = str(row.get("avoid_shapes", ""))
        ideal = [s.strip().lower() for s in ideal_raw.split("|")]
        avoid = [s.strip().lower() for s in avoid_raw.split("|")]
        
        is_ideal = shape_key in ideal or "all" in ideal
        is_avoided = shape_key in avoid
        return is_ideal and not is_avoided

    mask = [matches_shape(row) for _, row in filtered.iterrows()]
    filtered = filtered[mask]
    
    if filtered.empty:
        return filtered

    # 3. Filter by category if provided
    if category:
        cat_clean = category.strip().lower()
        cat_col = filtered["category"].astype(str).str.strip().str.lower()
        filtered = filtered[cat_col == cat_clean]
        if filtered.empty:
            return filtered

    # 4. Filter by occasion if provided
    if occasion:
        occ_clean = occasion.strip().lower()
        occ_col = filtered["occasion"].astype(str).str.strip().str.lower()
        filtered = filtered[(occ_col == occ_clean) | (occ_col == "all")]
        if filtered.empty:
            return filtered

    # 5. Filter by skin_tone if provided and ideal_skin_tones column exists
    if skin_tone and "ideal_skin_tones" in filtered.columns:
        tone_clean = str(skin_tone).strip().lower().replace("-", "_").replace(" ", "_")
        def matches_tone(row):
            tones_raw = str(row.get("ideal_skin_tones", "all"))
            tones = [t.strip().lower() for t in tones_raw.split("|")]
            return tone_clean in tones or "all" in tones or "neutral" in tones

        tone_mask = [matches_tone(row) for _, row in filtered.iterrows()]
        matched_tone_df = filtered[tone_mask]
        if not matched_tone_df.empty:
            filtered = matched_tone_df

    return filtered



from phase_2_data.groq_enricher import enrich_shape_mapping


def suggest_outfit(
    shape: str,
    gender: str = "female",
    occasion: Optional[str] = None,
    skin_tone: Optional[str] = None,
    catalog_df: Optional[pd.DataFrame] = None,
    include_groq_llm: bool = False
) -> Dict:
    """
    Generates a complete structured outfit recommendation for a given shape, gender, occasion, and skin tone.
    Optionally enriches body shape mapping using Groq LLM API.
    
    Parameters:
    - shape: Body shape name.
    - gender: "female" or "male".
    - occasion: "casual", "formal", "party", or None.
    - skin_tone: "warm", "cool", "neutral", "deep", "fair", "medium_olive", or None.
    - catalog_df: Optional catalog DataFrame. Loaded automatically if None.
    - include_groq_llm: If True, calls Groq LLM API to include additional styling insights.
    
    Returns:
    - Dict with profile guidance, matching products, structured outfit combination, and optional LLM insights.
    """
    profile = get_shape_profile(shape, gender)
    if catalog_df is None:
        catalog_df = load_catalog()
        
    matched_items = filter_catalog(catalog_df, shape, gender=gender, occasion=occasion, skin_tone=skin_tone)

    
    # Select best items per category
    tops = matched_items[matched_items["category"] == "tops"].to_dict(orient="records")
    bottoms = matched_items[matched_items["category"] == "bottoms"].to_dict(orient="records")
    dresses = matched_items[matched_items["category"] == "dresses"].to_dict(orient="records")
    outerwear = matched_items[matched_items["category"] == "outerwear"].to_dict(orient="records")
    suits = matched_items[matched_items["category"] == "suits"].to_dict(orient="records")
    
    # Determine occasion note snippet
    occ_key = occasion.strip().lower() if occasion else "casual"
    occasion_note = profile.get("occasion_notes", {}).get(occ_key, "Select items that match your body proportion goals.")
    
    # Build complete outfit pairing
    top_pick = tops[0] if tops else None
    bottom_pick = bottoms[0] if bottoms else None
    dress_pick = dresses[0] if dresses else None
    outerwear_pick = outerwear[0] if outerwear else None
    suit_pick = suits[0] if suits else None
    
    outfit_pairing = {}
    if _is_male_gender(gender):
        if occ_key == "formal" and suit_pick:
            outfit_pairing = {"primary": suit_pick, "type": "suit"}
        else:
            outfit_pairing = {"top": top_pick, "bottom": bottom_pick, "outerwear": outerwear_pick, "type": "two_piece"}
    else:
        if (occ_key in ["formal", "party"]) and dress_pick:
            outfit_pairing = {"primary": dress_pick, "outerwear": outerwear_pick, "type": "dress"}
        else:
            outfit_pairing = {"top": top_pick, "bottom": bottom_pick, "outerwear": outerwear_pick, "type": "two_piece"}
            
    res = {
        "gender": "male" if _is_male_gender(gender) else "female",
        "shape": shape,
        "occasion": occasion,
        "traits": profile.get("traits", ""),
        "goal": profile.get("goal", ""),
        "recommended_garments": profile.get("recommended", {}),
        "occasion_advice": occasion_note,
        "all_matched_products": matched_items.to_dict(orient="records"),
        "suggested_outfit": outfit_pairing
    }

    if include_groq_llm:
        res["groq_llm_enrichment"] = enrich_shape_mapping(shape, gender=gender, occasion=occasion, profile_rules=profile)

    return res

