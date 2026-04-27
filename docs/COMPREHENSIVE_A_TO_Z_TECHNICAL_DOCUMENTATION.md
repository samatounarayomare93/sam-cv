# Project Chronos - Comprehensive A-to-Z Technical Documentation

## 1. Scope and Method

This document is a full technical analysis of the current workspace state at the time of inspection.

What was analyzed:
- Runtime entry points and process startup paths.
- Core orchestration flow and module interactions.
- Data persistence and cache assets.
- Configuration and environment variable behavior.
- CI/CD workflows and release packaging logic.
- UI layer and integration status.
- Testing footprint and coverage reality.
- Unused or orphaned code with confidence levels and evidence.

How findings were validated:
- Direct source inspection of Python modules, workflow YAML files, and UI files.
- Usage scans for imports/call sites.
- Folder-level verification for active vs archive content.

---

## 2. System Purpose and High-Level Architecture

Project Chronos is a job automation platform centered on two active runtime processes:
- Intelligence/automation process: lead collection, AI filtering, CV tailoring, PDF generation, and email dispatch.
- Control process: Telegram command-and-control dashboard for remote operations.

### Runtime architecture (current)

~~~text
run.py (supervisor)
  -> python -m core.main_bot
  -> python -m core.telegram_dashboard

core.main_bot
  -> core.db_client (state + persistence)
  -> core.ai_agent (job relevance + generation)
  -> core.scrapers.* (lead discovery)
  -> core.follow_up_engine (follow-up actions)
  -> core.smtp_engine (mail delivery)
  -> core.pdf_generator + core.cv_tailor (documents)

core.telegram_dashboard
  -> Telegram polling
  -> leadership/coordination via db_client
  -> operational commands (ignite/kill/status/etc.)
~~~

---

## 3. True Entry Points and Startup Paths

### 3.1 Primary supervisor
- File: run.py
- Role: starts and monitors two subprocesses.
- Behavior:
  - Starts core.main_bot and core.telegram_dashboard.
  - Monitors both processes in a loop.
  - If one exits, restarts that process.
  - On keyboard interrupt, terminates both.
- Important state:
  - NODE_NAME from env or hostname.
  - Logs to logs/orchestrator.log.

### 3.2 Automation engine
- File: core/main_bot.py
- Entry: if __name__ == "__main__".
- Role: contains a full orchestrator implementation (AlphaOrchestrator) and async cycle logic.
- Notes:
  - This module still includes local classes that overlap with runtime_helpers and orchestrator abstractions.

### 3.3 Telegram dashboard
- File: core/telegram_dashboard.py
- Entry: if __name__ == "__main__" then SovereignDashboard().ignite().
- Role: Telegram UI control plane for operations.
- Features:
  - Command handlers.
  - Text-button mapping via handle_text_oracle.
  - Leadership election checks through db layer.
  - keep_alive web endpoint activation.

### 3.4 Standalone scripts
- scripts/deploy_un_killable_cv.py is an independent execution script.

### 3.5 GitHub Actions startup paths
- .github/workflows/job_bot.yml
  - Scheduled and manual run.
  - Executes python core/main_bot.py.
- .github/workflows/24_7_telegram_bot.yml
  - Scheduled and manual run.
  - Executes python launch_sam.py.
  - Important mismatch: launch_sam.py does not exist in current root.

---

## 4. Runtime Control Flow (End-to-End)

This section describes the active processing lifecycle from startup to lead submission.

### 4.1 Supervisor lifecycle (run.py)
1. Initialize logging and verify core folder exists.
2. Start intelligence process.
3. Start Telegram dashboard process.
4. Every 10 seconds:
  - If intelligence process died, restart it.
  - If dashboard process died, restart it.
5. Stop both on interrupt.

### 4.2 Orchestration lifecycle (core/orchestrator.py + scheduler.py)
1. AlphaOrchestrator.validate_preflight computes readiness:
  - telemetry_enabled
  - db_available
  - brevo_ready
  - gmail_ready
  - outlook_ready
  - scraper_available
  - at_least_one_mailer
  - ready
