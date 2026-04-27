$ErrorActionPreference = 'Stop'

Write-Host '=== Rita Job Automator Pre-Launch Test ==='
Write-Host ''
Write-Host '1) Python version'
py -3 --version
Write-Host ''
Write-Host '2) Pip version'
py -3 -m pip --version
Write-Host ''
Write-Host '3) Verify key environment variables'
@(
  'TEST_MODE',
  'BREVO_SMTP_LOGIN',
  'BREVO_SMTP_PASSWORD',
  'BREVO_API_KEY',
  'GMAIL_SMTP_USER',
  'GMAIL_APP_PASSWORD',
  'OUTLOOK_USER',
  'OUTLOOK_PASSWORD',
  'SUPABASE_URL',
  'SUPABASE_KEY',
  'GEMINI_API_KEY',
  'GROQ_API_KEY',
  'TELEGRAM_BOT_TOKEN',
  'TELEGRAM_CHAT_ID'
) | ForEach-Object {
  $value = [System.Environment]::GetEnvironmentVariable($_)
  if ([string]::IsNullOrWhiteSpace($value)) {
    Write-Host "$($_): MISSING"
  } else {
    Write-Host "$($_): SET"
  }
}
Write-Host ''
Write-Host '4) Create or refresh virtual environment'
if (-not (Test-Path '.\.venv')) {
  py -3 -m venv .venv
}
Write-Host ''
Write-Host '5) Install dependencies'
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Host ''
Write-Host '6) Run a syntax/import smoke test'
& .\.venv\Scripts\python.exe -m py_compile core\main_bot.py core\orchestrator.py core\ai_agent.py core\db_client.py core\follow_up_engine.py core\lead_schema.py core\lead_processor.py core\scrape_service.py core\smtp_engine.py core\cv_tailor.py core\run_reporter.py core\scheduler.py
Write-Host ''
Write-Host '7) Show preflight summary via a tiny Python probe'
& .\.venv\Scripts\python.exe -c "from core.orchestrator import AlphaOrchestrator; print(AlphaOrchestrator.validate_preflight())"
Write-Host ''
Write-Host '8) Send the forced test email to sam.dev1@hotmail.com'
& .\.venv\Scripts\python.exe -c "from core.smtp_engine import send_test_email; print(send_test_email())"
Write-Host ''
Write-Host '9) Optional: start the bot in test mode'
& .\.venv\Scripts\python.exe core\main_bot.py
