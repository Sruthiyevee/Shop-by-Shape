import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_5_ai_integration import (
    StylingRAGPipeline,
    explain_item_fit,
    explain_outfit_pairing,
    generate_fallback_fit_explanation
)


class TestAIIntegration(unittest.TestCase):

    def setUp(self):
        self.sample_item = {
            "id": "W001",
            "name": "Ribbed Boat-Neck Top",
            "category": "tops",
            "ideal_shapes": "pear|rectangle",
            "avoid_shapes": "inverted_triangle",
            "color": "Mustard Yellow",
            "description": "Elegant boat-neck top that draws attention to the shoulders."
        }

    def test_rag_pipeline_retrieval(self):
        """
        Test 1: Verify RAG indexing and context retrieval for shape and color rules.
        """
        rag = StylingRAGPipeline()
        self.assertTrue(len(rag.documents) > 0)

        docs = rag.retrieve_context(
            query="boat neck top",
            shape="Pear",
            gender="female",
            skin_tone="warm",
            k=2
        )
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]["type"], "shape_rule")
        self.assertEqual(docs[1]["type"], "color_rule")

    def test_fallback_fit_explanation(self):
        """
        Test 2: Verify deterministic fallback item fit explanation.
        """
        explanation = generate_fallback_fit_explanation(
            self.sample_item,
            shape="Pear",
            gender="female",
            skin_tone="warm"
        )
        self.assertEqual(explanation["status"], "fallback")
        self.assertFalse(explanation["is_live_llm"])
        self.assertIn("Ribbed Boat-Neck Top", explanation["fit_rationale"])

    @patch("phase_2_data.groq_enricher.get_groq_api_key")
    @patch("requests.post")
    def test_mocked_llm_item_fit_explanation(self, mock_post, mock_get_key):
        """
        Test 3: Verify live Groq LLM item fit analysis parsing when API key is present.
        """
        mock_get_key.return_value = "gsk_test_mock_key_12345"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"fit_rationale": "The boat neckline broadens your upper silhouette to balance hips.", "key_benefit": "Widens upper body visually."}'
                }
            }]
        }
        mock_post.return_value = mock_response

        exp = explain_item_fit(self.sample_item, shape="Pear", gender="female", skin_tone="warm")
        self.assertEqual(exp["status"], "success")
        self.assertTrue(exp["is_live_llm"])
        self.assertIn("broadens your upper silhouette", exp["fit_rationale"])

    def test_explain_outfit_pairing(self):
        """
        Test 4: Verify holistic outfit pairing rationale.
        """
        outfit = {
            "suggested_outfit": {
                "top": self.sample_item,
                "type": "two_piece"
            }
        }
        pairing_exp = explain_outfit_pairing(outfit, shape="Pear", gender="female", skin_tone="warm")
        self.assertIn("pairing_rationale", pairing_exp)
        self.assertIn("style_tip", pairing_exp)


if __name__ == '__main__':
    unittest.main()
