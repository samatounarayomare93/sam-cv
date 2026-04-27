import unittest

from core.linkedin_automator import NeuralLinkedIn


class _FakeAI:
    def __init__(self, response=None, raise_on_query=False):
        self._response = response if response is not None else {"nudge": "Hi Maya, your growth at Acme aligns with my HR ops focus. I would value connecting."}
        self._raise_on_query = raise_on_query

    async def structural_query(self, prompt):
        if self._raise_on_query:
            raise RuntimeError("query failed")
        return self._response

    def encode_shadow_text(self, text):
        return text


class _AsyncDB:
    def __init__(self):
        self.saved = None

    async def save_task(self, task_data):
        self.saved = task_data


class _SyncDB:
    def __init__(self):
        self.saved = None

    def save_task(self, task_data):
        self.saved = task_data


class LinkedInAutomatorTests(unittest.IsolatedAsyncioTestCase):
    async def test_generate_nudge_uses_structured_key(self):
        ai = _FakeAI(response={"nudge": "Short connection message"})
        linked = NeuralLinkedIn(ai)

        msg = await linked.generate_nudge("Maya", "Acme", "HR Manager", "New regional expansion")

        self.assertEqual(msg, "Short connection message")

    async def test_generate_nudge_hard_caps_to_200_chars(self):
        long_text = "A" * 400
        ai = _FakeAI(response={"nudge": long_text})
        linked = NeuralLinkedIn(ai)

        msg = await linked.generate_nudge("Maya", "Acme", "HR Manager")

        self.assertEqual(len(msg), 200)

    async def test_generate_nudge_fallback_when_ai_fails(self):
        ai = _FakeAI(raise_on_query=True)
        linked = NeuralLinkedIn(ai)

        msg = await linked.generate_nudge("Maya", "Acme", "HR Manager")

        self.assertIn("Maya", msg)
        self.assertLessEqual(len(msg), 200)

    async def test_record_nudge_task_handles_async_db(self):
        ai = _FakeAI()
        linked = NeuralLinkedIn(ai)
        db = _AsyncDB()

        await linked.record_nudge_task(db, "Maya", "Connect message", "https://linkedin.com/in/maya")

        self.assertIsNotNone(db.saved)
        self.assertEqual(db.saved["type"], "LINKEDIN_NUDGE")

    async def test_record_nudge_task_handles_sync_db(self):
        ai = _FakeAI()
        linked = NeuralLinkedIn(ai)
        db = _SyncDB()

        await linked.record_nudge_task(db, "Maya", "Connect message", "https://linkedin.com/in/maya")

        self.assertIsNotNone(db.saved)
        self.assertEqual(db.saved["target"], "Maya")


if __name__ == "__main__":
    unittest.main()