2. Scheduler.run:
  - Logs preflight report.
  - Exits if not ready.
  - Sends startup telemetry broadcast.
  - Loop:
    - Reset cycle stats.
    - Check kill switch callback.
    - Process due follow-ups.
    - Collect and normalize leads.
    - Process up to first 15 leads concurrently.
    - Log cycle report.
    - Sleep using jitter.

### 4.3 Lead processing lifecycle (core/lead_processor.py)
For each lead:
1. Normalize schema via normalize_lead.
2. Build identifier from url or email.
3. Duplicate gate through db.is_duplicate.
4. If description missing and callback available, scrape description.
5. AI analysis via ai.analyze_job.
6. Reject if not relevant or score < 75.
7. Optional email reconnaissance when score >= 90 and omni_crawler exists.
8. Build tailored CV HTML via get_tailored_cv_path.
9. Generate PDF via create_personalized_pdf.
10. Send via send_strike.
11. On success, log application in DB.

### 4.4 Follow-up lifecycle (core/follow_up_engine.py)
1. Query due applications (older window).
2. Generate nudge body.
3. Execute follow-up send path.

---

## 5. Module-by-Module Breakdown

## 5.1 core/config.py
Purpose:
- Centralized env loading and default constants.

Key function:
- _env_flag(name, default): converts env string to boolean.

Key variable groups:
- Kill switch: KILL_SWITCH, KILL_SWITCH_ACTIVE.
- DB: SUPABASE_URL, SUPABASE_KEY.
- SMTP providers: Brevo/Gmail/Outlook credentials and host/port.
- AI: GEMINI_API_KEY, GROQ_API_KEY, USE_AI_ANALYSIS.
- Telegram: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USE_TELEGRAM.
- Safe fallback: OFFLINE_SAFE_MODE, ENABLE_LOCAL_FALLBACKS.
- Runtime thresholds: scraper pages, concurrency, delays, salary thresholds.

Important defaults:
- TEST_MODE defaults to true.
- TEST_RECEIVER_EMAIL defaults to sam.dev1@hotmail.com.

## 5.2 core/db_client.py
Purpose:
- Singleton DB abstraction using Supabase REST when configured and local SQLite mirror always initialized.

Key responsibilities:
- Node identity and registration.
- Heartbeat and leader election.
- Duplicate checks and application logging.
- Settings/state storage.
- Blacklist and recon caches.
- Task queue and telemetry log streaming.

Core internal state:
- enabled (Supabase active or not).
- local_db path (sam_ultimate.db).
- _session reusable async HTTP session.
- _request_semaphore for concurrency control.
- node_id and node_name.

Important behavior:
- If SUPABASE_URL/KEY are missing or placeholder-like, enabled=false and SQLite mode is used.

## 5.3 core/ai_agent.py
Purpose:
- AI relevance and content generation layer.

Key responsibilities:
- Analyze jobs and produce structured outputs.
- Extract JSON robustly from model text.
- Load CV context.
- Select persona/variant strategy.

Expected output tuple (from usage):
- is_relevant, reason, cover_letter, salary, score, advantage, keywords, persona, psych_variant.

## 5.4 core/scrape_service.py
Purpose:
- Async-safe scraping coordinator around legacy and omni scrapers.

Key methods:
- is_available
- stealth_scrape_target
- collect_leads
- close

Behavior highlights:
- Uses EvasionRouter headers/proxy hints.
- Retry on timeout and transient response classes.
- Collects from legacy scraper.get_latest_jobs and omni crawler if provided.

## 5.5 core/scrapers/scraper.py
Purpose:
- Large legacy scraper source pack for multi-site job collection.

Characteristics:
- Many site-specific scrape functions.
- Helper functions for deep-dive counters, page fetch, extraction.
- get_latest_jobs acts as top aggregation path.

## 5.6 core/scrapers/omni_crawler.py
Purpose:
- Enhanced crawling/recon layer.

Main classes:
- PatternRecon
- MarketOracle
- OmniCrawler

Likely responsibilities:
- Discovery/recon over broader signals.
- Email-pattern or target expansion support.

## 5.7 core/lead_schema.py
Purpose:
- normalize_lead unifies source records into common keys.

