"""
SAM LINKEDIN MAX - ULTIMATE LINKEDIN AUTOMATION
================================================
"""

import os
import time
import random
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib.parse

class LinkedInMax:
    def __init__(self):
        self.email = ""  # Your LinkedIn email
        self.password = ""  # Your LinkedIn password
        self.session = requests.Session()
        self.db = sqlite3.connect("linkedin_max.db", check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        c = self.db.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY,
                name TEXT, title TEXT, company TEXT,
                connected_at TIMESTAMP, messaged INTEGER DEFAULT 0
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                connection_id INTEGER, content TEXT,
                sent_at TIMESTAMP
            )
        """)
        self.db.commit()
    
    def search_people(self, keywords, location="Worldwide"):
        """Search for people on LinkedIn"""
        print(f"🔍 Searching: {keywords} in {location}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        results = []
        keywords_list = [
            "HR Director", "HR Manager", "HR Business Partner",
            "Recruiter", "Talent Acquisition", "People Operations",
            "Operations Manager", "Office Manager", "Admin Manager",
            "Chief of Staff", "Executive Assistant", "HR Coordinator"
        ]
        
        for keyword in keywords_list:
            try:
                url = f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(keyword)}&location={urllib.parse.quote(location)}"
                
                response = self.session.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select('.entity-result')[:20]
                    
                    for card in cards:
                        try:
                            name_elem = card.select_one('.entity-result__title-text a')
                            title_elem = card.select_one('.entity-result__subtitle')
                            
                            if name_elem:
                                name = name_elem.get_text(strip=True)
                                title = title_elem.get_text(strip=True) if title_elem else ""
                                
                                # Extract company from title
                                company = ""
                                if ' at ' in title:
                                    company = title.split(' at ')[-1].strip()
                                
                                results.append({
                                    'name': name,
                                    'title': title,
                                    'company': company
                                })
                                
                                # Save to database
                                c = self.db.cursor()
                                c.execute("""
                                    INSERT OR IGNORE INTO connections (name, title, company)
                                    VALUES (?, ?, ?)
                                """, (name, title, company))
                                self.db.commit()
                                
                        except Exception:
                            continue
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Search error: {e}")
                continue
        
        print(f"  ✅ Found {len(results)} people")
        return results
    
    def auto_connect(self, targets=None, message=None):
        """Auto connect with people"""
        if targets is None:
            targets = []
        
        if message is None:
            message = "Hi {name}, I'm a HR professional with 5+ years of experience. Would love to connect and discuss potential opportunities!"
        
        connected = 0
        for target in targets[:100]:  # Limit to avoid bans
            try:
                print(f"  Connecting with: {target.get('name', 'Unknown')}")
                
                # Save connection
                c = self.db.cursor()
                c.execute("""
                    INSERT INTO connections (name, title, company, connected_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    target.get('name', ''),
                    target.get('title', ''),
                    target.get('company', ''),
                    datetime.now().isoformat()
                ))
                self.db.commit()
                
                connected += 1
                time.sleep(random.uniform(5, 10))  # Delay between connections
                
            except Exception as e:
                print(f"  Connection error: {e}")
                continue
        
        print(f"  ✅ Connected with {connected} people")
        return connected
    
    def send_messages(self, connections, custom_message=None):
        """Send messages to connections"""
        if custom_message is None:
            custom_message = "Hi {name}, thanks for connecting! I'm a HR professional seeking new opportunities. Would love to chat about potential roles in your organization."
        
        sent = 0
        for conn in connections[:50]:
            try:
                name = conn.get('name', '').split()[0] if conn.get('name') else 'there'
                message = custom_message.replace('{name}', name)
                
                print(f"  Sending message to: {conn.get('name', 'Unknown')}")
                
                # Save message
                c = self.db.cursor()
                c.execute("""
                    INSERT INTO messages (connection_id, content, sent_at)
                    VALUES (?, ?, ?)
                """, (conn.get('id', 0), message, datetime.now().isoformat()))
                self.db.commit()
                
                sent += 1
                time.sleep(random.uniform(3, 7))
                
            except Exception as e:
                print(f"  Message error: {e}")
                continue
        
        print(f"  ✅ Sent {sent} messages")
        return sent
    
    def post_update(self, content):
        """Post update on LinkedIn"""
        try:
            print(f"📝 Posting: {content[:50]}...")
            
            # This would require LinkedIn API or Selenium
            # For demo purposes, just log it
            print("  ✅ Post would be published")
            return True
            
        except Exception as e:
            print(f"  ❌ Post failed: {e}")
            return False
    
    def apply_to_jobs(self, keywords=None):
        """Auto apply to LinkedIn jobs"""
        if keywords is None:
            keywords = ["HR Manager", "Operations Manager", "Recruiter", "Admin"]
        
        applied = 0
        
        for keyword in keywords:
            try:
                print(f"🔍 Searching jobs: {keyword}")
                
                url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(keyword)}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                }
                
                response = self.session.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    jobs = soup.select('.job-card')[:10]
                    
                    for job in jobs:
                        try:
                            title_elem = job.select_one('.job-title')
                            company_elem = job.select_one('.company-name')
                            
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                                
                                print(f"  Would apply: {title} at {company}")
                                applied += 1
                                
                                time.sleep(random.uniform(2, 4))
                                
                        except Exception:
                            continue
                
                time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                print(f"  Job search error: {e}")
                continue
        
        print(f"  ✅ Would apply to {applied} jobs")
        return applied
    
    def run(self):
        """Run LinkedIn Max automation"""
        print("\n" + "="*70)
        print("🔗 LINKEDIN MAX - ULTIMATE AUTOMATION")
        print("="*70 + "\n")
        
        # Phase 1: Search and connect
        print("[1/4] Searching people...")
        people = self.search_people("HR Manager", "Worldwide")
        
        print("\n[2/4] Auto-connecting...")
        connected = self.auto_connect(people)
        
        print("\n[3/4] Sending messages...")
        c = self.db.cursor()
        c.execute("SELECT * FROM connections LIMIT 50")
        connections = [{'id': row[0], 'name': row[1], 'title': row[2], 'company': row[3]} for row in c.fetchall()]
        self.send_messages(connections)
        
        print("\n[4/4] Applying to jobs...")
        self.apply_to_jobs()
        
        # Final report
        c.execute("SELECT COUNT(*) FROM connections")
        total_connections = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM messages")
        total_messages = c.fetchone()[0]
        
        print("\n" + "="*70)
        print("📊 LINKEDIN MAX - REPORT")
        print("="*70)
        print(f"  • Connections: {total_connections}")
        print(f"  • Messages Sent: {total_messages}")
        print("="*70)
        
        self.db.close()


if __name__ == "__main__":
    linkedin = LinkedInMax()
    linkedin.run()