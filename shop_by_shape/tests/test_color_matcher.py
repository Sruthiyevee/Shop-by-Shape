import unittest
import sys
import os
import pandas as pd

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_3_color import (
    load_color_rules,
    normalize_skin_tone,
    get_color_palette,
    filter_catalog_by_color,
    recommend_colors_for_user
)
from phase_2_data import load_catalog, filter_catalog, suggest_outfit


class TestColorMatcher(unittest.TestCase):

    def test_load_color_rules(self):
        """
        Test 1: Verify loading of color_rules.json with required skin tone keys.
        """
        rules = load_color_rules()
        self.assertIn("warm", rules)
        self.assertIn("cool", rules)
        self.assertIn("neutral", rules)
        self.assertIn("deep", rules)
        self.assertIn("fair", rules)
        self.assertIn("medium_olive", rules)

    def test_normalize_skin_tone(self):
        """
        Test 2: Verify skin tone string normalization.
        """
        self.assertEqual(normalize_skin_tone("Warm Golden"), "warm")
        self.assertEqual(normalize_skin_tone("Cool Pink"), "cool")
        self.assertEqual(normalize_skin_tone("Deep Dark"), "deep")
        self.assertEqual(normalize_skin_tone("Fair Light"), "fair")
        self.assertEqual(normalize_skin_tone("Olive Medium"), "medium_olive")
        self.assertEqual(normalize_skin_tone("Unknown"), "neutral")

    def test_get_color_palette(self):
        """
        Test 3: Verify palette rules retrieval.
        """
        warm_pal = get_color_palette("warm")
        self.assertIn("Mustard Yellow", warm_pal["recommended_colors"])
        self.assertIn("Icy Blue", warm_pal["colors_to_avoid"])

        cool_pal = get_color_palette("cool")
        self.assertIn("Emerald Green", cool_pal["recommended_colors"])
        self.assertIn("Orange", cool_pal["colors_to_avoid"])

    def test_filter_catalog_by_color(self):
        """
        Test 4: Verify filtering catalog items by skin tone.
        """
        df = load_catalog()
        warm_items = filter_catalog_by_color(df, "warm")
        self.assertFalse(warm_items.empty)
        for _, row in warm_items.iterrows():
            tones = [t.strip() for t in str(row["ideal_skin_tones"]).split("|")]
            self.assertTrue("warm" in tones or "all" in tones or "neutral" in tones)

    def test_recommend_colors_for_user(self):
        """
        Test 5: Verify user color recommendation helper function output.
        """
        rec = recommend_colors_for_user("Fair Light", shape="Pear", gender="female")
        self.assertEqual(rec["normalized_skin_tone"], "fair")
        self.assertIn("recommended_colors", rec)
        self.assertIn("neutral_colors", rec)

    def test_suggest_outfit_with_skin_tone(self):
        """
        Test 6: Verify Phase 2 + Phase 3 integration in suggest_outfit with skin_tone.
        """
        outfit = suggest_outfit("Pear", gender="female", occasion="casual", skin_tone="warm")
        self.assertEqual(outfit["gender"], "female")
        self.assertEqual(outfit["shape"], "Pear")
        self.assertIn("suggested_outfit", outfit)
        self.assertFalse(len(outfit["all_matched_products"]) == 0)


if __name__ == '__main__':
    unittest.main()