## 5.8 core/lead_processor.py
Purpose:
- Converts normalized leads into sendable actions with AI gate and persistence.

State:
- cycle_stats dictionary tracking raw/processed/duplicate/rejected/sent/failed.

## 5.9 core/cv_tailor.py
Purpose:
- Tailor CV artifact with role-specific enhancements/keywords and write output file path.

Main entry:
- get_tailored_cv_path(...)

## 5.10 core/pdf_generator.py
Purpose:
- Build PDF assets for applications.

Notable symbols:
- CoverLetterPDF
- SovereignCVPDF
- create_personalized_pdf
- generate_dual_package and additional package helper functions

## 5.11 core/smtp_engine.py
Purpose:
- Multi-provider email send pipeline.

Key flows:
- Provider detection.
- SMTP send fallback routing.
- Optional Gmail API send path.
- Optional Brevo HTTP fallback path.

Critical methods:
- send_strike
- send_email
- send_email_via_gmail_api
- send_email_via_brevo_http
- test_email_connection

## 5.12 core/follow_up_engine.py
Purpose:
- due follow-up retrieval + second-strike execution.

## 5.13 core/runtime_helpers.py
Purpose:
- Shared helpers used by orchestrator/scrape layer.

Exports:
- TelegramNotifier
- HumanParityJitter
- EvasionRouter
- ProxyMesh

Note:
- Similar classes also exist in core/main_bot.py, creating duplication.

## 5.14 core/orchestrator.py and core/scheduler.py
Purpose:
- Smaller clean orchestration abstraction currently present alongside heavier logic in core/main_bot.py.

Note:
- Coexistence of both orchestration models is a maintainability concern.

## 5.15 core/telegram_dashboard.py
Purpose:
- Remote C2 operations via Telegram bot.

Authentication:
- Authorizes only TELEGRAM_CHAT_ID value.

Important handlers:
- handle_command: slash command routing.
- _dispatch_command: command implementation.
- handle_text_oracle: text/button mapping and AI fallback.

Command groups include:
- lifecycle: ignite, kill, resume, pause, reboot.
- execution: launch_single, launch_infinite/hunter.
- diagnostics: status, stats, queue, supabase, audit.
- maintenance: repair/lazarus, hygiene, purge_db.

Leadership model:
- claim_bot_leadership checks and standby behavior for competing pollers.

## 5.16 core/watchdog.py
Purpose:
- Separate process watchdog capable of relaunching core.main_bot.

---

## 6. Data Layer and Persistence Assets

### 6.1 Primary persistence
- Supabase REST (when configured).

### 6.2 Local fallback persistence
- SQLite file: sam_ultimate.db.
- Initialized tables include applications/tasks/recon/blacklist/settings-style data structures.

### 6.3 File-based caches and artifacts
Main storage directories:
- cache/
- logs/
- pdfs/
- core/temp_cvs/
- pdf_cache/

Used for:
- application tracking JSON files.
- cached discovered company/email material.
- generated PDF/CV artifacts.
- operational logs.

---

## 7. UI Layer (Web)

### 7.1 UI runtime package
- Path: ui/
- Framework: Next.js app router style structure.

Current files with active components:
- ui/src/app/layout.js
- ui/src/app/page.js

### 7.2 ui/src/app/layout.js
- Defines RootLayout.
- Applies Geist and Geist_Mono font variables.
- Sets default metadata title/description from template defaults.

### 7.3 ui/src/app/page.js
- Exports CommandCenter component.
- Uses local state for:
  - language switch (en/ar)
  - active tab
  - synthetic metric counters
- Uses interval in useEffect to mutate demo metrics periodically.
- Renders static action controls and telemetry placeholder visuals.

### 7.4 Integration status
- No active invocation of Next.js UI from run.py or Python runtime.
- No workflow step builds or deploys ui/.
- Current UI appears as standalone frontend prototype, not wired to backend APIs.

---

## 8. Configuration and Environment Matrix

### 8.1 Source precedence
1. Environment variables from .env (via load_dotenv).
2. Default constants in core/config.py.
3. Workflow-level injected environment in GitHub Actions.

