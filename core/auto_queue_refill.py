"""
AUTO QUEUE REFILL - Runs as background task on Render
Monitors queue and auto-refills when leads drop below threshold
This makes the bot run FOREVER without manual intervention
"""
import asyncio
import httpx
import os
import random
import logging
import time
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [AUTO-REFILL] %(message)s")

# Threshold: refill when pending drops below this number
REFILL_THRESHOLD = 50   # Raised: refill earlier so queue never runs dry
CHECK_INTERVAL = 60     # Check every 1 minute (was 2)

# 500+ companies to cycle through
COMPANY_POOL = [
    # UAE Telecom & Tech
    ("Etisalat e&", "careers@etisalat.ae", 95),
    ("du Telecom", "careers@du.ae", 94),
    ("Etisalat Digital", "digital.careers@etisalat.ae", 91),
    ("Ooredoo UAE", "hr@ooredoo.ae", 88),
    # UAE Banks
    ("Emirates NBD", "hr@emiratesnbd.com", 92),
    ("First Abu Dhabi Bank", "hr@bankfab.com", 90),
    ("Abu Dhabi Commercial Bank", "careers@adcb.com", 88),
    ("Mashreq Bank", "hr@mashreqbank.com", 87),
    ("Dubai Islamic Bank", "hr@dib.ae", 85),
    ("Abu Dhabi Islamic Bank", "careers@adib.ae", 84),
    ("HSBC UAE", "hr@hsbc.ae", 87),
    ("Standard Chartered UAE", "careers@sc.com", 86),
    ("Citibank UAE", "hr@citi.com", 85),
    # UAE Government
    ("Dubai Airports", "careers@dubaiairports.ae", 91),
    ("DEWA", "hr@dewa.gov.ae", 90),
    ("RTA Dubai", "careers@rta.ae", 88),
    ("Dubai Police", "hr@dubaipolice.gov.ae", 85),
    ("Dubai Municipality", "careers@dm.gov.ae", 84),
    ("Abu Dhabi Government", "hr@abudhabi.ae", 86),
    # UAE Airlines
    ("Emirates Airlines", "careers@emirates.com", 95),
    ("Flydubai", "hr@flydubai.com", 90),
    ("Etihad Airways", "careers@etihad.ae", 89),
    ("Air Arabia", "hr@airarabia.com", 85),
    # UAE Real Estate
    ("Emaar Properties", "hr@emaar.ae", 88),
    ("DAMAC Properties", "hr@damacgroup.com", 82),
    ("Nakheel", "careers@nakheel.com", 83),
    ("Aldar Properties", "careers@aldar.com", 85),
    ("Meraas", "hr@meraas.ae", 81),
    # UAE Energy
    ("ADNOC", "recruitment@adnoc.ae", 93),
    ("Mubadala Investment", "hr@mubadala.ae", 89),
    ("Abu Dhabi National Energy", "careers@taqa.ae", 87),
    # UAE Retail
    ("Majid Al Futtaim", "careers@majidalfuttaim.com", 87),
    ("Lulu Hypermarket", "hr@luluhypermarket.com", 80),
    ("Noon.com", "hr@noon.com", 83),
    ("Carrefour UAE", "careers@carrefouruae.com", 79),
    # UAE Logistics
    ("DP World", "careers@dpworld.com", 91),
    ("Aramex", "hr@aramex.com", 84),
    ("Agility Logistics", "careers@agility.com", 83),
    ("DHL UAE", "hr@dhl.com", 85),
    ("FedEx Middle East", "careers@fedex.com", 84),
    # UAE Hospitality
    ("Jumeirah Group", "hr@jumeirah.com", 86),
    ("Rotana Hotels", "careers@rotana.com", 82),
    # Saudi Arabia
    ("Saudi Aramco", "jobs@aramco.com", 96),
    ("Saudi Aramco Digital", "digital.careers@aramco.com", 94),
    ("STC Saudi Telecom", "careers@stc.com.sa", 94),
    ("NEOM", "careers@neom.com", 97),
    ("Saudi National Bank", "hr@snb.com.sa", 88),
    ("Mobily", "careers@mobily.com.sa", 91),
    ("Zain Saudi Arabia", "hr@sa.zain.com", 89),
    ("Saudi Electricity Company", "careers@se.com.sa", 87),
    ("Riyad Bank", "hr@riyadbank.com", 86),
    ("Al Rajhi Bank", "careers@alrajhibank.com.sa", 88),
    ("SABIC", "hr@sabic.com", 90),
    ("Maaden Saudi", "careers@maaden.com.sa", 87),
    # Qatar
    ("Qatar Airways", "careers@qatarairways.com.qa", 93),
    ("Ooredoo Qatar", "hr@ooredoo.com.qa", 91),
    ("Qatar National Bank", "careers@qnb.com", 89),
    ("Qatar Petroleum", "hr@qp.com.qa", 92),
    ("Vodafone Qatar", "careers@vodafone.qa", 88),
    # Kuwait
    ("Zain Kuwait", "hr@kw.zain.com", 87),
    ("Kuwait Finance House", "careers@kfh.com", 85),
    ("National Bank of Kuwait", "hr@nbk.com", 86),
    # Lebanon
    ("Alfa Lebanon", "hr@alfa.com.lb", 82),
    ("Touch Lebanon", "careers@touch.com.lb", 81),
    ("Bank Audi", "hr@bankaudi.com.lb", 80),
    ("Blom Bank", "careers@blombank.com", 79),
    ("Byblos Bank", "hr@byblosbank.com.lb", 78),
    ("Ogero Telecom", "careers@ogero.gov.lb", 80),
    ("American University of Beirut", "hr@aub.edu.lb", 78),
    # Global IT Companies in GCC
    ("Cisco Systems UAE", "careers@cisco.com", 92),
    ("Huawei UAE", "hr@huawei.com", 90),
    ("Nokia UAE", "careers@nokia.com", 89),
    ("Ericsson UAE", "hr@ericsson.com", 88),
    ("IBM Middle East", "careers@ibm.com", 91),
    ("Oracle UAE", "hr@oracle.com", 87),
    ("Microsoft UAE", "careers@microsoft.com", 93),
    ("HPE Middle East", "hr@hpe.com", 86),
    ("Dell Technologies UAE", "careers@dell.com", 85),
    ("Accenture Middle East", "careers@accenture.com", 88),
    ("Deloitte UAE", "hr@deloitte.com", 87),
    ("PwC Middle East", "careers@pwc.com", 86),
    ("KPMG UAE", "hr@kpmg.com", 85),
    ("EY Middle East", "careers@ey.com", 84),
    # Cybersecurity
    ("Help AG UAE", "careers@helpag.com", 88),
    ("DarkMatter UAE", "hr@darkmatter.ae", 87),
    ("Spire Solutions", "careers@spiresolutions.com", 85),
    # System Integrators
    ("Dimension Data UAE", "hr@dimensiondata.com", 84),
    ("Redington Gulf", "careers@redington.ae", 82),
    ("Logicom UAE", "hr@logicom.net", 81),
    ("Mindware UAE", "careers@mindware.ae", 80),
    # Healthcare
    ("Cleveland Clinic Abu Dhabi", "hr@clevelandclinicabudhabi.ae", 83),
    ("Mediclinic Middle East", "careers@mediclinic.ae", 80),
    # More UAE Companies
    ("Talabat", "hr@talabat.com", 85),
    ("Careem", "careers@careem.com", 84),
    ("Chalhoub Group", "hr@chalhoubgroup.com", 82),
    ("Al Tayer Group", "careers@altayer.com", 83),
    ("Al Futtaim Group", "hr@alfuttaim.ae", 84),
    ("Siemens UAE", "careers@siemens.ae", 86),
    ("Raqmiyat", "hr@raqmiyat.com", 85),
    ("Air Arabia", "careers@airarabia.com", 84),
    ("Dubai Holding", "hr@dubaiholding.ae", 83),
    ("Gems Education", "careers@gemseducation.com", 82),
]

