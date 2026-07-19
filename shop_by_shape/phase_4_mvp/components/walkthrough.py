"""
First-Time User Walkthrough Guide Component

Renders an interactive 4-step onboarding guide explaining how the application
calculates body shapes, matches skin tone color palettes, and generates copyable search queries.
"""

import streamlit as st


def render_walkthrough_guide():
    """
    Renders an expandable or tabbed first-time user walkthrough guide banner.
    """
    with st.expander("👋 **New Here? Take the 1-Minute Guided Tour (How It Works)**", expanded=False):
        st.markdown("### Welcome to **Shop by Shape & Skin Tone**! 👗👔")
        st.caption("Learn how to find your perfect silhouette and flattering outfit recommendations in 4 simple steps:")

        tab1, tab2, tab3, tab4 = st.tabs([
            "1️⃣ Choose Gender & Onboarding",
            "2️⃣ Calculate Shape & Skin Tone",
            "3️⃣ Explore Copyable Recommendations",
            "4️⃣ AI Styling Insights"
        ])

        with tab1:
            st.markdown("#### Step 1: Select Gender & Assessment Mode")
            st.markdown("""
            - Use the **sidebar** on the left to select **Women's Styling** 👩 or **Men's Styling** 👨.
            - Choose your preferred onboarding method:
              - **Quick Assessment Quiz**: Answer 3 simple questions about your weight distribution and shoulder-to-hip ratio.
              - **Precision Measurements**: Input exact Bust/Chest, Waist, and Hips (auto-detects inches vs cm).
            """)

        with tab2:
            st.markdown("#### Step 2: Select Skin Tone & View Profile")
            st.markdown("""
            - Select your **skin tone / undertone** in the sidebar (Warm, Cool, Neutral, Deep, Fair, Medium/Olive).
            - The engine instantly calculates:
              - **Your Body Shape**: Pear, Apple, Hourglass, Rectangle, Inverted Triangle (Women) or Trapezoid, Inverted Triangle, Rectangle, Triangle, Oval (Men).
              - **Key Traits & Styling Goals**: Ideal garment cuts to balance your silhouette.
              - **Skin Tone Color Palette**: Flattering recommended colors and tones to avoid.
            """)

        with tab3:
            st.markdown("#### Step 3: Copy & Search Recommendations")
            st.markdown("""
            - Browse filtered recommendation cards under the **🛍️ Browse Matching Catalog Grid** or **👔 Complete Outfit Pairings** tabs.
            - Every recommendation includes a **📋 Copyable Search Term** (e.g. `Cobalt Blue Boat-Neck Gown`).
            - Simply click the copy icon on the search query box and paste it into **Google Shopping, Amazon, Myntra, or ASOS**!
            """)

        with tab4:
            st.markdown("#### Step 4: AI Groq LLM Styling Analysis")
            st.markdown("""
            - Toggle **🤖 Enable AI Groq LLM Styling Insights** in the sidebar.
            - Expand **💡 Why This Item Fits You (AI Fit Analysis)** on any recommendation card to get personalized advice on silhouette balance, color blocking, fabric drapes, and pro styling secrets!
            - *Built with strict token optimization & in-memory caching for ultra-fast, reliable performance.*
            """)
