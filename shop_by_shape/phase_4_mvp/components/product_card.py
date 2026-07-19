"""
Streamlit Product Card & Outfit Renderer Component

Renders e-commerce clothing recommendation cards with high visual appeal,
badges for category, price, ideal shapes, skin tone tags, and image placeholders.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from phase_5_ai_integration import explain_item_fit


def render_product_card(
    item: Dict[str, Any],
    enable_ai: bool = False,
    shape: str = "Pear",
    gender: str = "female",
    skin_tone: Optional[str] = None,
    key_prefix: str = "card_"
):
    """
    Renders an individual product item card in Streamlit with custom CSS styling and AI fit explainer.
    Ensures unique button keys via key_prefix.
    """
    name = item.get("name", "Clothing Item")
    category = item.get("category", "General").capitalize()
    price = f"${float(item.get('price', 0.0)):.2f}"
    image_url = item.get("image_url", "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400")
    color = item.get("color", "Classic Color")
    desc = item.get("description", "Flattering fit designed for your body shape.")
    shapes = item.get("ideal_shapes", "").replace("|", ", ").title()
    search_term = item.get("search_term", f"{color} {name}")
    item_id = item.get("id", name)

    with st.container():
        st.image(image_url, use_container_width=True)
        st.markdown(f"#### {name}")
        st.markdown(f"**Category**: `{category}` | **Color**: `{color}`")
        st.markdown(f"**Ideal Shapes**: `{shapes}`")
        st.markdown(f"_{desc}_")

        if enable_ai:
            explanation = explain_item_fit(item, shape=shape, gender=gender, skin_tone=skin_tone)
            with st.expander("💡 Why This Item Fits You (AI Fit Analysis)"):
                st.markdown(f"**Rationale**: {explanation.get('fit_rationale')}")
                st.markdown(f"**Key Benefit**: {explanation.get('key_benefit')}")

        st.markdown("🔍 **Copyable Search Recommendation:**")
        st.code(search_term, language=None)
        st.caption("📋 Copy & paste this exact term into your favorite store (Amazon, Myntra, ASOS, Google Shopping).")
        st.markdown("---")



def render_outfit_combination(
    outfit_data: Dict[str, Any],
    enable_ai: bool = False,
    shape: str = "Pear",
    gender: str = "female",
    skin_tone: Optional[str] = None,
    key_prefix: str = "outfit_"
):
    """
    Renders a complete paired outfit recommendation.
    """
    st.markdown("### 👔 Suggested Outfit Pairings")

    pairing = outfit_data.get("suggested_outfit", {})
    pairing_type = pairing.get("type", "two_piece")

    if pairing_type == "suit" and pairing.get("primary"):
        st.subheader("👔 Complete Suit Outfit")
        render_product_card(pairing["primary"], enable_ai=enable_ai, shape=shape, gender=gender, skin_tone=skin_tone, key_prefix=f"{key_prefix}suit_")
    elif pairing_type == "dress" and pairing.get("primary"):
        st.subheader("👗 Recommended Dress Outfit")
        render_product_card(pairing["primary"], enable_ai=enable_ai, shape=shape, gender=gender, skin_tone=skin_tone, key_prefix=f"{key_prefix}dress_")
        if pairing.get("outerwear"):
            st.subheader("🧥 Paired Outerwear Layer")
            render_product_card(pairing["outerwear"], enable_ai=enable_ai, shape=shape, gender=gender, skin_tone=skin_tone, key_prefix=f"{key_prefix}dress_outer_")
    else:
        cols = st.columns(2)
        if pairing.get("top"):
            with cols[0]:
                st.subheader("👕 Upper Body Top Pick")
                render_product_card(pairing["top"], enable_ai=enable_ai, shape=shape, gender=gender, skin_tone=skin_tone, key_prefix=f"{key_prefix}top_")
        if pairing.get("bottom"):
            with cols[1]:
                st.subheader("👖 Lower Body Bottom Pick")
                render_product_card(pairing["bottom"], enable_ai=enable_ai, shape=shape, gender=gender, skin_tone=skin_tone, key_prefix=f"{key_prefix}bottom_")

        if pairing.get("outerwear"):
            st.subheader("🧥 Recommended Layering Piece")
            render_product_card(pairing["outerwear"], enable_ai=enable_ai, shape=shape, gender=gender, skin_tone=skin_tone, key_prefix=f"{key_prefix}outer_")

