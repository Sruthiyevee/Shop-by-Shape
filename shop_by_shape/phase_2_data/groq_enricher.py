"""
Groq LLM Body Shape Mapping Enricher

Integrates Groq LLM API to generate dynamic, personalized styling insights,
color palette guidance, and fabric recommendations for body shapes. Reads API key
from .env file (GROQ_API_KEY).
"""

import os
import json
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

# Find and load .env file from project root or current working directory
module_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(module_dir, ".."))
env_path = os.path.join(project_dir, ".env")

if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"


def get_groq_api_key() -> Optional[str]:
    """Retrieve Groq API key from environment variables."""
    key = os.getenv("GROQ_API_KEY")
    if not key or key.strip() in ["gsk_your_groq_api_key_here", "your_groq_api_key_here"]:
        return None
    return key.strip()


def get_groq_model() -> str:
    """Retrieve Groq model name from environment variables."""
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()


def generate_fallback_enrichment(shape: str, gender: str = "female", occasion: Optional[str] = None) -> Dict:
    """
    Generates structured fallback styling insights when Groq API key is not present or offline.
    """
    g = "men" if gender and str(gender).strip().lower() in ["male", "man", "men", "m"] else "women"
    occ = occasion.strip().lower() if occasion else "casual"

    return {
        "status": "fallback",
        "is_live_llm": False,
        "model_used": "rule-based-engine",
        "styling_insights": f"Focus on maintaining vertical symmetry for {g}'s {shape} profile during {occ} wear.",
        "color_palette_advice": "Pair dark monochromatic tones on areas you wish to streamline with brighter contrast tones on areas you wish to highlight.",
        "fabric_recommendations": "Structured cottons, tailored wool blends, and draping rayon or crepe fabrics hold shape best.",
        "pro_tip": f"Ensure shoulders and waist seams align with natural body breakpoints for the {shape} silhouette."
    }


from functools import lru_cache

# In-memory dictionary cache to prevent redundant LLM API calls and save tokens
_LLM_CACHE: Dict[str, Dict] = {}


@lru_cache(maxsize=128)
def _cached_groq_call(cache_key: str, api_key: str, model: str, system_prompt: str, user_prompt: str) -> str:
    """Internal helper to call Groq API with LRU caching."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 200,  # Strictly limited to prevent token overuse
        "response_format": {"type": "json_object"}
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=6)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    raise RuntimeError(f"Groq API returned HTTP {response.status_code}")


def enrich_shape_mapping(
    shape: str,
    gender: str = "female",
    occasion: Optional[str] = None,
    profile_rules: Optional[Dict] = None
) -> Dict:
    """
    Queries Groq LLM API to retrieve enhanced styling advice and body shape mapping details.
    Employs caching and strict max_tokens caps to minimize token usage.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return generate_fallback_enrichment(shape, gender, occasion)

    model = get_groq_model()
    occ_str = occasion if occasion else "general"
    traits = profile_rules.get("traits", "") if profile_rules else ""
    goal = profile_rules.get("goal", "") if profile_rules else ""

    cache_key = f"{shape}:{gender}:{occ_str}:{traits}:{goal}".lower()
    if cache_key in _LLM_CACHE:
        return _LLM_CACHE[cache_key]

    system_prompt = (
        "You are an expert personal fashion stylist. "
        "Provide concise, high-impact styling advice in clean JSON format."
    )

    user_prompt = f"""
    Gender: {gender}, Shape: {shape}, Occasion: {occ_str}
    Traits: {traits}, Goal: {goal}
    Return JSON object:
    - "styling_insights": 1 short sentence.
    - "color_palette_advice": 1 short sentence.
    - "fabric_recommendations": 1 short sentence.
    - "pro_tip": 1 short sentence.
    """

    try:
        content_str = _cached_groq_call(cache_key, api_key, model, system_prompt, user_prompt)
        parsed_content = json.loads(content_str)
        res = {
            "status": "success",
            "is_live_llm": True,
            "model_used": model,
            "styling_insights": parsed_content.get("styling_insights", ""),
            "color_palette_advice": parsed_content.get("color_palette_advice", ""),
            "fabric_recommendations": parsed_content.get("fabric_recommendations", ""),
            "pro_tip": parsed_content.get("pro_tip", "")
        }
        _LLM_CACHE[cache_key] = res
        return res
    except Exception:
        return generate_fallback_enrichment(shape, gender, occasion)

