"""
LLM Fit & Outfit Explainer

Generates personalized, RAG-grounded explanations of why specific clothing items
or outfit combinations complement a user's body shape and skin tone.
"""

import json
from typing import Dict, Optional
from phase_2_data import get_shape_profile
from phase_2_data.groq_enricher import get_groq_api_key, get_groq_model, _cached_groq_call
from phase_3_color import get_color_palette
from phase_5_ai_integration.rag_pipeline import StylingRAGPipeline

# Global RAG Pipeline Instance
rag_engine = StylingRAGPipeline()

# Local cache for item fit explanations
_EXPLANATION_CACHE: Dict[str, Dict] = {}


def generate_fallback_fit_explanation(
    item: Dict,
    shape: str,
    gender: str = "female",
    skin_tone: Optional[str] = None
) -> Dict:
    """
    Generates structured RAG rule-based item fit explanation when Groq API key is unconfigured.
    """
    profile = get_shape_profile(shape, gender)
    color_pal = get_color_palette(skin_tone) if skin_tone else {}

    item_name = item.get("name", "Clothing Item")
    category = item.get("category", "garment")
    color = item.get("color", "color")

    goal = profile.get("goal", "balance proportions")
    rec_colors = ", ".join(color_pal.get("recommended_colors", [])[:3]) or "complementary tones"

    reason = (
        f"The {item_name} is tailored to support your {shape} silhouette by working to {goal.lower()}. "
        f"Its {color} color aligns well with recommended {skin_tone or 'neutral'} palette shades ({rec_colors})."
    )

    return {
        "status": "fallback",
        "is_live_llm": False,
        "item_id": item.get("id"),
        "item_name": item_name,
        "fit_rationale": reason,
        "key_benefit": f"Balances your {shape} proportions while flattering your {skin_tone or 'natural'} skin undertone."
    }


def explain_item_fit(
    item: Dict,
    shape: str,
    gender: str = "female",
    skin_tone: Optional[str] = None
) -> Dict:
    """
    Generates an AI explanation (or RAG fallback) detailing why a clothing item fits the user.
    """
    item_id = item.get("id", item.get("name"))
    cache_key = f"{item_id}:{shape}:{gender}:{skin_tone}".lower()

    if cache_key in _EXPLANATION_CACHE:
        return _EXPLANATION_CACHE[cache_key]

    api_key = get_groq_api_key()
    if not api_key:
        fallback = generate_fallback_fit_explanation(item, shape, gender, skin_tone)
        _EXPLANATION_CACHE[cache_key] = fallback
        return fallback

    # Retrieve RAG context
    rag_context = rag_engine.retrieve_context(
        query=f"{item.get('name')} {item.get('category')}",
        shape=shape,
        gender=gender,
        skin_tone=skin_tone
    )

    context_str = "\n".join([doc["content"] for doc in rag_context])
    model = get_groq_model()

    system_prompt = (
        "You are an expert personal stylist. Explain why a clothing item fits the user's body shape "
        "and skin tone based strictly on the provided RAG styling context. Return JSON only."
    )

    user_prompt = f"""
    User: Gender={gender}, Body Shape={shape}, Skin Tone={skin_tone or 'Neutral'}
    Item: Name={item.get('name')}, Category={item.get('category')}, Color={item.get('color')}, Description={item.get('description')}
    
    RAG Knowledge Context:
    {context_str}

    Return JSON object:
    - "fit_rationale": 2 short sentences explaining why this cut and color complement their body shape and skin tone.
    - "key_benefit": 1 punchy sentence highlighting the main visual advantage.
    """

    try:
        content_str = _cached_groq_call(cache_key, api_key, model, system_prompt, user_prompt)
        parsed = json.loads(content_str)
        res = {
            "status": "success",
            "is_live_llm": True,
            "item_id": item_id,
            "item_name": item.get("name"),
            "fit_rationale": parsed.get("fit_rationale", ""),
            "key_benefit": parsed.get("key_benefit", "")
        }
        _EXPLANATION_CACHE[cache_key] = res
        return res
    except Exception:
        fallback = generate_fallback_fit_explanation(item, shape, gender, skin_tone)
        _EXPLANATION_CACHE[cache_key] = fallback
        return fallback


def explain_outfit_pairing(
    outfit: Dict,
    shape: str,
    gender: str = "female",
    skin_tone: Optional[str] = None
) -> Dict:
    """
    Generates a holistic explanation of why a complete outfit pairing works together.
    """
    profile = get_shape_profile(shape, gender)
    color_pal = get_color_palette(skin_tone) if skin_tone else {}

    return {
        "outfit_type": outfit.get("suggested_outfit", {}).get("type", "two_piece"),
        "shape": shape,
        "pairing_rationale": (
            f"This combination harmonizes your {shape} silhouette by drawing visual interest to key proportion break points. "
            f"The chosen color tones accent your {color_pal.get('name', 'natural')} complexion."
        ),
        "style_tip": profile.get("goal", "Maintain balanced silhouette proportions.")
    }
