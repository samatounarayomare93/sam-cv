# Pre-Launch Test Commands

Run these from PowerShell at the repository root.

## 1) Check Python
```powershell
py -3 --version
py -3 -m pip --version
```

## 2) Create virtual environment
```powershell
py -3 -m venv .venv
```

## 3) Activate virtual environment
```powershell
.\.venv\Scripts\Activate.ps1
```

## 4) Install dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5) Syntax smoke test
```powershell
python -m py_compile core\main_bot.py core\orchestrator.py core\ai_agent.py core\db_client.py core\follow_up_engine.py core\lead_schema.py core\lead_processor.py core\scrape_service.py core\smtp_engine.py core\cv_tailor.py core\run_reporter.py core\scheduler.py
```

## 6) Print preflight summary
```powershell
python -c "from core.orchestrator import AlphaOrchestrator; print(AlphaOrchestrator.validate_preflight())"
```

## 7) Send the test email
```powershell
python -c "from core.smtp_engine import send_test_email; print(send_test_email())"
```

## 8) Start the bot in test mode
```powershell
python core\main_bot.py
```
