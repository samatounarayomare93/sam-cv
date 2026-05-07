"""Inject starter leads into Supabase to kickstart the application queue."""
import os, httpx, asyncio
from dotenv import load_dotenv
load_dotenv()

SAMPLE_LEADS = [
    {"company_name": "Majid Al Futtaim", "job_title": "HR Operations Manager", "email": "careers@majidalfuttaim.com", "job_url": "https://www.majidalfuttaim.com/careers", "status": "pending", "priority_score": 90},
    {"company_name": "Emaar Properties", "job_title": "HR Manager", "email": "hr@emaar.ae", "job_url": "https://www.emaar.com/careers", "status": "pending", "priority_score": 88},
    {"company_name": "NEOM", "job_title": "Operations Manager", "email": "careers@neom.com", "job_url": "https://www.neom.com/careers", "status": "pending", "priority_score": 95},
    {"company_name": "Aramco", "job_title": "HR Business Partner", "email": "recruitment@aramco.com", "job_url": "https://www.aramco.com/careers", "status": "pending", "priority_score": 92},
    {"company_name": "Dubai Future Foundation", "job_title": "Administrative Manager", "email": "hr@dubaifuture.ae", "job_url": "https://www.dubaifuture.ae/careers", "status": "pending", "priority_score": 87},
    {"company_name": "Aldar Properties", "job_title": "HR Director", "email": "careers@aldar.com", "job_url": "https://www.aldar.com/careers", "status": "pending", "priority_score": 85},
    {"company_name": "Mubadala Investment", "job_title": "Operations Lead", "email": "hr@mubadala.ae", "job_url": "https://www.mubadala.com/careers", "status": "pending", "priority_score": 89},
    {"company_name": "Saudi Aramco", "job_title": "HR Manager", "email": "jobs@aramco.com", "job_url": "https://www.aramco.com/jobs", "status": "pending", "priority_score": 93},
    {"company_name": "Etihad Airways", "job_title": "HR Business Partner", "email": "careers@etihad.ae", "job_url": "https://www.etihad.com/careers", "status": "pending", "priority_score": 86},
    {"company_name": "Abu Dhabi National Oil", "job_title": "Administrative Manager", "email": "recruitment@adnoc.ae", "job_url": "https://www.adnoc.ae/careers", "status": "pending", "priority_score": 91},
]

async def inject():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    headers = {
        "apikey": key,
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation"
    }
    
    print("Injecting leads into Supabase...")
    async with httpx.AsyncClient(timeout=15) as c:
        success_count = 0
        for lead in SAMPLE_LEADS:
            r = await c.post(url + "/rest/v1/leads", json=lead, headers=headers)
            status = "OK" if r.status_code in (200, 201) else "FAIL:" + str(r.status_code)
            print(f"  {lead['company_name']}: {status}")
            if r.status_code in (200, 201):
                success_count += 1
        
        print()
        print(f"Injected: {success_count}/{len(SAMPLE_LEADS)} leads")
        
        # Verify pending count
        r2 = await c.get(url + "/rest/v1/leads?status=eq.pending&limit=20", headers=headers)
        data = r2.json()
        print(f"Total pending leads in queue: {len(data)}")
        for l in data:
            print(f"  - {l.get('company_name')} | {l.get('email')}")

asyncio.run(inject())
