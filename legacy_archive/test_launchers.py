import unittest
from unittest import mock

import launch_main_bot


class LauncherTests(unittest.TestCase):
    @mock.patch.object(launch_main_bot, "main_bot", autospec=True)
    def test_main_invokes_main_bot(self, mocked_main_bot):
        with mock.patch.object(launch_main_bot.sys.path, "insert") as mocked_insert:
            exit_code = launch_main_bot.main()

        self.assertEqual(exit_code, 0)
        self.assertTrue(mocked_insert.called)
        self.assertTrue(mocked_main_bot.main.called)


if __name__ == "__main__":
    unittest.main()
