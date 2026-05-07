"""
SMART LEAD RECYCLER - Resets processed leads back to pending with new job titles
so the bot can apply to same companies for different positions
"""
import asyncio, httpx, os, random
from dotenv import load_dotenv
load_dotenv()

# New job titles to apply for (different from first round)
NEW_JOB_TITLES = [
    "Network Security Engineer",
    "IT Infrastructure Manager", 
    "Senior Systems Administrator",
    "Network Architect",
    "NOC Engineer",
    "Telecom Engineer",
    "IT Operations Manager",
    "Network Consultant",
    "Cisco Network Engineer",
    "Fortinet Security Engineer",
]

async def recycle_and_inject():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    headers = {
        "apikey": key,
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation"
    }
    
    async with httpx.AsyncClient(timeout=20) as c:
        # Get all processed leads
        r = await c.get(
            url + "/rest/v1/leads?status=eq.processed&select=id,company_name,email,job_url&limit=200",
            headers=headers
        )
        processed = r.json() if r.status_code == 200 else []
        print(f"Found {len(processed)} processed leads to recycle")
        
        # Create new leads with different job titles and unique URLs
        new_leads = []
        for lead in processed[:100]:  # Take first 100
            new_title = random.choice(NEW_JOB_TITLES)
            # Create unique URL by adding job title suffix
            base_url = lead.get("job_url", "").rstrip("/")
            new_url = base_url + f"/{new_title.lower().replace(' ', '-')}-2"
            
            new_leads.append({
                "company_name": lead.get("company_name"),
                "email": lead.get("email"),
                "job_title": new_title,
                "job_url": new_url,
                "status": "pending",
                "priority_score": random.randint(75, 92)
            })
        
        # Inject new leads
        success = 0
        fail = 0
        batch_size = 10
        for i in range(0, len(new_leads), batch_size):
            batch = new_leads[i:i+batch_size]
            tasks = [c.post(url + "/rest/v1/leads", json=lead, headers=headers) for lead in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for lead, result in zip(batch, results):
                if isinstance(result, Exception):
                    fail += 1
                elif result.status_code in (200, 201):
                    success += 1
                    print(f"  OK [{lead['priority_score']}] {lead['company_name']} | {lead['job_title']}")
                else:
                    fail += 1
            await asyncio.sleep(0.3)
        
        print(f"\nRecycled: {success} leads | Failed: {fail}")
        
        # Final count
        r2 = await c.get(url + "/rest/v1/leads?status=eq.pending&select=id", headers=headers)
        pending = r2.json() if r2.status_code == 200 else []
        print(f"Total pending in queue: {len(pending)}")
        print("\nBot will process these automatically!")

asyncio.run(recycle_and_inject())
