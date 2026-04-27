import unittest
from datetime import datetime, timezone

from core.core_utils import build_fallback_email, is_recent, normalize_company_slug


class CoreUtilsTests(unittest.TestCase):
    def test_normalize_company_slug(self):
        self.assertEqual(normalize_company_slug("Sam Salameh Group"), "samcordahigroup")

    def test_build_fallback_email(self):
        self.assertEqual(build_fallback_email("Example Company"), "careers@examplecompany.com")

    def test_is_recent_accepts_iso_timestamp(self):
        self.assertTrue(is_recent(datetime.now(timezone.utc).isoformat(), hours=24))

    def test_is_recent_rejects_old_timestamp(self):
        self.assertFalse(is_recent("2000-01-01T00:00:00+00:00", hours=24))


if __name__ == "__main__":
    unittest.main()
