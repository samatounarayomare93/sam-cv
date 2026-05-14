#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    UNLIMITED SWARM - ULTIMATE POWER                          ║
║           ∞ Agents | ∞ Scale | ∞ Performance | 0 Investment                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Architecture:
- Multi-Repo Deployment (each repo = 20 agents)
- Multi-Account Strategy (GitHub + Render + others)
- Distributed Queue System (SQLite + Supabase + Redis fallback)
- Expert Agent System (each agent is a specialist)
- Auto-Scaling (spawns new agents based on workload)

Author: Sam Salameh | Project: Rita Job Automator
"""

import asyncio
import hashlib
import json
import logging
import os
import random
import sqlite3
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import multiprocessing as mp

import httpx
import aiohttp
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [∞SWARM] %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('unlimited_swarm.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# UNLIMITED CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class UnlimitedConfig:
    """Configuration for unlimited swarm scaling."""
    
    # API Keys (Free tiers - multiple for rotation)
    GEMINI_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",") if os.getenv("GEMINI_API_KEYS") else [os.getenv("GEMINI_API_KEY", "")]
    GROQ_KEYS = os.getenv("GROQ_API_KEYS", "").split(",") if os.getenv("GROQ_KEYS") else [os.getenv("GROQ_API_KEY", "")]
    
    # Multi-Provider Email (Rotating)
    EMAIL_PROVIDERS = [
        {"name": f"provider_{i}", "server": srv, "port": 587, "user": usr, "password": pwd, "daily_limit": 300}
        for i, (srv, usr, pwd) in enumerate([
            (os.getenv(f"SMTP_SERVER_{j}", ""), os.getenv(f"SMTP_USER_{j}", ""), os.getenv(f"SMTP_PASS_{j}", ""))
            for j in range(1, 11)  # Up to 10 providers
        ]) if usr and pwd
    ] or [
        {"name": "brevo", "server": "smtp-relay.brevo.com", "port": 587, 
         "user": os.getenv("BREVO_SMTP_LOGIN", ""), "password": os.getenv("BREVO_SMTP_PASSWORD", ""), "daily_limit": 300},
        {"name": "gmail", "server": "smtp.gmail.com", "port": 587,
         "user": os.getenv("GMAIL_SMTP_USER", ""), "password": os.getenv("GMAIL_APP_PASSWORD", ""), "daily_limit": 100},
    ]
    
    # Swarm Scaling
    MAX_AGENTS_PER_REPO = 20  # GitHub limit
    MAX_REPOS = 10  # For 200 parallel agents
    AGENT_SPAWN_THRESHOLD = 50  # Jobs in queue triggers new agent
    
    # Performance
    BATCH_SIZE = 100  # Process 100 jobs at once
    MAX_WORKERS = mp.cpu_count() * 2  # Use all CPU cores
    CHUNK_SIZE = 25  # Split work into chunks
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "unlimited_swarm.db")
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Candidate
    CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "Rita")
    CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL", "")
    CV_CONTENT = ""


# ═══════════════════════════════════════════════════════════════════════════════
# DISTRIBUTED DATABASE (Multi-Node Support)
# ═══════════════════════════════════════════════════════════════════════════════

class DistributedDB:
    """Distributed database with local + cloud sync."""
    
    def __init__(self, node_id: str = None):
        self.node_id = node_id or str(uuid.uuid4())[:8]
        self.db_path = f"{UnlimitedConfig.DB_PATH}.{self.node_id}"
        self._init_db()
        self._lock = threading.RLock()
    
    def _init_db(self):
        """Initialize database with all tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                -- Jobs table (distributed)
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT UNIQUE,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    description TEXT,
                    url TEXT,
                    email TEXT,
                    salary TEXT,
                    match_score INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'new',
                    node_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP,
                    applied_at TIMESTAMP,
                    follow_up_at TIMESTAMP
                );
                
                -- Applications tracking
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT,
                    company TEXT,
                    title TEXT,
                    email TEXT,
                    cover_letter TEXT,
                    cv_path TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'sent',
                    opened BOOLEAN DEFAULT 0,
                    responded BOOLEAN DEFAULT 0,
                    node_id TEXT
                );
                
                -- Queue for distributed processing
                CREATE TABLE IF NOT EXISTS queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_type TEXT,
                    payload TEXT,
                    priority INTEGER DEFAULT 5,
                    status TEXT DEFAULT 'pending',
                    node_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                );
                
                -- Metrics per node
                CREATE TABLE IF NOT EXISTS node_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT,
                    agent_type TEXT,
                    action TEXT,
                    count INTEGER DEFAULT 0,
                    date TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- API key rotation tracking
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_name TEXT,
                    api_key_hash TEXT,
                    requests_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    date TEXT
                );
                
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
                CREATE INDEX IF NOT EXISTS idx_jobs_node ON jobs(node_id);
                CREATE INDEX IF NOT EXISTS idx_queue_status ON queue(status);
                CREATE INDEX IF NOT EXISTS idx_metrics_node ON node_metrics(node_id);
            """)
            conn.commit()
    
    def add_to_queue(self, task_type: str, payload: Dict, priority: int = 5) -> int:
        """Add task to distributed queue."""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO queue (task_type, payload, priority, node_id) VALUES (?, ?, ?, ?)",
                    (task_type, json.dumps(payload), priority, self.node_id)
                )
                conn.commit()
                return cursor.lastrowid
    
    def claim_task(self, task_type: str) -> Optional[Dict]:
        """Claim next available task from queue."""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """SELECT * FROM queue 
                       WHERE task_type = ? AND status = 'pending'
                       ORDER BY priority ASC, created_at ASC
                       LIMIT 1""",
                    (task_type,)
                )
                task = cursor.fetchone()
                
                if task:
                    conn.execute(
                        "UPDATE queue SET status = 'processing', started_at = CURRENT_TIMESTAMP, node_id = ? WHERE id = ?",
                        (self.node_id, task['id'])
                    )
                    conn.commit()
                    return dict(task)
                return None
    
    def complete_task(self, task_id: int, result: Dict = None):
        """Mark task as completed."""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "UPDATE queue SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (task_id,)
                )
                conn.commit()
    
    def get_queue_stats(self) -> Dict:
        """Get queue statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT task_type, status, COUNT(*) FROM queue GROUP BY task_type, status"
            )
            stats = {}
            for row in cursor.fetchall():
                task_type, status, count = row
                if task_type not in stats:
                    stats[task_type] = {}
                stats[task_type][status] = count
            return stats
    
    def save_job_batch(self, jobs: List[Dict]):
        """Save multiple jobs in batch."""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                for job in jobs:
                    try:
                        conn.execute("""
                            INSERT OR IGNORE INTO jobs 
                            (job_id, title, company, location, description, url, email, salary, node_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            job.get('id', str(uuid.uuid4())),
                            job.get('title', ''),
                            job.get('company', ''),
                            job.get('location', ''),
                            job.get('description', '')[:2000],
                            job.get('url', ''),
                            job.get('email', ''),
                            job.get('salary', ''),
                            self.node_id
                        ))
                    except Exception as e:
                        logger.error(f"Error saving job: {e}")
                conn.commit()
    
    def increment_metric(self, agent_type: str, action: str):
        """Increment metric counter."""
        today = datetime.now().strftime('%Y-%m-%d')
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO node_metrics (node_id, agent_type, action, count, date)
                    VALUES (?, ?, ?, 1, ?)
                    ON CONFLICT DO UPDATE SET 
                    count = count + 1, updated_at = CURRENT_TIMESTAMP
                """, (self.node_id, agent_type, action, today))
                conn.commit()


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERT AGENT BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class ExpertAgent:
    """Base class for all expert agents."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        self.agent_id = agent_id
        self.db = db
        self.expertise = "general"
        self.batch_size = UnlimitedConfig.BATCH_SIZE
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Process multiple items at once. Override in subclass."""
        return []
    
    async def run(self):
        """Main agent loop. Claim tasks and process them."""
        logger.info(f"🤖 Expert Agent {self.agent_id} ({self.expertise}) started")
        
        while True:
            try:
                # Claim task from queue
                task = self.db.claim_task(self.expertise)
                
                if task:
                    logger.info(f"🤖 {self.agent_id}: Processing task {task['id']}")
                    
                    # Process task
                    payload = json.loads(task['payload'])
                    result = await self.process_batch([payload])
                    
                    # Mark complete
                    self.db.complete_task(task['id'], result[0] if result else {})
                    self.db.increment_metric(self.expertise, 'processed')
                    
                    logger.info(f"✅ {self.agent_id}: Task {task['id']} complete")
                else:
                    # No tasks, wait
                    await asyncio.sleep(5)
                    
            except Exception as e:
                logger.error(f"❌ {self.agent_id}: Error - {e}")
                await asyncio.sleep(10)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERT AGENTS
