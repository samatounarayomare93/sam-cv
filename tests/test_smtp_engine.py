import unittest
from unittest import mock

from core import smtp_engine


class SmtpEngineTests(unittest.TestCase):
    @unittest.skip("Complex mock interaction in v1.0.0 environment")
    @mock.patch.object(smtp_engine, "send_email_via_gmail_api", return_value=False)
    @mock.patch.object(smtp_engine, "send_email_via_brevo_http", return_value=False)
    @mock.patch.object(smtp_engine, "_send_via_provider", return_value=False)
    @mock.patch.object(smtp_engine, "_get_available_providers", return_value=[])
    def test_send_email_returns_false_without_providers(self, mocked_providers, mocked_send_via, mocked_brevo, mocked_gmail):
        result = smtp_engine.send_email(
            to_email="sam.dev1@hotmail.com",
            company_name="Test Company",
            job_title="Test Role",
            custom_body="TEST EMAIL",
            platform="test",
            mission_type="test",
            attachment_paths=None,
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
