import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_2_data import (
    enrich_shape_mapping,
    get_groq_api_key,
    get_groq_model,
    suggest_outfit
)
from phase_2_data.groq_enricher import generate_fallback_enrichment


class TestGroqEnricher(unittest.TestCase):

    def test_fallback_enrichment(self):
        """
        Test 1: Verify deterministic fallback styling advice generation.
        """
        fb_female = generate_fallback_enrichment("Pear", gender="female", occasion="casual")
        self.assertEqual(fb_female["status"], "fallback")
        self.assertFalse(fb_female["is_live_llm"])
        self.assertIn("styling_insights", fb_female)
        self.assertIn("color_palette_advice", fb_female)
        self.assertIn("fabric_recommendations", fb_female)

        fb_male = generate_fallback_enrichment("Trapezoid", gender="male", occasion="formal")
        self.assertEqual(fb_male["status"], "fallback")
        self.assertIn("Trapezoid", fb_male["styling_insights"])

    @patch("phase_2_data.groq_enricher.get_groq_api_key")
    @patch("requests.post")
    def test_mocked_groq_api_call(self, mock_post, mock_get_key):
        """
        Test 2: Verify live LLM payload handling when Groq API succeeds.
        """
        mock_get_key.return_value = "gsk_test_mock_key_12345"
        
        # Mock HTTP 200 response from Groq API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"styling_insights": "Highlight defined waist", "color_palette_advice": "Wear navy and burgundy", "fabric_recommendations": "Soft silk blends", "pro_tip": "Add a thin belt"}'
                }
            }]
        }
        mock_post.return_value = mock_response

        res = enrich_shape_mapping("Hourglass", gender="female", occasion="party")
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["is_live_llm"])
        self.assertEqual(res["styling_insights"], "Highlight defined waist")
        self.assertEqual(res["color_palette_advice"], "Wear navy and burgundy")
        self.assertEqual(res["fabric_recommendations"], "Soft silk blends")
        self.assertEqual(res["pro_tip"], "Add a thin belt")

    @patch("phase_2_data.groq_enricher.get_groq_api_key")
    @patch("requests.post")
    def test_suggest_outfit_integration_with_groq(self, mock_post, mock_get_key):
        """
        Test 3: Verify suggest_outfit include_groq_llm flag attaches LLM enrichment dict.
        """
        mock_get_key.return_value = "gsk_test_mock_key_12345"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"styling_insights": "Structured shoulders", "color_palette_advice": "Monochrome dark", "fabric_recommendations": "Crisp wool blend", "pro_tip": "Tailored fit"}'
                }
            }]
        }
        mock_post.return_value = mock_response

        outfit = suggest_outfit("Trapezoid", gender="male", occasion="formal", include_groq_llm=True)
        self.assertIn("groq_llm_enrichment", outfit)
        self.assertEqual(outfit["groq_llm_enrichment"]["status"], "success")
        self.assertTrue(outfit["groq_llm_enrichment"]["is_live_llm"])


if __name__ == '__main__':
    unittest.main()
