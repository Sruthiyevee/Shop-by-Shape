import unittest
import sys
import os
import pandas as pd

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_2_data import (
    load_shape_rules,
    normalize_shape_name,
    get_shape_profile,
    load_catalog,
    filter_catalog,
    suggest_outfit
)


class TestDataLoader(unittest.TestCase):

    def test_load_shape_rules(self):
        """
        Test 1: Verify shape_rules.json loads and contains top-level keys.
        """
        rules = load_shape_rules()
        self.assertIn("women", rules)
        self.assertIn("men", rules)
        self.assertIn("usage_notes", rules)
        self.assertIn("pear", rules["women"])
        self.assertIn("trapezoid", rules["men"])

    def test_normalize_shape_name(self):
        """
        Test 2: Verify normalization of shape strings to snake_case keys.
        """
        self.assertEqual(normalize_shape_name("Inverted Triangle"), "inverted_triangle")
        self.assertEqual(normalize_shape_name("Pear"), "pear")
        self.assertEqual(normalize_shape_name("hourglass"), "hourglass")
        self.assertEqual(normalize_shape_name("Apple-Shoulder"), "apple_shoulder")
        self.assertEqual(normalize_shape_name(""), "")

    def test_get_shape_profile_women(self):
        """
        Test 3: Verify profile retrieval for female body shapes.
        """
        pear_profile = get_shape_profile("Pear", gender="female")
        self.assertIn("traits", pear_profile)
        self.assertIn("goal", pear_profile)
        self.assertIn("recommended", pear_profile)
        self.assertIn("occasion_notes", pear_profile)
        self.assertIn("boat neck", pear_profile["recommended"]["tops"])

        inv_profile = get_shape_profile("Inverted Triangle", gender="female")
        self.assertEqual(inv_profile["aka"], ["apple-shoulder", "athletic"])

    def test_get_shape_profile_men(self):
        """
        Test 4: Verify profile retrieval for male body shapes.
        """
        trap_profile = get_shape_profile("Trapezoid", gender="male")
        self.assertIn("traits", trap_profile)
        self.assertIn("suits", trap_profile["recommended"])

        oval_profile = get_shape_profile("Oval", gender="men")
        self.assertIn("vertical stripes", oval_profile["recommended"]["tops"])

    def test_load_catalog(self):
        """
        Test 5: Verify loading mock_catalog.csv into a DataFrame with required columns.
        """
        df = load_catalog()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        required_cols = {"id", "name", "gender", "category", "ideal_shapes", "avoid_shapes", "occasion", "price"}
        self.assertTrue(required_cols.issubset(set(df.columns)))

    def test_filter_catalog_women(self):
        """
        Test 6: Verify catalog filtering for female shapes and categories.
        """
        df = load_catalog()
        
        # Filter tops for Pear female
        pear_tops = filter_catalog(df, shape="Pear", gender="female", category="tops")
        self.assertFalse(pear_tops.empty)
        for _, row in pear_tops.iterrows():
            self.assertEqual(row["gender"], "female")
            self.assertEqual(row["category"], "tops")
            self.assertIn("pear", row["ideal_shapes"])

        # Filter dresses for Hourglass female
        hourglass_dresses = filter_catalog(df, shape="Hourglass", gender="female", category="dresses")
        self.assertFalse(hourglass_dresses.empty)

    def test_filter_catalog_men(self):
        """
        Test 7: Verify catalog filtering for male shapes, categories, and occasions.
        """
        df = load_catalog()

        # Filter suits for Trapezoid male formal
        trap_suits = filter_catalog(df, shape="Trapezoid", gender="male", category="suits", occasion="formal")
        self.assertFalse(trap_suits.empty)

        # Filter bottoms for Oval male casual
        oval_bottoms = filter_catalog(df, shape="Oval", gender="men", category="bottoms", occasion="casual")
        self.assertFalse(oval_bottoms.empty)

    def test_suggest_outfit(self):
        """
        Test 8: Verify structured outfit suggestions generation.
        """
        # Suggest female casual outfit for Pear
        rec_female = suggest_outfit("Pear", gender="female", occasion="casual")
        self.assertEqual(rec_female["gender"], "female")
        self.assertEqual(rec_female["shape"], "Pear")
        self.assertIn("suggested_outfit", rec_female)

        # Suggest male formal outfit for Trapezoid
        rec_male = suggest_outfit("Trapezoid", gender="male", occasion="formal")
        self.assertEqual(rec_male["gender"], "male")
        self.assertIn("suggested_outfit", rec_male)

    def test_file_not_found_error(self):
        """
        Test 9: Verify FileNotFoundError when loading non-existent files.
        """
        with self.assertRaises(FileNotFoundError):
            load_shape_rules("non_existent_rules.json")
        with self.assertRaises(FileNotFoundError):
            load_catalog("non_existent_catalog.csv")


if __name__ == '__main__':
    unittest.main()
