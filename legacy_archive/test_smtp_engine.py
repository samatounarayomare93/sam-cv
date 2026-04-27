import unittest
from unittest import mock

import smtp_engine


class SmtpEngineTests(unittest.TestCase):
    @mock.patch.object(smtp_engine, "_get_available_providers", return_value=[])
    def test_send_email_returns_false_without_providers(self, mocked_providers):
        result = smtp_engine.send_email(
            to_email="sam.dev1@hotmail.com",
            company_name="Test Company",
            job_title="Test Role",
            custom_body="TEST EMAIL",
            platform="test",
            mission_type="test",
            pdf_path=None,
        )
        self.assertFalse(result)
        self.assertTrue(mocked_providers.called)

    @mock.patch.object(smtp_engine, "send_email", return_value=True)
    def test_send_strike_delegates_to_send_email(self, mocked_send_email):
        lead = {
            "company_name": "Acme",
            "email": "hr@acme.com",
            "job_title": "HR Manager",
            "custom_body": "TEST EMAIL",
            "mission_type": "test",
        }
        self.assertTrue(smtp_engine.send_strike(lead, None))
        self.assertTrue(mocked_send_email.called)


if __name__ == "__main__":
    unittest.main()
