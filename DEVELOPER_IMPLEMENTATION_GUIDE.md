# 🔧 DEVELOPER IMPLEMENTATION GUIDE

Complete guide for developers implementing new features in Project Chronos.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Core Modules Reference](#core-modules-reference)
5. [Adding Features](#adding-features)
6. [Testing Guidelines](#testing-guidelines)
7. [Code Standards](#code-standards)
8. [Common Tasks](#common-tasks)
9. [Debugging](#debugging)

---

## Architecture Overview

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT CHRONOS v1.0.0                   │
├─────────────────────────────────────────────────────────────┤
│
│  EXTERNAL INTEGRATIONS
│  ├─ Telegram Bot API (Control & Monitoring)
│  ├─ Google Gemini / Groq (LLM for Job Analysis)
│  ├─ Gmail API / Brevo SMTP (Email Delivery)
│  ├─ Supabase / SQLite (Database)
│  └─ Web Scrapers (Lead Discovery)
│
├─────────────────────────────────────────────────────────────┤
│
│  CORE ENGINE (async orchestration)
│  ├─ run.py (Main supervisor)
│  ├─ core/main_bot.py (AlphaOrchestrator - job automation)
│  └─ core/telegram_dashboard.py (SovereignDashboard - C2)
│
├─────────────────────────────────────────────────────────────┤
│
│  PROCESSING PIPELINE
│  ├─ core/lead_processor.py (Filter & Score Leads)
│  ├─ core/ai_agent.py (LLM Analysis - OmniIntelligence)
│  ├─ core/pdf_generator.py (CV Generation - FPDF2)
│  ├─ core/smtp_engine.py (Email Dispatch)
│  └─ core/follow_up_engine.py (Scheduled Follow-ups)
│
├─────────────────────────────────────────────────────────────┤
│
│  DATA LAYER
│  ├─ core/db_client.py (RealityShapingDB - Dual-DB)
│  ├─ Supabase (Cloud Primary)
│  └─ SQLite (Local Fallback)
│
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles
1. **Fallback Architecture**: Multiple providers for each service
2. **Async-First**: asyncio for concurrent operations
3. **Swarm Intelligence**: Leadership election for multi-instance
4. **Cloud-Ready**: Render.com compatible
5. **Modular Design**: Each component independent and testable

---

## Development Environment Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/Sam-Cordahi/Sam_Job_Automator.git
cd Sam_Job_Automator
```

### Step 2: Create Virtual Environment
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example
cp .env.example .env

# Edit .env with your credentials
# Minimum required:
#   - ONE LLM key (GEMINI_API_KEY or GROQ_API_KEY)
#   - ONE email provider (GMAIL_SMTP_USER or BREVO_SMTP_LOGIN)
#   - TELEGRAM_BOT_TOKEN
```

### Step 5: Verify Setup
```bash
# Compile check
python -m py_compile core/*.py

# Test imports
python -c "import core.main_bot; print('✅ Imports OK')"

# Run locally
python run.py
```

---

## Project Structure

```
Sam_Job_Automator/
├── core/                              # Main business logic
│   ├── main_bot.py                   # AlphaOrchestrator - job automation engine
│   ├── telegram_dashboard.py         # SovereignDashboard - 50 Telegram commands
│   ├── ai_agent.py                   # OmniIntelligence - LLM interface
│   ├── db_client.py                  # RealityShapingDB - database abstraction
│   ├── smtp_engine.py                # Email delivery (Gmail + Brevo)
│   ├── pdf_generator.py              # FPDF2 CV generation
│   ├── lead_processor.py             # Lead filtering & scoring
│   ├── follow_up_engine.py           # Scheduled follow-ups
│   ├── scrapers/
│   │   ├── scraper.py               # DuckDuckGo scraper
│   │   ├── omni_crawler.py          # Multi-source crawler
│   │   ├── healer_intelligence.py   # Intelligence engine
│   │   └── linkedin_automator.py    # LinkedIn scraper
│   ├── utils/
│   │   ├── cv_tailor.py             # CV customization
│   │   ├── config.py                # Configuration loading
│   │   └── core_utils.py            # Utility functions
│   └── ...
│
├── tests/                            # Unit tests
│   ├── test_main_bot_helpers.py
│   ├── test_smtp_engine.py
│   ├── test_data_validator.py
│   └── ...
│
├── .github/
│   ├── workflows/
│   │   ├── ci_quality.yml            # Test & coverage
│   │   ├── job_bot.yml               # Scheduled automation
│   │   ├── 24_7_telegram_bot.yml    # Cloud deployment
│   │   └── release.yml               # Versioning
│   ├── CONTRIBUTING.md               # Developer guidelines
│   └── pull_request_template.md
│
├── run.py                            # Main entry point (spawns dual processes)
├── launch_sam.py                    # Telegram bot launcher (Render.com)
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment template
├── README.md                         # Project overview
├── QUICK_START.md                    # 5-minute setup
├── DEPLOYMENT_SECRETS_GUIDE.md      # Configuration reference
├── PRODUCTION_READINESS_CHECKLIST.md # Go-live checklist
├── MONITORING_AND_OPERATIONS.md     # Operations guide
└── render.yaml                       # Cloud deployment config
```

---

## Core Modules Reference

### core/main_bot.py - AlphaOrchestrator
**Purpose**: Master orchestration engine for job automation  
**Main Class**: `AlphaOrchestrator`  
**Entry Point**: `execute_divine_loop()` (async)

```python
from core.main_bot import AlphaOrchestrator

# Usage
async def main():
    orchestrator = AlphaOrchestrator()
    await orchestrator.execute_divine_loop()
```

**Key Methods**:
- `execute_divine_loop()` - Main automation cycle
- `discover_leads()` - Find job opportunities
- `process_batch()` - Analyze and score leads
- `dispatch_applications()` - Send CVs
- `schedule_followups()` - Plan follow-ups

---

### core/telegram_dashboard.py - SovereignDashboard
**Purpose**: Command & control via Telegram (50+ commands)  
**Main Class**: `SovereignDashboard`  
**Entry Point**: `ignite()`

```python
from core.telegram_dashboard import SovereignDashboard

# Usage
async def main():
    dashboard = SovereignDashboard()
    await dashboard.ignite()
```

**Command Categories**:
1. **Status**: /status, /health, /ping, /uptime
2. **Queue**: /queue, /current, /delivered, /failed
3. **Analytics**: /stats, /performance, /analytics
4. **Testing**: /test_email, /test_ai, /test_database
5. **Admin**: /restart, /pause, /resume, /force_cycle

---

### core/ai_agent.py - OmniIntelligence
**Purpose**: LLM integration with fallback chain  
**Main Class**: `OmniIntelligence`  
**Fallback Chain**: Gemini → Groq

```python
from core.ai_agent import OmniIntelligence

ai = OmniIntelligence()

# Analyze job
analysis = await ai.analyze_job(job_url)

# Generate CV tailoring
cv_outline = await ai.generate_cv_outline(job_description)

# Rate job relevance
score = await ai.rate_job_relevance(job_details)
```

**Features**:
- Automatic fallback to Groq if Gemini fails
- Rate limit handling
- Caching of results
- Streaming responses

---

### core/db_client.py - RealityShapingDB
**Purpose**: Database abstraction (Supabase + SQLite)  
**Main Class**: `RealityShapingDB`  
**Dual Mode**: Cloud primary, local fallback

```python
from core.db_client import RealityShapingDB

db = RealityShapingDB()

# CRUD operations
await db.create_lead(lead_data)
lead = await db.get_lead(lead_id)
await db.update_lead(lead_id, updates)

# Leadership election
is_leader = await db.become_leader()

# Duplicate detection
is_duplicate = await db.is_duplicate(email)
```

**Features**:
- SQLite fallback automatic
- Leadership election for multi-instance
- Heartbeat mechanism
- Duplicate detection

---

### core/smtp_engine.py - Email Delivery
**Purpose**: Send emails with dual provider  
**Main Class**: `SMTPEngine`  
**Providers**: Gmail API + Brevo SMTP

```python
from core.smtp_engine import SMTPEngine

email_engine = SMTPEngine()

# Send application
await email_engine.send_strike(
    recipient="hiring@company.com",
    subject="Software Engineer Application",
    body_html=html_content,
    attachment_path="cv.pdf"
)
```

**Features**:
- Automatic fallback (Gmail → Brevo)
- Rate limiting
- Retry logic
- Delivery tracking

---

### core/pdf_generator.py - PDF Generation
**Purpose**: Generate personalized CVs  
**Main Class**: `PDFGenerator`  
**Library**: FPDF2

```python
from core.pdf_generator import PDFGenerator

pdf_gen = PDFGenerator()

pdf_path = await pdf_gen.create_personalized_pdf(
    cv_data=cv_dict,
    job_description=job_desc,
    output_path="cv_personalized.pdf"
)
```

**Features**:
- Dynamic font selection
- Polymorphic customization
- Fast generation
- FPDF2 backed

---

## Adding Features

### Feature 1: Add a New Telegram Command

**Step 1**: Open `core/telegram_dashboard.py`

**Step 2**: Find the command handler section (around line 500+)

**Step 3**: Add your command handler:
```python
async def cmd_my_command(self, update, context):
    """Handle /my_command"""
    user_id = update.effective_user.id
    args = context.args  # Command arguments
    
    # Your logic here
    result = await self.perform_operation()
    
    # Send response
    await update.message.reply_text(result)
```

**Step 4**: Register in the dispatcher:
```python
# In __init__ method, add:
self.application.add_handler(
    CommandHandler("my_command", self.cmd_my_command)
)
```

**Step 5**: Add to /menu command:
```python
# In cmd_menu(), add:
commands.append("my_command - Description")
```

**Step 6**: Test locally:
```bash
python run.py
# Send /my_command to bot
```

---

### Feature 2: Add a New Lead Source (Scraper)

**Step 1**: Create new scraper file in `core/scrapers/`:
```python
# core/scrapers/my_scraper.py
import asyncio
from typing import List, Dict

class MySourceScraper:
    async def scrape(self, keywords: str) -> List[Dict]:
        """Scrape jobs from my source"""
        leads = []
        
        # Your scraping logic
        leads.append({
            "job_title": "...",
            "company": "...",
            "location": "...",
            "job_url": "...",
            "description": "...",
        })
        
        return leads
```

**Step 2**: Add to lead discovery in `core/lead_processor.py`:
```python
from core.scrapers.my_scraper import MySourceScraper

# In discover_leads():
my_scraper = MySourceScraper()
new_leads = await my_scraper.scrape(keywords)
all_leads.extend(new_leads)
```

**Step 3**: Add to tests:
```python
# tests/test_my_scraper.py
import pytest
from core.scrapers.my_scraper import MySourceScraper

@pytest.mark.asyncio
async def test_my_scraper():
    scraper = MySourceScraper()
    leads = await scraper.scrape("Python Engineer")
    assert len(leads) > 0
    assert "job_title" in leads[0]
```

---

### Feature 3: Add a New Database Table

**Step 1**: Define your table structure in `core/db_client.py`:
```python
# In RealityShapingDB class, add migration:
async def migrate_my_table(self):
    """Create my_table if not exists"""
    if self.using_sqlite:
        # SQLite migration
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS my_table (
                id TEXT PRIMARY KEY,
                field1 TEXT,
                field2 INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        # Supabase: Create manually via dashboard
        pass
```

**Step 2**: Add CRUD methods:
```python
async def create_my_record(self, data: Dict) -> str:
    """Create record"""
    record_id = str(uuid4())
    await self.connection.execute(
        "INSERT INTO my_table (id, field1, field2) VALUES (?, ?, ?)",
        [record_id, data.get("field1"), data.get("field2")]
    )
    return record_id

async def get_my_record(self, record_id: str) -> Dict:
    """Get record"""
    cursor = await self.connection.execute(
        "SELECT * FROM my_table WHERE id = ?",
        [record_id]
    )
    return await cursor.fetchone()
```

---

## Testing Guidelines

### Unit Test Template
```python
# tests/test_my_module.py
import pytest
from core.my_module import MyClass

class TestMyClass:
    @pytest.fixture
    def instance(self):
        """Create test instance"""
        return MyClass()
    
    def test_initialization(self, instance):
        """Test class initialization"""
        assert instance is not None
    
    @pytest.mark.asyncio
    async def test_async_method(self, instance):
        """Test async method"""
        result = await instance.my_async_method()
        assert result is not None
    
    def test_error_handling(self, instance):
        """Test error handling"""
        with pytest.raises(ValueError):
            instance.invalid_operation()
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test
python -m pytest tests/test_my_module.py::TestMyClass::test_method

# Run with coverage
python -m pytest --cov=core --cov-report=html

# Run async tests
python -m pytest -m asyncio
```

---

## Code Standards

### Python Style Guide
- Follow **PEP 8**
- Max line length: **100 characters**
- Use **type hints** for functions
- Use **docstrings** for modules, classes, functions

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `AlphaOrchestrator`)
- **Functions/Methods**: `snake_case` (e.g., `execute_divine_loop`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Async Functions**: Prefix with `async` keyword

### Example Code
```python
from typing import Dict, List, Optional

class JobAnalyzer:
    """Analyze job opportunities using AI."""
    
    def __init__(self, max_retries: int = 3):
        """Initialize analyzer.
        
        Args:
            max_retries: Maximum retry attempts
        """
        self.max_retries = max_retries
    
    async def analyze_job(self, job_url: str) -> Optional[Dict]:
        """Analyze a job opportunity.
        
        Args:
            job_url: URL to job posting
            
        Returns:
            Analysis dict or None if analysis fails
            
        Raises:
            ValueError: If URL is invalid
        """
        if not job_url.startswith("http"):
            raise ValueError(f"Invalid URL: {job_url}")
        
        for attempt in range(self.max_retries):
            try:
                # Your logic here
                return {"score": 95, "relevance": "high"}
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Common Tasks

### Task 1: Add a New Configuration Parameter

**File**: `core/utils/config.py`

```python
# Add to configuration class
class Config:
    # ... existing config ...
    
    MY_NEW_PARAM: str = os.getenv(
        "MY_NEW_PARAM",
        default="default_value"
    )
```

**File**: `.env.example`
```
MY_NEW_PARAM=default_value
```

---

### Task 2: Add Logging to a Module

```python
import logging

logger = logging.getLogger(__name__)

async def my_function():
    logger.info("Starting operation")
    try:
        result = await do_something()
        logger.info(f"Success: {result}")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise
```

---

### Task 3: Handle Async Errors

```python
import asyncio

async def safe_operation():
    try:
        result = await risky_operation()
    except asyncio.TimeoutError:
        logger.warning("Operation timed out")
        # Fallback logic
    except Exception as e:
        logger.error(f"Error: {e}")
        # Error recovery
```

---

## Debugging

### Enable Debug Logging
```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Then run
python run.py
```

### Debug Telegram Bot
```python
# In core/telegram_dashboard.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug Database
```python
# In core/db_client.py, add:
logger.debug(f"Executing: {query}")
logger.debug(f"Parameters: {params}")
```

### Debug Async Issues
```python
import asyncio

# Enable debug mode
asyncio.run(main(), debug=True)
```

### Common Debug Commands
```bash
# Check Python version
python --version

# Check imports
python -c "from core.main_bot import AlphaOrchestrator; print('OK')"

# Compile check
python -m py_compile core/*.py

# Check environment
python -c "import os; print(os.getenv('TELEGRAM_BOT_TOKEN'))"
```

---

## Best Practices

### 1. Always Use Async
```python
# ❌ Bad
def my_function():
    return get_data()

# ✅ Good
async def my_function():
    return await get_data()
```

### 2. Use Type Hints
```python
# ❌ Bad
def process(data):
    return data

# ✅ Good
def process(data: Dict[str, Any]) -> Dict[str, Any]:
    return data
```

### 3. Handle Errors Gracefully
```python
# ❌ Bad
result = await api_call()  # May fail silently

# ✅ Good
try:
    result = await api_call()
except Exception as e:
    logger.error(f"API call failed: {e}")
    result = fallback_data()
```

### 4. Use Context Managers
```python
# ✅ Good
async with database.transaction():
    await database.create_record(data)
    await database.update_record(id, updates)
```

### 5. Write Tests First (TDD)
```python
# 1. Write test
def test_my_function():
    assert my_function() == expected_result

# 2. Write minimal implementation
def my_function():
    return expected_result

# 3. Refactor
```

---

## Deployment After Changes

### Local Testing
```bash
# 1. Test locally
python run.py

# 2. Test with Telegram
# Send /status to bot

# 3. Run tests
python -m pytest

# 4. Check coverage
python -m coverage report --fail-under=70
```

### Push to GitHub
```bash
git add .
git commit -m "feature: Add my new feature"
git push origin main
```

### Monitor Deployment
```bash
# GitHub Actions will auto-test and deploy to Render.com
# Check: https://github.com/Sam-Cordahi/Sam_Job_Automator/actions

# If deployed to Render, test:
# Send /status to bot on Render service
```

---

## Getting Help

- **Code Issues**: Check [GitHub Issues](https://github.com/Sam-Cordahi/Sam_Job_Automator/issues)
- **Documentation**: See [COMPLETE_AUDIT_A_TO_Z.md](COMPLETE_AUDIT_A_TO_Z.md)
- **Configuration**: See [DEPLOYMENT_SECRETS_GUIDE.md](DEPLOYMENT_SECRETS_GUIDE.md)
- **Monitoring**: See [MONITORING_AND_OPERATIONS.md](MONITORING_AND_OPERATIONS.md)

---

**Happy Coding! 🚀**
