"""
Streamlit Quiz & Measurement Input Form Component

Renders the interactive onboarding forms for both Women and Men body shape evaluation.
"""

import streamlit as st
from typing import Dict, Tuple, Optional
from phase_1_logic import calculate_shape_from_quiz, calculate_shape_from_measurements


def render_quiz_form(gender: str = "female") -> Optional[str]:
    """
    Renders Quick Assessment Quiz form and calculates body shape.
    """
    st.markdown("### ⚡ Quick Assessment Questionnaire")
    st.caption("Answer 3 simple questions about your silhouette proportions.")

    with st.form("quiz_form"):
        if gender == "male":
            w_gain = st.selectbox(
                "1. Where do you tend to carry weight or bulk first?",
                options=[
                    "Evenly across shoulders and waist",
                    "Chest and upper shoulders",
                    "Midsection, abdomen, and stomach",
                    "Hips, thighs, and lower body"
                ]
            )
            ratio = st.selectbox(
                "2. How would you describe your shoulder-to-waist ratio?",
                options=[
                    "V-taper: Shoulders noticeably wider than hips",
                    "Trapezoid: Broad shoulders with defined tapered waist",
                    "Straight: Shoulders and waist are about equal",
                    "Narrower shoulders compared to waist/hips"
                ]
            )
            prominent = st.selectbox(
                "3. What is your most prominent visual feature?",
                options=[
                    "Athletic shoulders/chest",
                    "Stomach/midsection",
                    "Hips/thighs",
                    "Balanced overall build"
                ]
            )
        else:
            w_gain = st.selectbox(
                "1. Where do you notice weight gain first?",
                options=[
                    "Evenly all over",
                    "Hips and thighs",
                    "Upper body, arms, and shoulders",
                    "Midsection and abdomen"
                ]
            )
            ratio = st.selectbox(
                "2. How would you describe your upper-to-lower body ratio?",
                options=[
                    "Shoulders are narrower than hips",
                    "Shoulders are wider than hips",
                    "Shoulders and hips are about the same, with a defined waist",
                    "Shoulders and hips are about the same, with a straight waist"
                ]
            )
            prominent = st.selectbox(
                "3. What is your most prominent feature?",
                options=[
                    "Hips",
                    "Waist",
                    "Shoulders",
                    "Midsection"
                ]
            )

        submit = st.form_submit_button("✨ Find My Shape", use_container_width=True)
        if submit:
            return calculate_shape_from_quiz(w_gain, ratio, prominent, gender=gender)

    return None


def render_measurement_form(gender: str = "female") -> Optional[str]:
    """
    Renders Precision Measurement Calculator form with unit auto-detection and validation.
    """
    st.markdown("### 📏 Precision Measurement Calculator")
    st.caption("Enter your measurements in inches or centimeters.")

    with st.form("measurement_form"):
        col1, col2, col3 = st.columns(3)

        label_top = "Chest Measurement" if gender == "male" else "Bust Measurement"
        with col1:
            bust = st.number_input(f"{label_top}:", min_value=1.0, max_value=200.0, value=36.0, step=0.5)
        with col2:
            waist = st.number_input("Waist Measurement:", min_value=1.0, max_value=200.0, value=28.0, step=0.5)
        with col3:
            hips = st.number_input("Hips Measurement:", min_value=1.0, max_value=200.0, value=36.0, step=0.5)

        unit_hint = "cm" if (bust + waist + hips) / 3.0 > 50.0 else "inches"
        st.info(f"💡 Auto-detected measurement unit: **{unit_hint}**")

        submit = st.form_submit_button("📐 Calculate Exact Proportions", use_container_width=True)
        if submit:
            try:
                return calculate_shape_from_measurements(bust, waist, hips, gender=gender)
            except ValueError as e:
                st.error(f"Invalid measurement: {str(e)}")

    return None
