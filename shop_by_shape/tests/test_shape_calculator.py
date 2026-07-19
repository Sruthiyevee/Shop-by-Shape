import unittest
import sys
import os

# Add the project directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_1_logic import (
    calculate_shape_from_quiz,
    calculate_shape_from_measurements,
    calculate_male_shape_from_quiz,
    calculate_male_shape_from_measurements
)

class TestShapeCalculator(unittest.TestCase):
    
    def test_quiz_calculation(self):
        """
        Test 1: Verify that various quiz responses correctly map to target body shapes for women.
        """
        # Test Pear response
        shape_pear = calculate_shape_from_quiz(
            weight_gain="Hips and thighs",
            ratio="Shoulders are narrower than hips",
            prominent_feature="Hips"
        )
        self.assertEqual(shape_pear, "Pear")
        
        # Test Inverted Triangle response
        shape_inv = calculate_shape_from_quiz(
            weight_gain="Upper body and arms",
            ratio="Shoulders are wider than hips",
            prominent_feature="Shoulders"
        )
        self.assertEqual(shape_inv, "Inverted Triangle")

        # Test Hourglass response
        shape_hourglass = calculate_shape_from_quiz(
            weight_gain="Evenly all over",
            ratio="Shoulders and hips are about the same, with a defined waist",
            prominent_feature="Waist"
        )
        self.assertEqual(shape_hourglass, "Hourglass")

        # Test Apple response
        shape_apple = calculate_shape_from_quiz(
            weight_gain="Midsection and abdomen",
            ratio="Shoulders and hips are about the same, with a straight waist",
            prominent_feature="Midsection"
        )
        self.assertEqual(shape_apple, "Apple")

        # Test Rectangle response (Fallback)
        shape_rect = calculate_shape_from_quiz(
            weight_gain="Evenly",
            ratio="Straight silhouette",
            prominent_feature="None"
        )
        self.assertEqual(shape_rect, "Rectangle")

    def test_male_quiz_calculation(self):
        """
        Test 2: Verify quiz responses for male body shapes (Oval, Triangle, Inverted Triangle, Trapezoid, Rectangle).
        """
        # Test Oval male response
        shape_oval = calculate_shape_from_quiz(
            weight_gain="Midsection and stomach",
            ratio="Shoulders and hips equal",
            prominent_feature="Stomach",
            gender="male"
        )
        self.assertEqual(shape_oval, "Oval")

        # Test Triangle male response
        shape_tri = calculate_shape_from_quiz(
            weight_gain="Hips and lower body",
            ratio="Shoulders are narrower than hips",
            prominent_feature="Hips",
            gender="men"
        )
        self.assertEqual(shape_tri, "Triangle")

        # Test Inverted Triangle male response
        shape_inv_male = calculate_male_shape_from_quiz(
            weight_gain="Chest and broad shoulders",
            ratio="V-taper shoulders wider than hips",
            prominent_feature="Chest"
        )
        self.assertEqual(shape_inv_male, "Inverted Triangle")

        # Test Trapezoid male response
        shape_trap = calculate_male_shape_from_quiz(
            weight_gain="Evenly",
            ratio="Defined tapered waist",
            prominent_feature="Athletic build"
        )
        self.assertEqual(shape_trap, "Trapezoid")

        # Test Rectangle male response
        shape_rect_male = calculate_male_shape_from_quiz(
            weight_gain="Evenly",
            ratio="Straight chest and hips",
            prominent_feature="None"
        )
        self.assertEqual(shape_rect_male, "Rectangle")

    def test_quiz_edge_cases(self):
        """
        Test 3: Verify case insensitivity, whitespace trimming, and handling of empty/None strings.
        """
        # Case insensitivity & whitespace
        self.assertEqual(
            calculate_shape_from_quiz("  HIPS  ", " NARROWER ", " HIPS ", gender=" FEMALE "),
            "Pear"
        )
        self.assertEqual(
            calculate_male_shape_from_quiz("  STOMACH ", " EQUAL ", " MIDSECTION "),
            "Oval"
        )
        # Empty inputs should safely fall back to Rectangle
        self.assertEqual(calculate_shape_from_quiz("", "", ""), "Rectangle")
        self.assertEqual(calculate_male_shape_from_quiz(None, None, None), "Rectangle")

    def test_measurements_inches(self):
        """
        Test 4: Verify that measurements in inches correctly map to target female body shapes.
        """
        # Hourglass: Bust=36, Waist=26, Hips=36 -> (36-36)=0 <=2, (36-26)=10 >=8
        self.assertEqual(calculate_shape_from_measurements(36, 26, 36), "Hourglass")
        
        # Pear: Bust=34, Waist=26, Hips=40 -> (40-34)=6 >=2, (40-26)=14 >=7
        self.assertEqual(calculate_shape_from_measurements(34, 26, 40), "Pear")
        
        # Inverted Triangle: Bust=40, Waist=28, Hips=34 -> (40-34)=6 >=2, (40-28)=12 >=7
        self.assertEqual(calculate_shape_from_measurements(40, 28, 34), "Inverted Triangle")
        
        # Apple: Bust=38, Waist=37, Hips=38 -> Waist is close to bust/hips
        self.assertEqual(calculate_shape_from_measurements(38, 37, 38), "Apple")
        
        # Rectangle: Bust=36, Waist=32, Hips=36 -> Waist is not small enough, bust/hips are close
        self.assertEqual(calculate_shape_from_measurements(36, 32, 36), "Rectangle")

    def test_male_measurements_inches(self):
        """
        Test 5: Verify that measurements in inches correctly map to target male body shapes.
        """
        # Oval: Chest=38, Waist=42, Hips=38 -> Waist > Chest and Waist > Hips
        self.assertEqual(calculate_shape_from_measurements(38, 42, 38, gender="male"), "Oval")
        
        # Triangle: Chest=36, Waist=36, Hips=40 -> Hips - Chest = 4 >= 2.0
        self.assertEqual(calculate_shape_from_measurements(36, 36, 40, gender="men"), "Triangle")
        
        # Inverted Triangle: Chest=44, Waist=32, Hips=36 -> Chest-Waist=12 >=7, Chest-Hips=8 >=3
        self.assertEqual(calculate_male_shape_from_measurements(44, 32, 36), "Inverted Triangle")
        
        # Trapezoid: Chest=40, Waist=34, Hips=38 -> Chest-Waist=6 >=2, abs(Chest-Hips)=2 <=4
        self.assertEqual(calculate_male_shape_from_measurements(40, 34, 38), "Trapezoid")
        
        # Rectangle: Chest=38, Waist=37, Hips=38 -> Chest-Waist=1 < 2
        self.assertEqual(calculate_male_shape_from_measurements(38, 37, 38), "Rectangle")

    def test_measurements_centimeters(self):
        """
        Test 6: Verify that measurements in centimeters are auto-detected, converted, and mapped for both genders.
        """
        # Hourglass in cm: Bust=91.44 cm (36"), Waist=66.04 cm (26"), Hips=91.44 cm (36")
        self.assertEqual(calculate_shape_from_measurements(91.4, 66.0, 91.4), "Hourglass")
        
        # Pear in cm: Bust=86.36 cm (34"), Waist=66.04 cm (26"), Hips=101.6 cm (40")
        self.assertEqual(calculate_shape_from_measurements(86.4, 66.0, 101.6), "Pear")

        # Male Trapezoid in cm: Chest=101.6 cm (40"), Waist=86.36 cm (34"), Hips=96.52 cm (38")
        self.assertEqual(calculate_male_shape_from_measurements(101.6, 86.4, 96.5), "Trapezoid")

    def test_invalid_measurements(self):
        """
        Test 7 (Edge Cases): Verify that invalid/zero/negative/non-numeric values raise ValueError.
        """
        # Zero values
        with self.assertRaises(ValueError):
            calculate_shape_from_measurements(0, 28, 36)
        # Negative values
        with self.assertRaises(ValueError):
            calculate_shape_from_measurements(36, -5, 36)
        with self.assertRaises(ValueError):
            calculate_male_shape_from_measurements(-40, 32, 36)
        # Non-numeric types (strings, booleans, None)
        with self.assertRaises(ValueError):
            calculate_shape_from_measurements("36", 28, 36)
        with self.assertRaises(ValueError):
            calculate_shape_from_measurements(True, 28, 36)
        with self.assertRaises(ValueError):
            calculate_male_shape_from_measurements(40, None, 36)

if __name__ == '__main__':
    unittest.main()


