import unittest

from data_validator import DataValidator, validate_company_name, validate_email, validate_job_title, validate_location, validate_salary, validate_url


class DataValidatorTests(unittest.TestCase):
    def test_validate_email_accepts_standard_address(self):
        self.assertEqual(validate_email("person@example.com"), (True, None))

    def test_validate_email_rejects_disposable(self):
        ok, reason = validate_email("person@mailinator.com")
        self.assertFalse(ok)
        self.assertIn("Disposable", reason)

    def test_validate_salary_parses_string(self):
        self.assertEqual(validate_salary("$1,250"), (True, 1250))

    def test_validate_job_title_rejects_placeholder(self):
        ok, reason = validate_job_title("Test Job")
        self.assertFalse(ok)
        self.assertIn("Test", reason)

    def test_validate_location_accepts_normal_location(self):
        self.assertEqual(validate_location("Beirut"), (True, None))

    def test_validate_company_name_accepts_normal_name(self):
        self.assertEqual(validate_company_name("Acme Inc"), (True, None))

    def test_validate_url_accepts_http(self):
        self.assertEqual(validate_url("https://example.com/job"), (True, None))

    def test_validate_lead_full_valid(self):
        lead = {
            "company_name": "Acme Inc",
            "job_title": "HR Manager",
            "email": "hr@acme.com",
            "location": "Beirut",
            "salary": "$2500",
            "url": "https://example.com/job"
        }
        ok, errors = DataValidator.validate_lead(lead)
        self.assertTrue(ok)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