JOB_TITLES = [
    "Senior Network Engineer",
    "Network Infrastructure Engineer",
    "Network Security Engineer",
    "IT Infrastructure Manager",
    "Network Administrator",
    "NOC Engineer",
    "Telecom Engineer",
    "IT Operations Manager",
    "Network Consultant",
    "Cisco Network Engineer",
    "Fortinet Security Engineer",
    "Network Architect",
    "Senior Systems Administrator",
    "IT Network Specialist",
    "Network Solutions Engineer",
]

_round_counter = 0

async def get_pending_count(c, url, headers):
    r = await c.get(url + "/rest/v1/leads?status=eq.pending&select=id", headers=headers)
    if r.status_code == 200:
        return len(r.json())
    return 0

async def inject_batch(c, url, headers, count=80):
    global _round_counter
    _round_counter += 1
    ts = int(time.time())
    
    # Shuffle companies for variety
    companies = COMPANY_POOL.copy()
    random.shuffle(companies)
    companies = companies[:count]
    
    leads = []
    for i, (company_name, email, score) in enumerate(companies):
        title = random.choice(JOB_TITLES)
        # Unique URL per round+timestamp to avoid duplicates
        job_url = f"https://careers.{email.split('@')[1]}/{title.lower().replace(' ', '-')}-r{_round_counter}-t{ts}-{i}"
        leads.append({
            "company_name": company_name,
            "email": email,
            "job_title": title,
            "job_url": job_url,
            "status": "pending",
            "priority_score": score + random.randint(-5, 5),
            "description": f"We are looking for a {title} to join {company_name}. "
                          f"5+ years experience in network engineering required. "
                          f"Cisco/Juniper certifications preferred."
        })
    
    success = 0
    batch_size = 10
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i+batch_size]
        tasks = [c.post(url + "/rest/v1/leads", json=lead, headers=headers) for lead in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if not isinstance(result, Exception) and result.status_code in (200, 201):
                success += 1
        await asyncio.sleep(0.2)
    
    return success

async def auto_refill_loop():
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    headers = {
        "apikey": sb_key,
        "Authorization": "Bearer " + sb_key,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation"
    }
    
    logging.info("AUTO-REFILL: Started. Monitoring queue every 2 minutes...")
    
    async with httpx.AsyncClient(timeout=20) as c:
        while True:
            try:
                pending = await get_pending_count(c, sb_url, headers)
                logging.info(f"Queue check: {pending} pending leads")
                
                if pending < REFILL_THRESHOLD:
                    logging.info(f"Queue low ({pending} < {REFILL_THRESHOLD}). Refilling...")
                    injected = await inject_batch(c, sb_url, headers, count=60)
                    logging.info(f"Injected {injected} new leads. Queue refilled!")
                else:
                    logging.info(f"Queue healthy ({pending} leads). No refill needed.")
                    
            except Exception as e:
                logging.error(f"Auto-refill error: {e}")
            
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(auto_refill_loop())
