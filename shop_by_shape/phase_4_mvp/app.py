"""
Shop by Shape & Skin Tone - Main Screen Multi-Step Wizard Application

Eliminates sidebar completely and guides users through a clean 4-step main-screen wizard:
Step 1: Gender & Body Assessment Onboarding (Women & Men)
Step 2: Skin Tone & Occasion Preference Selection
Step 3: Calculated Style Profile & Default AI Groq LLM Insights
Step 4: Copyable Search Recommendations & Outfit Pairings
"""

import sys
import os
import streamlit as st

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_2_data import (
    load_catalog,
    filter_catalog,
    get_shape_profile,
    suggest_outfit
)
from phase_3_color import recommend_colors_for_user
from phase_4_mvp.components.quiz import render_quiz_form, render_measurement_form
from phase_4_mvp.components.product_card import render_product_card, render_outfit_combination
from phase_4_mvp.components.walkthrough import render_walkthrough_guide


def apply_custom_css():
    """Applies modern styling, gradients, stepper indicators, and custom badges."""
    st.markdown("""
        <style>
        .main-title {
            font-size: 2.3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #4F46E5, #EC4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1.05rem;
            color: #6B7280;
            margin-bottom: 1.5rem;
        }
        .stepper-container {
            display: flex;
            justify-content: space-between;
            background-color: #F3F4F6;
            padding: 0.75rem;
            border-radius: 0.75rem;
            margin-bottom: 1.5rem;
        }
        .step-pill {
            flex: 1;
            text-align: center;
            padding: 0.5rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            color: #4B5563;
        }
        .step-pill.active {
            background-color: #4F46E5;
            color: #FFFFFF;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }
        .shape-badge {
            display: inline-block;
            background-color: #EEF2FF;
            color: #4338CA;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 1.2rem;
            border: 1px solid #C7D2FE;
        }
        .goal-box {
            background-color: rgba(79, 70, 229, 0.08);
            border-left: 4px solid #4F46E5;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }

        .color-chip {
            display: inline-block;
            background-color: #ECFDF5;
            color: #065F46;
            padding: 0.25rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.9rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .avoid-chip {
            display: inline-block;
            background-color: #FEF2F2;
            color: #991B1B;
            padding: 0.25rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.9rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        /* Hide sidebar completely */
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)


def render_stepper_header(current_step: int):
    """Renders visual multi-step progress stepper bar."""
    steps = [
        "1. Body Assessment",
        "2. Skin Tone & Occasion",
        "3. Profile & Style Suggestions",
        "4. Recommendations"
    ]

    pills_html = '<div class="stepper-container">'
    for idx, step_name in enumerate(steps, start=1):
        active_cls = "active" if idx == current_step else ""
        pills_html += f'<div class="step-pill {active_cls}">{step_name}</div>'
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Shop by Shape & Skin Tone",
        page_icon="👗",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    apply_custom_css()

    # Header & Hero
    st.markdown('<div class="main-title">Shop by Shape & Skin Tone</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">E-Commerce Recommendation Engine matching apparel to your body proportions & skin complexions.</div>', unsafe_allow_html=True)

    # First-Time User Walkthrough Guide
    render_walkthrough_guide()

    # Session State Initialization
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 1
    if "gender" not in st.session_state:
        st.session_state["gender"] = "female"
    if "method" not in st.session_state:
        st.session_state["method"] = "quiz"
    if "skin_tone" not in st.session_state:
        st.session_state["skin_tone"] = "warm"
    if "occasion" not in st.session_state:
        st.session_state["occasion"] = "all"
    if "calculated_shape" not in st.session_state:
        st.session_state["calculated_shape"] = "Pear" if st.session_state["gender"] == "female" else "Trapezoid"

    current_step = st.session_state["current_step"]
    render_stepper_header(current_step)

    # ==========================================
    # STEP 1: GENDER & BODY ASSESSMENT ONBOARDING
    # ==========================================
    if current_step == 1:
        st.markdown("### Step 1: Body Shape Assessment")
        st.caption("Select your target gender fit and choose your preferred body shape evaluation method.")

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            gender = st.radio(
                "Select Styling Category:",
                options=["female", "male"],
                format_func=lambda x: "👩 Women's Styling" if x == "female" else "👨 Men's Styling",
                index=0 if st.session_state["gender"] == "female" else 1,
                horizontal=True
            )
            st.session_state["gender"] = gender

        with col_opt2:
            method = st.radio(
                "Assessment Method:",
                options=["quiz", "measurements"],
                format_func=lambda x: "⚡ Quick Assessment Quiz" if x == "quiz" else "📏 Precision Measurements",
                index=0 if st.session_state["method"] == "quiz" else 1,
                horizontal=True
            )
            st.session_state["method"] = method

        st.markdown("---")

        if method == "quiz":
            shape_result = render_quiz_form(gender=gender)
        else:
            shape_result = render_measurement_form(gender=gender)

        if shape_result:
            st.session_state["calculated_shape"] = shape_result
            st.success(f"🎉 Shape Identified: **{shape_result}**")

        current_shape = st.session_state.get("calculated_shape", "Pear" if gender == "female" else "Trapezoid")
        st.info(f"Selected Profile: **{current_shape}** ({gender.capitalize()})")

        st.markdown("---")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn2:
            if st.button("Next: Select Skin Tone & Occasion ➡️", use_container_width=True, type="primary"):
                st.session_state["current_step"] = 2
                st.rerun()

    # ==========================================
    # STEP 2: SKIN TONE & OCCASION SELECTION
    # ==========================================
    elif current_step == 2:
        st.markdown("### Step 2: Select Skin Tone & Occasion")
        st.caption("Choose your skin tone undertone and target wearing occasion.")

        col_st1, col_st2 = st.columns(2)
        with col_st1:
            skin_tone = st.selectbox(
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
                index=["warm", "cool", "neutral", "deep", "fair", "medium_olive"].index(st.session_state["skin_tone"])
            )
            st.session_state["skin_tone"] = skin_tone

        with col_st2:
            occasion = st.selectbox(
                "Filter by Occasion:",
                options=["all", "casual", "formal", "party"],
                format_func=lambda x: "🌟 All Occasions" if x == "all" else f"📌 {x.capitalize()}",
                index=["all", "casual", "formal", "party"].index(st.session_state["occasion"])
            )
            st.session_state["occasion"] = occasion

        st.markdown("---")
        color_profile = recommend_colors_for_user(skin_tone, shape=st.session_state["calculated_shape"], gender=st.session_state["gender"])

        col_pal1, col_pal2 = st.columns(2)
        with col_pal1:
            st.markdown(f"#### Palette: `{color_profile.get('palette_name')}`")
            st.write(color_profile.get("description"))

            st.markdown("**Recommended Colors:**")
            rec_colors_html = "".join([f'<span class="color-chip">{c}</span>' for c in color_profile.get("recommended_colors", [])])
            st.markdown(rec_colors_html, unsafe_allow_html=True)

        with col_pal2:
            st.markdown("**Colors to Avoid:**")
            avoid_colors_html = "".join([f'<span class="avoid-chip">{c}</span>' for c in color_profile.get("colors_to_avoid", [])])
            st.markdown(avoid_colors_html, unsafe_allow_html=True)

            st.markdown("**Neutral Base Colors:**")
            neut_colors_html = "".join([f'<span class="color-chip">{c}</span>' for c in color_profile.get("neutral_colors", [])])
            st.markdown(neut_colors_html, unsafe_allow_html=True)

        st.markdown("---")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("⬅️ Back to Body Assessment", use_container_width=True):
                st.session_state["current_step"] = 1
                st.rerun()
        with col_btn2:
            if st.button("Next: View Style Profile & AI Insights ➡️", use_container_width=True, type="primary"):
                st.session_state["current_step"] = 3
                st.rerun()

    # ==========================================
    # STEP 3: STYLE PROFILE & STYLE SUGGESTIONS
    # ==========================================
    elif current_step == 3:
        st.markdown("### Step 3: Personalized Style Profile & Style Suggestions")
        st.caption("Review your calculated body shape profile, flattering color palette, and personalized style suggestions.")

        current_shape = st.session_state.get("calculated_shape", "Pear" if st.session_state["gender"] == "female" else "Trapezoid")
        gender = st.session_state["gender"]
        skin_tone = st.session_state["skin_tone"]
        occ_val = None if st.session_state["occasion"] == "all" else st.session_state["occasion"]

        shape_profile = get_shape_profile(current_shape, gender=gender)
        color_profile = recommend_colors_for_user(skin_tone, shape=current_shape, gender=gender)

        col_prof1, col_prof2 = st.columns(2)
        with col_prof1:
            st.markdown(f'Calculated Shape: <span class="shape-badge">{current_shape} ({gender.capitalize()})</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="goal-box"><b>Key Traits:</b> {shape_profile.get("traits", "N/A")}<br><br><b>Styling Goal:</b> {shape_profile.get("goal", "N/A")}</div>', unsafe_allow_html=True)

        with col_prof2:
            st.markdown(f"#### 🎨 Palette: `{color_profile.get('palette_name')}`")
            st.markdown("**Recommended Colors:**")
            rec_colors_html = "".join([f'<span class="color-chip">{c}</span>' for c in color_profile.get("recommended_colors", [])])
            st.markdown(rec_colors_html, unsafe_allow_html=True)

            st.markdown("**Colors to Avoid:**")
            avoid_colors_html = "".join([f'<span class="avoid-chip">{c}</span>' for c in color_profile.get("colors_to_avoid", [])])
            st.markdown(avoid_colors_html, unsafe_allow_html=True)

        # Style Suggestions Section
        st.markdown("---")
        st.markdown("### ✨ Style Suggestions")


        outfit_data = suggest_outfit(
            shape=current_shape,
            gender=gender,
            occasion=occ_val,
            skin_tone=skin_tone,
            include_groq_llm=True  # Always enabled by default
        )

        if "groq_llm_enrichment" in outfit_data:
            ai_info = outfit_data["groq_llm_enrichment"]
            col_ai1, col_ai2 = st.columns(2)
            with col_ai1:
                st.markdown(f"**Silhouette Insight**: {ai_info.get('styling_insights')}")
                st.markdown(f"**Color Blocking Advice**: {ai_info.get('color_palette_advice')}")
            with col_ai2:
                st.markdown(f"**Recommended Fabrics**: {ai_info.get('fabric_recommendations')}")
                st.markdown(f"**Pro Tip**: {ai_info.get('pro_tip')}")

        st.markdown("---")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("⬅️ Edit Preferences", use_container_width=True):
                st.session_state["current_step"] = 2
                st.rerun()
        with col_btn2:
            if st.button("View Copyable Recommendations 🛍️ ➡️", use_container_width=True, type="primary"):
                st.session_state["current_step"] = 4
                st.rerun()

    # ==========================================
    # STEP 4: SEARCHABLE RECOMMENDATIONS & OUTFITS
    # ==========================================
    elif current_step == 4:
        st.markdown("### Step 4: Searchable Dress & Outfit Recommendations")
        st.caption("Copy 1-click search terms (e.g. Cobalt Blue Boat-Neck Gown) to search on Amazon, Myntra, ASOS, or Google Shopping.")

        current_shape = st.session_state.get("calculated_shape", "Pear" if st.session_state["gender"] == "female" else "Trapezoid")
        gender = st.session_state["gender"]
        skin_tone = st.session_state["skin_tone"]
        occ_val = None if st.session_state["occasion"] == "all" else st.session_state["occasion"]

        outfit_data = suggest_outfit(
            shape=current_shape,
            gender=gender,
            occasion=occ_val,
            skin_tone=skin_tone,
            include_groq_llm=True  # Always enabled by default
        )

        tab_catalog, tab_outfit = st.tabs(["🛍️ Browse Copyable Search Grid", "👔 Complete Outfit Pairings"])

        catalog_df = load_catalog()
        matched_df = filter_catalog(
            catalog_df,
            shape=current_shape,
            gender=gender,
            occasion=occ_val,
            skin_tone=skin_tone
        )

        with tab_catalog:
            if matched_df.empty:
                st.warning("No matching items found for the selected filter combination. Showing all gender items.")
                matched_df = catalog_df[catalog_df["gender"] == gender]

            categories = ["All"] + list(matched_df["category"].str.capitalize().unique())
            selected_cat = st.radio("Category Filter:", options=categories, horizontal=True)

            display_df = matched_df if selected_cat == "All" else matched_df[matched_df["category"] == selected_cat.lower()]
            items_list = display_df.to_dict(orient="records")
            st.caption(f"Showing **{len(items_list)}** items matching **{current_shape}** ({gender}) and **{skin_tone}** skin tone.")

            cols_per_row = 3
            for i in range(0, len(items_list), cols_per_row):
                row_items = items_list[i:i + cols_per_row]
                grid_cols = st.columns(cols_per_row)
                for idx, item in enumerate(row_items):
                    with grid_cols[idx]:
                        render_product_card(
                            item,
                            enable_ai=True,  # Always default to True
                            shape=current_shape,
                            gender=gender,
                            skin_tone=skin_tone,
                            key_prefix=f"grid_{i}_{idx}_"
                        )

        with tab_outfit:
            render_outfit_combination(
                outfit_data,
                enable_ai=True,  # Always default to True
                shape=current_shape,
                gender=gender,
                skin_tone=skin_tone,
                key_prefix="tab_outfit_"
            )

        st.markdown("---")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("⬅️ Back to Profile Summary", use_container_width=True):
                st.session_state["current_step"] = 3
                st.rerun()
        with col_btn2:
            if st.button("🔄 Start Over / New Assessment", use_container_width=True):
                st.session_state["current_step"] = 1
                st.rerun()


if __name__ == "__main__":
    main()
