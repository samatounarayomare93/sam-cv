import unittest

from core.main_bot_helpers import fast_filter, is_relevant_to_cv, is_valid_target, lead_priority_score, render_application_body


class MainBotHelperTests(unittest.TestCase):
    def test_is_valid_target_accepts_prime_lebanon_role(self):
        ok, reason, salary, perks = is_valid_target(
            company_name="Example Co",
            location="Beirut",
            salary="6500",
            phase="lebanon",
            description="Visa sponsorship and relocation package"
        )
        self.assertTrue(ok)
        self.assertIn("Valid", reason)
        self.assertGreaterEqual(salary, 6500)
        self.assertGreaterEqual(perks, 1)

    def test_fast_filter_rejects_obviously_wrong_location(self):
        lead = {
            "location": "Tokyo",
            "salary_min": "0",
            "job_title": "HR Manager",
        }
        self.assertFalse(fast_filter(lead, current_phase="global"))

    def test_fast_filter_accepts_lebanon_remote_hr_role(self):
        lead = {
            "location": "Remote Lebanon",
            "salary_min": "0",
            "job_title": "HR Manager",
        }
        self.assertTrue(fast_filter(lead, current_phase="lebanon"))

    def test_lead_priority_scores_senior_hr_remote_higher(self):
        lead = {
            "job_title": "Senior HR Manager",
            "description": "Visa sponsorship and relocation available",
            "location": "Remote Worldwide",
            "salary_min": "120000",
        }
        score = lead_priority_score(lead)
        self.assertGreaterEqual(score, 40)

    def test_render_application_body_replaces_placeholders(self):
        body = render_application_body(
            "Dear {company_name}, I am applying for {job_title}.",
            {"company_name": "Acme", "job_title": "Operations Manager"}
        )
        self.assertEqual(body, "Dear Acme, I am applying for Operations Manager.")

    def test_render_application_body_leaves_plain_text_intact(self):
        body = render_application_body(
            "Plain text application",
            {"company_name": "Acme", "job_title": "Operations Manager"}
        )
        self.assertEqual(body, "Plain text application")

    def test_is_relevant_to_cv_prefers_hr_keywords(self):
        # "HR Manager" is in BANNED_TITLES (Sam is a Network Engineer, not HR).
        # Use a valid IT/network title that matches TARGET_KEYWORDS instead.
        result = is_relevant_to_cv("Operations Manager", "Hiring now")
        self.assertTrue(result[0])
        self.assertIn("Matched", result[1])

    def test_is_relevant_to_cv_rejects_unrelated_role(self):
        result = is_relevant_to_cv("Warehouse Worker", "Manual labor")
        self.assertFalse(result[0])


if __name__ == "__main__":
    unittest.main()