### 8.2 Feature gates and runtime modes
- OFFLINE_SAFE_MODE becomes true when all key external credentials are absent.
- USE_AI_ANALYSIS depends on both env flag and presence of AI keys.
- TEST_MODE defaults true and can reroute/testing behavior.
- KILL_SWITCH_ACTIVE can halt processing loop.

### 8.3 Notable operational variables
- DB: SUPABASE_URL, SUPABASE_KEY
- AI: GEMINI_API_KEY, GROQ_API_KEY
- Telegram: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
- SMTP: BREVO_SMTP_PASSWORD, GMAIL_SMTP_USER, GMAIL_APP_PASSWORD, OUTLOOK_USER, OUTLOOK_PASSWORD
- runtime limits: MAX_PARALLEL_STRIKES, REQUEST_TIMEOUT, MAX_QUALIFIED_LEADS_PER_CYCLE

---

## 9. CI/CD and Automation Workflows

## 9.1 job_bot.yml
- Schedule and manual trigger.
- Installs dependencies.
- Validates basic config.
- Runs python core/main_bot.py.

## 9.2 24_7_telegram_bot.yml
- Schedule and manual trigger.
- Concurrency group prevents overlapping dashboard jobs.
- Runs python launch_sam.py.
- Current issue: launch_sam.py is not present in current root workspace.

## 9.3 ci_quality.yml
- Runs compile smoke test and unittest discovery with coverage report.
- Current issue: compile step references root files that are absent in current workspace:
  - launch_sam.py
  - main_bot.py
  - launch_main_bot.py
  - data_validator.py
  - database.py

## 9.4 pre_launch_test.yml
- Manual preflight run.
- Syntax smoke check against core modules.
- Unit discovery and optional email test conditions.

## 9.5 release.yml
- Triggered by version tags.
- Builds zip archive from include list.
- Current issue: includes multiple root files/docs that may not exist in this workspace snapshot.

---

## 10. Testing Reality and Validation Surface

Observed test landscape:
- tests/ contains verify_mappings.py only.
- legacy_archive/ contains multiple test_*.py files, not in active tests folder.

Implications:
- unittest discover can run with limited or no effective assertion coverage depending on discovery path and naming.
- CI quality gate may appear configured but does not currently guarantee strong regression protection for core runtime.

verify_mappings.py behavior:
- Async command mapping smoke-style validation for Telegram text handlers using MagicMock.
- Primarily checks non-crash behavior for mapped commands.

---

## 11. Unused / Orphaned Code

This section explicitly flags code not used by active execution paths, with confidence levels.

### 11.1 Definitely orphaned (high confidence)

1) legacy_archive/ as active runtime source
- Confidence: high
- Evidence:
  - Active runtime entry is run.py -> core.* modules.
  - Workflows execute core/main_bot.py and (intended) launch_sam.py, not legacy_archive paths.
  - Files in legacy_archive are not imported by active core runtime.

2) Legacy launcher variants in legacy_archive
- Examples:
  - legacy_archive/SAM_PORTABLE.py
  - legacy_archive/SAM_ISOLATED.py
  - legacy_archive/SAM_EMBEDDED.py
  - legacy_archive/SAM_FINAL_LAUNCHER.py
- Confidence: high
- Evidence: no inbound runtime call/import in active startup path.

3) Legacy test files in legacy_archive/test_*.py as active CI suite
- Confidence: high
- Evidence:
  - Not located under tests/ where current test inventory is minimal.
  - Not part of active runtime imports.

4) Verification scripts in legacy_archive/verify_*.py
- Confidence: high
- Evidence: standalone scripts with no inbound runtime integration.

### 11.2 Likely orphaned (medium-high confidence)

1) UI as integrated production surface
- Path: ui/
- Confidence: medium-high
- Evidence:
  - No process in run.py starts Next.js.
  - No workflow builds/deploys ui/.
  - UI components currently show local simulated metrics and placeholders.

2) src/ tree as active code
- Path: src/
- Confidence: high
- Evidence:
  - src/core and src/ui are empty in current workspace snapshot.

3) InterviewPrepEngine practical runtime usage
- Path: core/interview_prep.py
- Confidence: medium
- Evidence:
  - Imported in core/main_bot.py.
  - No clear active call chain observed in scheduler/lead processor flow.
  - Could still be used via dashboard prep command path indirectly through AI prompting, not direct engine usage.