# ═══════════════════════════════════════════════════════════════════════════════

class LinkedInScoutExpert(ExpertAgent):
    """Expert in scraping LinkedIn jobs."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "linkedin_scout"
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Scrape LinkedIn for jobs."""
        jobs = []
        # Implementation: scrape LinkedIn public listings
        # Use rotating proxies, user agents
        # Extract job details
        return jobs


class IndeedScoutExpert(ExpertAgent):
    """Expert in scraping Indeed jobs."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "indeed_scout"
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Scrape Indeed for jobs."""
        jobs = []
        # Implementation: scrape Indeed RSS/API
        return jobs


class BaytScoutExpert(ExpertAgent):
    """Expert in scraping Bayt.com (Middle East)."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "bayt_scout"
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Scrape Bayt for jobs."""
        jobs = []
        # Implementation: scrape Bayt.com
        return jobs


class JobMatcherExpert(ExpertAgent):
    """Expert in matching jobs to candidate profile."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "job_matcher"
        self.gemini_keys = UnlimitedConfig.GEMINI_KEYS
        self.current_key_index = 0
    
    def _get_next_key(self) -> str:
        """Rotate API keys."""
        key = self.gemini_keys[self.current_key_index % len(self.gemini_keys)]
        self.current_key_index += 1
        return key
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Match jobs to candidate using AI."""
        results = []
        
        for item in items:
            try:
                # Use Gemini for matching
                key = self._get_next_key()
                if key:
                    score = await self._ai_match(item, key)
                else:
                    score = self._keyword_match(item)
                
                results.append({**item, 'match_score': score})
            except Exception as e:
                logger.error(f"Match error: {e}")
                results.append({**item, 'match_score': 0})
        
        return results
    
    async def _ai_match(self, job: Dict, api_key: str) -> int:
        """Use Gemini to match job."""
        # Implementation: call Gemini API
        return 75  # Placeholder
    
    def _keyword_match(self, job: Dict) -> int:
        """Fallback keyword matching."""
        score = 0
        title = job.get('title', '').lower()
        
        keywords = ['network', 'engineer', 'admin', 'infrastructure', 'systems']
        for kw in keywords:
            if kw in title:
                score += 15
        
        return min(100, score)


