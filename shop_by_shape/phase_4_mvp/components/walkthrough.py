"""
First-Time User Walkthrough Guide Component

Renders an interactive 4-step onboarding guide explaining how the application
calculates body shapes, matches skin tone color palettes, and generates copyable search queries.
Uses an accordion view for 100% responsiveness across all mobile, tablet, and desktop viewports.
"""

import streamlit as st


def render_walkthrough_guide():
    """
    Renders an expandable first-time user walkthrough guide banner with an accordion layout.
    Guarantees 100% responsiveness on mobile, tablet, and desktop viewports without overflow.
    """
    with st.expander("👋 **New Here? Take the 1-Minute Guided Tour (How It Works)**", expanded=False):
        st.markdown("### Welcome to **Shop by Shape & Skin Tone**! 👗👔")
        st.caption("Follow these 4 simple steps to find your perfect fit & flattering clothing search queries:")

        with st.expander("1️⃣ Step 1: Select Gender & Assessment Mode", expanded=True):
            st.markdown("""
            - Select **Women's Styling** 👩 or **Men's Styling** 👨 directly on the screen in Step 1.
            - Choose your preferred onboarding method:
              - **⚡ Quick Assessment Quiz**: Answer 3 simple visual proportion questions.
              - **📏 Precision Measurements**: Input exact Bust/Chest, Waist, and Hips (auto-detects inches vs cm).
            """)

        with st.expander("2️⃣ Step 2: Select Skin Tone & Occasion", expanded=False):
            st.markdown("""
            - Select your **skin tone / undertone** directly on the screen (Warm, Cool, Neutral, Deep, Fair, Medium/Olive).
            - Select your target wearing occasion (All Occasions, Casual, Formal, Party).
            - The engine instantly calculates:
              - **Your Body Shape Profile** (Pear, Apple, Hourglass, Rectangle, Inverted Triangle for Women; Trapezoid, Inverted Triangle, Rectangle, Triangle, Oval for Men).
              - **Key Traits & Proportion Goals** to balance your silhouette.
              - **Skin Tone Color Palette**: Flattering recommended colors and tones to avoid.
            """)

        with st.expander("3️⃣ Step 3: View Style Profile & Style Suggestions", expanded=False):
            st.markdown("""
            - Review your calculated body shape profile, flattering color chips, and **✨ Style Suggestions**.
            - **Personalized AI Styling Insights** (silhouette advice, color placement, fabric drapes, pro tips) are automatically enabled by default!
            """)

        with st.expander("4️⃣ Step 4: Copy Searchable Recommendations", expanded=False):
            st.markdown("""
            - Browse filtered recommendation cards under the **🛍️ Copyable Search Grid** or **👔 Complete Outfit Pairings** tabs.
            - Every recommendation includes a **📋 Copyable Search Query** (e.g. `Cobalt Blue Flared Pleated Midi Skirt`).
            - Click the copy icon on the search box and paste it directly into **Google Shopping, Amazon, Myntra, or ASOS**!
            """)
