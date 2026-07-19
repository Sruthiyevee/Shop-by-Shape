"""
Streamlit Sidebar Component

Renders interactive sidebar options: gender selection, onboarding assessment method,
skin tone selector, occasion filter, and AI styling insights toggle.
"""

import streamlit as st
from typing import Dict


def render_sidebar() -> Dict:
    """
    Renders sidebar configuration controls and returns user parameter settings.
    """
    st.sidebar.markdown("## ⚙️ Style Preferences")
    
    # 1. Gender Selection
    gender = st.sidebar.radio(
        "Select Target Fit / Gender:",
        options=["female", "male"],
        format_func=lambda x: "👩 Women's Styling" if x == "female" else "👨 Men's Styling",
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # 2. Assessment Methodology
    method = st.sidebar.selectbox(
        "Body Shape Assessment Method:",
        options=["quiz", "measurements"],
        format_func=lambda x: "⚡ Quick Assessment Quiz" if x == "quiz" else "📏 Precision Measurements",
        index=0
    )

    st.sidebar.markdown("---")

    # 3. Skin Tone Selection (Phase 3 Integration)
    skin_tone = st.sidebar.selectbox(
        "Select Your Skin Tone / Undertone:",
        options=["warm", "cool", "neutral", "deep", "fair", "medium_olive"],
        format_func=lambda x: {
            "warm": "✨ Warm (Golden / Yellow)",
            "cool": "💎 Cool (Pink / Blue)",
            "neutral": "🌸 Neutral (Balanced)",
            "deep": "👑 Deep / Dark",
            "fair": "❄️ Fair / Light",
            "medium_olive": "🌿 Medium / Olive"
        }.get(x, x.capitalize()),
        index=0
    )

    st.sidebar.markdown("---")

    # 4. Occasion Filter
    occasion = st.sidebar.selectbox(
        "Filter by Occasion:",
        options=["all", "casual", "formal", "party"],
        format_func=lambda x: "🌟 All Occasions" if x == "all" else f"📌 {x.capitalize()}",
        index=0
    )

    st.sidebar.markdown("---")

    # 5. AI Insights Toggle
    enable_ai = st.sidebar.checkbox(
        "🤖 Enable AI Groq LLM Styling Insights",
        value=False,
        help="Retrieves AI-generated personalized styling insights (token-optimized & cached)."
    )

    return {
        "gender": gender,
        "method": method,
        "skin_tone": skin_tone,
        "occasion": None if occasion == "all" else occasion,
        "enable_ai": enable_ai
    }