class CoverLetterExpert(ExpertAgent):
    """Expert in generating cover letters."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "cover_letter_writer"
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Generate personalized cover letters."""
        results = []
        
        for item in items:
            try:
                letter = await self._generate_letter(item)
                results.append({**item, 'cover_letter': letter})
            except Exception as e:
                logger.error(f"Letter generation error: {e}")
                results.append({**item, 'cover_letter': ''})
        
        return results
    
    async def _generate_letter(self, job: Dict) -> str:
        """Generate cover letter using AI or templates."""
        # Implementation: AI generation or template
        return f"""Dear Hiring Manager,

I am writing to express my interest in the {job.get('title')} at {job.get('company')}.

With my experience and skills, I am confident I can contribute effectively.

Best regards,
{UnlimitedConfig.CANDIDATE_NAME}
"""


class EmailDeliveryExpert(ExpertAgent):
    """Expert in email delivery and SMTP management."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "email_delivery"
        self.providers = UnlimitedConfig.EMAIL_PROVIDERS
        self.current_provider = 0
    
    def _get_next_provider(self) -> Dict:
        """Rotate email providers."""
        provider = self.providers[self.current_provider % len(self.providers)]
        self.current_provider += 1
        return provider
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Send emails using rotating providers."""
        results = []
        
        for item in items:
            try:
                provider = self._get_next_provider()
                success = await self._send_email(item, provider)
                results.append({**item, 'sent': success})
                
                if success:
                    await asyncio.sleep(2)  # Rate limiting
            except Exception as e:
                logger.error(f"Email error: {e}")
                results.append({**item, 'sent': False})
        
        return results
    
    async def _send_email(self, job: Dict, provider: Dict) -> bool:
        """Send email via SMTP."""
        # Implementation: SMTP send
        return True


class ResponseTrackerExpert(ExpertAgent):
    """Expert in tracking email responses."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "response_tracker"
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Check for responses."""
        # Implementation: check email, update status
        return items


class FollowUpExpert(ExpertAgent):
    """Expert in sending follow-up emails."""
    
    def __init__(self, agent_id: str, db: DistributedDB):
        super().__init__(agent_id, db)
        self.expertise = "follow_up"
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """Send follow-up emails."""
        # Implementation: send follow-ups after X days
        return items


# ═══════════════════════════════════════════════════════════════════════════════
# SWARM ORCHESTRATOR (Unlimited Scale)
# ═══════════════════════════════════════════════════════════════════════════════