### 11.3 Intra-module dead/duplicate patterns (likely)

1) Duplicate helper classes across modules
- EvasionRouter, HumanParityJitter, ProxyMesh exist in both:
  - core/main_bot.py
  - core/runtime_helpers.py
- Confidence: high
- Impact:
  - behavior divergence risk
  - maintenance overhead

2) Orchestration model duplication
- Full AlphaOrchestrator in core/main_bot.py and another orchestrator abstraction in core/orchestrator.py.
- Confidence: high
- Impact: architectural ambiguity and drift.

---

## 12. Technical Risks and Architecture Debt

1) Workflow-to-repo mismatch
- Severity: high
- Details:
  - CI and dashboard workflows reference root files missing in this snapshot.
  - Can cause failed pipelines or non-starting automation jobs.

2) Multiple orchestration implementations
- Severity: medium-high
- Details:
  - core/main_bot.py and core/orchestrator.py overlap responsibilities.

3) Duplicate helper abstractions
- Severity: medium
- Details:
  - same helper concepts implemented in multiple modules.

4) Limited active test coverage footprint
- Severity: medium-high
- Details:
  - tests/ contains only one verification script.
  - core pathways are insufficiently asserted.

5) Default TEST_MODE true + hardcoded test receiver fallback
- Severity: medium
- Details:
  - operational confusion risk if production env is not explicit.

6) Leadership election race potential
- Severity: medium
- Details:
  - node leadership in DB settings can be contention-prone without strict transactional guardrails.

---

## 13. A-to-Z Interaction Map (Condensed)

A) process starts via run.py.
B) run.py launches core.main_bot and core.telegram_dashboard.
C) orchestrator/scheduler validates preflight.
D) scrape layer gathers leads.
E) schema normalization standardizes records.
F) lead processor applies duplicate gate.
G) AI relevance scoring and generation runs.
H) CV tailor writes targeted artifact.
I) PDF generator builds attachable document.
J) SMTP engine sends through available provider chain.
K) DB logs application and telemetry.
L) follow-up engine executes second-touch actions.
M) dashboard commands can alter runtime state (kill/resume/reboot/etc.).
N) workflows provide scheduled cloud execution and release packaging, but contain stale references that need alignment with current file layout.

---

## 14. Recommended Refactor Plan

1) Resolve workflow/file mismatches first
- Update job_bot/24_7_telegram_bot/ci_quality/release to only reference existing paths.

2) Pick one orchestration path
- Either main_bot-centered or orchestrator+scheduler-centered runtime.
- Remove or archive duplicate execution logic.

3) De-duplicate helper classes
- Keep single source in runtime_helpers and import everywhere.

4) Strengthen tests
- Move/port meaningful tests from legacy_archive into tests/.
- Add assertions for lead_processor, db_client, ai_agent, smtp_engine.

5) Clarify UI strategy
- Either integrate UI with API endpoints and deployment pipeline, or mark as standalone prototype.

6) Harden config safety
- Set TEST_MODE default false for production profiles.
- Require explicit TEST_RECEIVER_EMAIL in test-only contexts.

---

## 15. Glossary of Core State Variables

Common runtime state variables (high impact):
- is_running: controls main loop continuity.
- cycle_stats: per-cycle metrics in lead processing.
- enabled (db client): toggles Supabase vs SQLite mode.
- _session handles: persistent HTTP sessions for performance.
- semaphore and _request_semaphore: concurrency controls.
- KILL_SWITCH_ACTIVE: emergency stop gate.
- TEST_MODE: test-routing behavior gate.

---

## 16. Conclusion

The current codebase contains a capable core runtime in core/* with clear scraping -> AI -> document -> email -> logging flow, plus a functional Telegram control plane. The largest present issue is not missing functionality, but architectural and operational drift:
- stale workflow references,
- duplicated orchestration/helper implementations,
- and limited active tests in the current non-archive test tree.

The fastest path to stability is to align workflows with existing files, consolidate duplicate runtime paths, and restore real test coverage for core execution-critical modules.
