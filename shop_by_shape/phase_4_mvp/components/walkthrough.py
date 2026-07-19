"""
First-Time User Walkthrough Guide Component

Renders an interactive 4-step onboarding guide explaining how the application
calculates body shapes, matches skin tone color palettes, and generates copyable search queries.
"""

import streamlit as st


def render_walkthrough_guide():
    """
    Renders an expandable first-time user walkthrough guide banner.
    Supports responsive tab labels and accordion views for mobile/tablet screens.
    """
    with st.expander("👋 **New Here? Take the 1-Minute Guided Tour (How It Works)**", expanded=False):
        st.markdown("### Welcome to **Shop by Shape & Skin Tone**! 👗👔")
        st.caption("Learn how to find your perfect silhouette and flattering outfit recommendations in 4 simple steps:")

        # Concise tab titles for clean mobile rendering
        tab1, tab2, tab3, tab4 = st.tabs([
            "1️⃣ Onboarding",
            "2️⃣ Skin Tone",
            "3️⃣ Search Query",
            "4️⃣ AI Insights"
        ])

        with tab1:
            st.markdown("#### Step 1: Select Gender & Assessment Mode")
            st.markdown("""
            - Select **Women's Styling** 👩 or **Men's Styling** 👨 directly on the screen in Step 1.
            - Choose your preferred onboarding method:
              - **⚡ Quick Assessment Quiz**: Answer 3 simple visual proportion questions.
              - **📏 Precision Measurements**: Input exact Bust/Chest, Waist, and Hips (auto-detects inches vs cm).
            """)

        with tab2:
            st.markdown("#### Step 2: Select Skin Tone & Occasion")
            st.markdown("""
            - Select your **skin tone / undertone** directly on the screen (Warm, Cool, Neutral, Deep, Fair, Medium/Olive).
            - The engine instantly calculates:
              - **Your Body Shape**: Pear, Apple, Hourglass, Rectangle, Inverted Triangle (Women) or Trapezoid, Inverted Triangle, Rectangle, Triangle, Oval (Men).
              - **Key Traits & Styling Goals**: Flattering garment cuts to balance your silhouette.
              - **Skin Tone Color Palette**: Recommended colors and tones to avoid.
            """)

        with tab3:
            st.markdown("#### Step 3: Copy Searchable Recommendations")
            st.markdown("""
            - Browse filtered recommendation cards under Step 4's **🛍️ Browse Copyable Search Grid** or **👔 Complete Outfit Pairings** tabs.
            - Every recommendation includes a **📋 Copyable Search Recommendation** box (e.g. `Cobalt Blue Flared Pleated Midi Skirt`).
            - Simply click the copy icon on the search query box and paste it directly into **Google Shopping, Amazon, Myntra, or ASOS**!
            """)

        with tab4:
            st.markdown("#### Step 4: Default AI Styling Analysis")
            st.markdown("""
            - **Personalized AI Styling Insights** are automatically enabled for all recommendations!
            - Expand **💡 Why This Item Fits You (AI Fit Analysis)** on any recommendation card to get personalized advice on silhouette balance, color blocking, fabric drapes, and pro styling tips.
            - *Built with strict token optimization & in-memory caching for ultra-fast, reliable performance.*
            """)
