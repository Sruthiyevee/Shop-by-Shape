"""
Styling RAG (Retrieval-Augmented Generation) Pipeline

Indexes styling rules from shape_rules.json and color_rules.json into a searchable
retrieval engine to ground AI explanations in deterministic fashion domain knowledge.
"""

import os
import json
from typing import Dict, List, Optional
from phase_2_data import load_shape_rules, normalize_shape_name
from phase_3_color import load_color_rules, normalize_skin_tone


class StylingRAGPipeline:
    """
    Lightweight, fast retrieval engine for fashion rules and body shape knowledge.
    """

    def __init__(self):
        self.documents: List[Dict] = []
        self._build_knowledge_index()

    def _build_knowledge_index(self):
        """Indexes shape rules and color rules into searchable knowledge chunks."""
        shape_data = load_shape_rules()
        color_data = load_color_rules()

        # Index Women & Men shape rules
        for gender in ["women", "men"]:
            shapes_dict = shape_data.get(gender, {})
            for shape_key, profile in shapes_dict.items():
                rec = profile.get("recommended", {})
                doc_text = (
                    f"Gender: {gender}. Shape: {shape_key}. Traits: {profile.get('traits')}. "
                    f"Goal: {profile.get('goal')}. Recommended Tops: {', '.join(rec.get('tops', []))}. "
                    f"Recommended Bottoms: {', '.join(rec.get('bottoms', []))}. "
                    f"Recommended Dresses: {', '.join(rec.get('dresses', []))}. "
                    f"Avoid: {', '.join(rec.get('avoid', []))}."
                )
                self.documents.append({
                    "type": "shape_rule",
                    "gender": gender,
                    "shape": shape_key,
                    "content": doc_text,
                    "profile": profile
                })

        # Index Skin Tone color rules
        for tone_key, tone_profile in color_data.items():
            doc_text = (
                f"Skin Tone: {tone_key} ({tone_profile.get('name')}). "
                f"Description: {tone_profile.get('description')}. "
                f"Recommended Colors: {', '.join(tone_profile.get('recommended_colors', []))}. "
                f"Neutral Colors: {', '.join(tone_profile.get('neutral_colors', []))}. "
                f"Colors to Avoid: {', '.join(tone_profile.get('colors_to_avoid', []))}."
            )
            self.documents.append({
                "type": "color_rule",
                "skin_tone": tone_key,
                "content": doc_text,
                "profile": tone_profile
            })

    def retrieve_context(
        self,
        query: str,
        shape: str,
        gender: str = "female",
        skin_tone: Optional[str] = None,
        k: int = 2
    ) -> List[Dict]:
        """
        Retrieves the most relevant knowledge context chunks matching the query, shape, and skin tone.
        """
        norm_shape = normalize_shape_name(shape)
        target_gender = "men" if gender and str(gender).strip().lower() in ["male", "man", "men", "m"] else "women"
        norm_tone = normalize_skin_tone(skin_tone) if skin_tone else "neutral"

        results = []
        # Primary match: Shape document for target gender
        for doc in self.documents:
            if doc["type"] == "shape_rule" and doc["gender"] == target_gender and doc["shape"] == norm_shape:
                results.append(doc)
                break

        # Secondary match: Color rule document for target skin tone
        for doc in self.documents:
            if doc["type"] == "color_rule" and doc["skin_tone"] == norm_tone:
                results.append(doc)
                break

        return results[:k]
