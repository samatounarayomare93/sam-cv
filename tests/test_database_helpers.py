import unittest
from unittest import mock

from core import database


class DatabaseHelperTests(unittest.TestCase):
    def test_encode_param_quotes_special_characters(self):
        self.assertEqual(database._encode_param("A B/C"), "A%20B%2FC")

    @mock.patch.object(database, "get_global_stats", return_value={"leads": 7, "applications": 3})
    def test_get_stats_maps_global_stats(self, mocked_stats):
        stats = database.get_stats()
        self.assertEqual(stats["leads"], 7)
        self.assertEqual(stats["apps"], 3)
        self.assertTrue(mocked_stats.called)

    def test_is_duplicate_without_supabase_returns_false(self):
        with mock.patch.object(database.config, "SUPABASE_URL", "", create=True), \
             mock.patch.object(database.config, "SUPABASE_KEY", "", create=True):
            self.assertFalse(database.is_duplicate("https://example.com/job/123"))


if __name__ == "__main__":
    unittest.main()