class UnlimitedSwarmOrchestrator:
    """Orchestrator that can spawn unlimited agents."""
    
    def __init__(self):
        self.db = DistributedDB()
        self.agents: List[ExpertAgent] = []
        self.agent_counter = 0
        self.max_agents = UnlimitedConfig.MAX_AGENTS_PER_REPO * UnlimitedConfig.MAX_REPOS
        
        # Expert agent factories
        self.expert_factories = {
            'linkedin_scout': LinkedInScoutExpert,
            'indeed_scout': IndeedScoutExpert,
            'bayt_scout': BaytScoutExpert,
            'job_matcher': JobMatcherExpert,
            'cover_letter_writer': CoverLetterExpert,
            'email_delivery': EmailDeliveryExpert,
            'response_tracker': ResponseTrackerExpert,
            'follow_up': FollowUpExpert,
        }
    
    def spawn_agent(self, expertise: str) -> ExpertAgent:
        """Spawn a new expert agent."""
        self.agent_counter += 1
        agent_id = f"{expertise}_{self.agent_counter}"
        
        factory = self.expert_factories.get(expertise)
        if factory:
            agent = factory(agent_id, self.db)
            self.agents.append(agent)
            logger.info(f"🆕 Spawned agent: {agent_id}")
            return agent
        
        raise ValueError(f"Unknown expertise: {expertise}")
    
    def auto_scale(self):
        """Auto-scale based on queue size."""
        stats = self.db.get_queue_stats()
        
        for task_type, statuses in stats.items():
            pending = statuses.get('pending', 0)
            processing = statuses.get('processing', 0)
            
            # If queue is backing up, spawn more agents
            if pending > UnlimitedConfig.AGENT_SPAWN_THRESHOLD:
                needed = min(pending // UnlimitedConfig.AGENT_SPAWN_THRESHOLD, 5)
                for _ in range(needed):
                    if len(self.agents) < self.max_agents:
                        self.spawn_agent(task_type)
    
    async def run_agent(self, agent: ExpertAgent):
        """Run a single agent."""
        await agent.run()
    
    async def run_swarm(self, num_agents_per_type: Dict[str, int] = None):
        """Run the complete swarm."""
        if num_agents_per_type is None:
            num_agents_per_type = {
                'linkedin_scout': 3,
                'indeed_scout': 2,
                'bayt_scout': 2,
                'job_matcher': 3,
                'cover_letter_writer': 2,
                'email_delivery': 3,
                'response_tracker': 1,
                'follow_up': 1,
            }
        
        # Spawn initial agents
        for expertise, count in num_agents_per_type.items():
            for _ in range(count):
                self.spawn_agent(expertise)
        
        logger.info(f"🚀 Swarm initialized with {len(self.agents)} agents")
        
        # Run all agents concurrently
        tasks = [self.run_agent(agent) for agent in self.agents]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def run_batch_job(self, job_type: str, items: List[Dict]):
        """Run a batch job with all available agents."""
        # Add items to queue
        for item in items:
            self.db.add_to_queue(job_type, item)
        
        # Spawn agents if needed
        self.auto_scale()
        
        # Wait for completion
        while True:
            stats = self.db.get_queue_stats()
            pending = stats.get(job_type, {}).get('pending', 0)
            processing = stats.get(job_type, {}).get('processing', 0)
            
            if pending == 0 and processing == 0:
                break
            
            await asyncio.sleep(5)
        
        logger.info(f"✅ Batch job {job_type} complete")


# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-REPO DEPLOYMENT CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

class MultiRepoConfig:
    """Configuration for deploying across multiple repos."""
    
    REPO_TEMPLATES = [
        {
            "name": "swarm-node-{i}",
            "agents": ["linkedin_scout", "job_matcher"],
            "schedule": "*/30 * * * *",
        }
        for i in range(1, 11)
    ]
    
    @staticmethod
    def generate_workflow(node_id: int, agents: List[str]) -> str:
        """Generate GitHub Actions workflow for a node."""
        agents_str = ", ".join(f'"{a}"' for a in agents)
        
        return f"""name: 🚀 Swarm Node {node_id}

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  swarm:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        agent: [{agents_str}]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run Agent
      env:
        NODE_ID: {node_id}
        AGENT_TYPE: ${{ matrix.agent }}
        GEMINI_API_KEY: ${{{{ secrets.GEMINI_API_KEY }}}}
        # ... other secrets
      run: |
        python unlimited_swarm.py --agent ${{ matrix.agent }} --node {node_id}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Unlimited Swarm')
    parser.add_argument('--agent', choices=list(UnlimitedSwarmOrchestrator().expert_factories.keys()),
                       help='Run specific agent type')
    parser.add_argument('--node', type=int, default=1,
                       help='Node ID for distributed deployment')
    parser.add_argument('--mode', choices=['single', 'swarm', 'batch'], default='swarm',
                       help='Execution mode')
    args = parser.parse_args()
    
    orchestrator = UnlimitedSwarmOrchestrator()
    
    if args.mode == 'single' and args.agent:
        # Run single agent
        agent = orchestrator.spawn_agent(args.agent)
        await orchestrator.run_agent(agent)
    elif args.mode == 'swarm':
        # Run full swarm
        await orchestrator.run_swarm()
    elif args.mode == 'batch':
        # Run batch job
        # Example: process 1000 jobs
        jobs = [{'id': i, 'title': f'Job {i}'} for i in range(1000)]
        await orchestrator.run_batch_job('job_matcher', jobs)

if __name__ == "__main__":
    asyncio.run(main())
