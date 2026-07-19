import unittest
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase_4_mvp.components.product_card import render_product_card, render_outfit_combination


class TestMVPComponents(unittest.TestCase):

    def test_mvp_imports(self):
        """
        Test 1: Verify Phase 4 MVP app module and components import cleanly.
        """
        import phase_4_mvp.app as app_module
        self.assertTrue(hasattr(app_module, "main"))
        self.assertTrue(hasattr(app_module, "apply_custom_css"))


if __name__ == '__main__':
    unittest.main()
