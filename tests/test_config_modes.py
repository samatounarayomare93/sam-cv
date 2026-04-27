import unittest

from core import config


class ConfigModeTests(unittest.TestCase):
    def test_offline_safe_mode_is_boolean(self):
        self.assertIsInstance(config.OFFLINE_SAFE_MODE, bool)

    def test_local_fallbacks_enabled_default_true(self):
        self.assertIsInstance(config.ENABLE_LOCAL_FALLBACKS, bool)

    def test_use_ai_analysis_is_boolean(self):
        self.assertIsInstance(config.USE_AI_ANALYSIS, bool)

    def test_use_telegram_is_boolean(self):
        self.assertIsInstance(config.USE_TELEGRAM, bool)


if __name__ == "__main__":
    unittest.main()
