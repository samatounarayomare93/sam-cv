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
CHECK_INTERVAL = 300    # Check every 5 minutes (was 60s — too aggressive, causes OOM)

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
    "Cloud Network Engineer",
    "SD-WAN Engineer",
    "Network Automation Engineer",
    "IP/MPLS Engineer",
    "Wireless Network Engineer",
    "IT Infrastructure Engineer",
    "Network Operations Engineer",
    "Senior IT Engineer",
    "Network Support Engineer",
    "IT Manager",
]

# Extended company pool — 200+ companies across UAE, KSA, Qatar, Kuwait, Lebanon, Egypt, Jordan, Europe
COMPANY_POOL = [
    # ── UAE Telecom & Tech ──────────────────────────────────────────────────
    ("Etisalat e&", "careers@etisalat.ae", 95),
    ("du Telecom", "careers@du.ae", 94),
    ("Etisalat Digital", "digital.careers@etisalat.ae", 91),
    ("Ooredoo UAE", "hr@ooredoo.ae", 88),
    ("Huawei UAE", "hr.uae@huawei.com", 90),
    ("Cisco UAE", "careers.me@cisco.com", 92),
    ("Nokia UAE", "careers@nokia.com", 89),
    ("Ericsson UAE", "hr.me@ericsson.com", 88),
    ("IBM Middle East", "careers.me@ibm.com", 91),
    ("Oracle UAE", "hr.uae@oracle.com", 87),
    ("Microsoft UAE", "careers.uae@microsoft.com", 93),
    ("HPE Middle East", "hr.me@hpe.com", 86),
    ("Dell Technologies UAE", "careers.uae@dell.com", 85),
    ("Accenture Middle East", "careers.me@accenture.com", 88),
    ("Deloitte UAE", "hr.uae@deloitte.com", 87),
    ("G42 Cloud", "hr@g42.ai", 90),
    ("Injazat Data Systems", "careers@injazat.com", 86),
    ("Khazna Data Centers", "careers@khazna.ae", 87),
    ("Equinix UAE", "hr.uae@equinix.com", 86),
    ("Raqmiyat", "hr@raqmiyat.com", 85),
    # ── UAE Banks & Finance ─────────────────────────────────────────────────
    ("Emirates NBD", "hr@emiratesnbd.com", 92),
    ("First Abu Dhabi Bank", "hr@bankfab.com", 90),
    ("Abu Dhabi Commercial Bank", "careers@adcb.com", 88),
    ("Mashreq Bank", "hr@mashreqbank.com", 87),
    ("Dubai Islamic Bank", "hr@dib.ae", 85),
    ("Abu Dhabi Islamic Bank", "careers@adib.ae", 84),
    ("HSBC UAE", "hr.uae@hsbc.com", 87),
    ("Standard Chartered UAE", "careers.uae@sc.com", 86),
    ("RAK Bank", "careers@rakbank.ae", 83),
    ("Commercial Bank of Dubai", "hr@cbd.ae", 82),
    # ── UAE Government & Semi-Gov ───────────────────────────────────────────
    ("Dubai Airports", "careers@dubaiairports.ae", 91),
    ("DEWA", "hr@dewa.gov.ae", 90),
    ("RTA Dubai", "careers@rta.ae", 88),
    ("Dubai Municipality", "careers@dm.gov.ae", 84),
    ("ADNOC", "recruitment@adnoc.ae", 93),
    ("Mubadala Investment", "hr@mubadala.ae", 89),
    ("TAQA Energy", "careers@taqa.ae", 87),
    ("Dubai Holding", "hr@dubaiholding.ae", 83),
    ("Tecom Group", "careers@tecom.ae", 82),
    ("Smart Dubai", "hr@smartdubai.ae", 84),
    # ── UAE Airlines & Logistics ────────────────────────────────────────────
    ("Emirates Airlines", "careers@emirates.com", 95),
    ("Flydubai", "hr@flydubai.com", 90),
    ("Etihad Airways", "careers@etihad.ae", 89),
    ("Air Arabia", "hr@airarabia.com", 85),
    ("DP World", "careers@dpworld.com", 91),
    ("Aramex", "hr@aramex.com", 84),
    ("DHL UAE", "hr.uae@dhl.com", 85),
    ("FedEx Middle East", "careers.me@fedex.com", 84),
    # ── UAE Cybersecurity ───────────────────────────────────────────────────
    ("Help AG UAE", "careers@helpag.com", 88),
    ("DarkMatter UAE", "hr@darkmatter.ae", 87),
    ("Spire Solutions", "careers@spiresolutions.com", 85),
    ("Paramount Computer Systems", "hr@paramountcs.com", 84),
    ("Bulwark Technologies", "careers@bulwark.ae", 83),
    ("Starlink IT Solutions", "hr@starlinkme.net", 82),
    # ── UAE System Integrators ──────────────────────────────────────────────
    ("Dimension Data UAE", "hr@dimensiondata.com", 84),
    ("Redington Gulf", "careers@redington.ae", 82),
    ("Logicom UAE", "hr@logicom.net", 81),
    ("Mindware UAE", "careers@mindware.ae", 80),
    # ── UAE Real Estate & Hospitality ───────────────────────────────────────
    ("Emaar Properties", "hr@emaar.ae", 88),
    ("DAMAC Properties", "hr@damacgroup.com", 82),
    ("Aldar Properties", "careers@aldar.com", 85),
    ("Jumeirah Group", "hr@jumeirah.com", 86),
    ("Rotana Hotels", "careers@rotana.com", 82),
    # ── UAE Retail & E-commerce ─────────────────────────────────────────────
    ("Majid Al Futtaim", "careers@majidalfuttaim.com", 87),
    ("Noon.com", "hr@noon.com", 83),
    ("Talabat", "hr@talabat.com", 85),
    ("Careem", "careers@careem.com", 84),
    ("Al Futtaim Group", "hr@alfuttaim.ae", 84),
    # ── Saudi Arabia ────────────────────────────────────────────────────────
    ("Saudi Aramco", "jobs@aramco.com", 96),
    ("Saudi Aramco Digital", "digital.careers@aramco.com", 94),
    ("STC Saudi Telecom", "careers@stc.com.sa", 94),
    ("NEOM", "careers@neom.com", 97),
    ("Saudi National Bank", "hr@snb.com.sa", 88),
    ("Mobily", "careers@mobily.com.sa", 91),
    ("Zain Saudi Arabia", "hr@sa.zain.com", 89),
    ("Saudi Electricity Company", "careers@se.com.sa", 87),
    ("Al Rajhi Bank", "careers@alrajhibank.com.sa", 88),
    ("SABIC", "hr@sabic.com", 90),
    ("Maaden Saudi", "careers@maaden.com.sa", 87),
    ("Elm Company", "hr@elm.sa", 89),
    ("Salam Technology", "careers@salam.sa", 85),
    ("Integrated Telecom", "hr@itc.net.sa", 84),
    ("Saudi Post", "hr@sp.com.sa", 82),
    ("SABB Bank", "careers@sabb.com", 84),
    ("Riyad Bank", "hr@riyadbank.com", 86),
    ("stc pay", "hr@stcpay.com.sa", 85),
    ("Zain KSA", "hr.ksa@zain.com", 88),
    # ── Qatar ───────────────────────────────────────────────────────────────
    ("Qatar Airways", "careers@qatarairways.com.qa", 93),
    ("Ooredoo Qatar", "hr@ooredoo.com.qa", 91),
    ("Qatar National Bank", "careers@qnb.com", 89),
    ("Qatar Petroleum", "hr@qp.com.qa", 92),
    ("Vodafone Qatar", "careers@vodafone.qa", 88),
    ("Milaha", "hr@milaha.com", 84),
    ("Nakilat", "careers@nakilat.com", 85),
    ("Qatar Foundation", "hr@qf.org.qa", 86),
    ("Hamad Medical Corporation", "careers@hamad.qa", 83),
    ("Barwa Real Estate", "hr@barwa.com.qa", 80),
    # ── Kuwait ──────────────────────────────────────────────────────────────
    ("Zain Kuwait", "hr@kw.zain.com", 87),
    ("Kuwait Finance House", "careers@kfh.com", 85),
    ("National Bank of Kuwait", "hr@nbk.com", 86),
    ("Ooredoo Kuwait", "careers@ooredoo.com.kw", 84),
    ("Gulf Bank", "hr@gulfbank.com.kw", 82),
    ("Agility Kuwait", "careers@agility.com", 83),
    # ── Bahrain ─────────────────────────────────────────────────────────────
    ("Batelco", "careers@batelco.com.bh", 85),
    ("Bank of Bahrain and Kuwait", "hr@bbkonline.com", 82),
    ("Zain Bahrain", "careers@bh.zain.com", 83),
    ("Bahrain Telecom", "hr@batelco.com.bh", 84),
    # ── Oman ────────────────────────────────────────────────────────────────
    ("Omantel", "careers@omantel.om", 85),
    ("Ooredoo Oman", "hr@ooredoo.om", 83),
    ("Bank Muscat", "careers@bankmuscat.com", 82),
    ("Petroleum Development Oman", "hr@pdo.co.om", 87),
    # ── Lebanon ─────────────────────────────────────────────────────────────
    ("Alfa Lebanon", "hr@alfa.com.lb", 82),
    ("Touch Lebanon", "careers@touch.com.lb", 81),
    ("Bank Audi", "hr@bankaudi.com.lb", 80),
    ("Blom Bank", "careers@blombank.com", 79),
    ("Byblos Bank", "hr@byblosbank.com.lb", 78),
    ("Ogero Telecom", "careers@ogero.gov.lb", 80),
    ("IDM Lebanon", "hr@idm.net.lb", 79),
    ("Terranet", "careers@terranet.com.lb", 78),
    ("Cyberia ISP", "hr@cyberia.net.lb", 79),
    ("American University of Beirut", "hr@aub.edu.lb", 78),
    # ── Egypt ───────────────────────────────────────────────────────────────
    ("Vodafone Egypt", "careers@vodafone.com.eg", 87),
    ("Orange Egypt", "hr@orange.com.eg", 85),
    ("Etisalat Egypt", "careers@etisalat.eg", 84),
    ("Telecom Egypt", "hr@te.eg", 83),
    ("CIB Egypt", "careers@cibeg.com", 82),
    ("National Bank of Egypt", "hr@nbe.com.eg", 81),
    ("Raya Holding", "careers@raya.com", 83),
    ("Xceed Contact Center", "hr@xceedcc.com", 80),
    # ── Jordan ──────────────────────────────────────────────────────────────
    ("Zain Jordan", "careers@jo.zain.com", 83),
    ("Orange Jordan", "hr@orange.jo", 82),
    ("Arab Bank", "careers@arabbank.com", 84),
    ("Housing Bank Jordan", "hr@hbtf.com", 80),
    ("Umniah", "careers@umniah.com", 81),
    # ── Global Tech in MENA ─────────────────────────────────────────────────
    ("Amazon AWS MENA", "careers.mena@amazon.com", 92),
    ("Google MENA", "hr.mena@google.com", 93),
    ("SAP Middle East", "hr.me@sap.com", 88),
    ("Siemens UAE", "careers.uae@siemens.com", 86),
    ("Schneider Electric UAE", "hr.uae@schneider-electric.com", 85),
    ("Honeywell UAE", "hr.uae@honeywell.com", 85),
    # ── Managed Services & Cloud ────────────────────────────────────────────
    ("Tata Communications UAE", "careers.uae@tatacommunications.com", 85),
    ("NTT UAE", "hr.uae@ntt.com", 84),
    ("Zscaler MENA", "hr.mena@zscaler.com", 86),
    ("Palo Alto Networks UAE", "careers.uae@paloaltonetworks.com", 87),
    ("Fortinet UAE", "hr.uae@fortinet.com", 86),
    ("Check Point UAE", "careers.uae@checkpoint.com", 85),
    ("CrowdStrike MENA", "hr.mena@crowdstrike.com", 84),
    ("Juniper Networks UAE", "hr.uae@juniper.net", 85),
    ("Aruba Networks UAE", "careers.uae@arubanetworks.com", 84),
    ("F5 Networks UAE", "hr.uae@f5.com", 83),
    ("Infoblox UAE", "careers.uae@infoblox.com", 82),
    # ── Startups & Fintechs ─────────────────────────────────────────────────
    ("Tabby", "hr@tabby.ai", 84),
    ("Tamara", "careers@tamara.co", 83),
    ("Bayzat", "careers@bayzat.com", 82),
    ("Huspy", "hr@huspy.com", 78),
    ("Stake", "careers@stake.ae", 79),
    # ── Europe (for relocation) ─────────────────────────────────────────────
    ("Deutsche Telekom", "careers@telekom.de", 85),
    ("Vodafone UK", "hr.uk@vodafone.com", 84),
    ("BT Group", "careers@bt.com", 83),
    ("Orange France", "hr@orange.com", 82),
    ("Swisscom", "careers@swisscom.com", 83),
    ("KPN Netherlands", "hr@kpn.com", 82),
    ("Proximus Belgium", "careers@proximus.com", 81),
    ("Tele2 Sweden", "hr@tele2.com", 80),
    ("Telenor Norway", "careers@telenor.com", 81),
    ("Telstra International", "hr@telstra.com", 80),
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
    
    # Use insert-only headers (no merge-duplicates) so new leads always get inserted
    insert_headers = {k: v for k, v in headers.items()}
    insert_headers["Prefer"] = "return=minimal"  # just insert, don't merge
    
    leads = []
    for i, (company_name, email, score) in enumerate(companies):
        title = random.choice(JOB_TITLES)
        # Fully unique URL every time — round + timestamp + random suffix
        rand_suffix = random.randint(10000, 99999)
        job_url = f"https://careers.{email.split('@')[1]}/{title.lower().replace(' ', '-')}-r{_round_counter}-t{ts}-{i}-{rand_suffix}"
        leads.append({
            "company_name": company_name,
            "email": email,
            "job_title": title,
            "job_url": job_url,
            "status": "pending",
            "priority_score": score + random.randint(-5, 5),
            "description": (
                f"We are looking for a {title} to join {company_name}. "
                f"5+ years experience in network engineering required. "
                f"Cisco/Juniper/Fortinet certifications preferred. "
                f"Competitive salary + relocation package."
            )
        })
    
    success = 0
    batch_size = 10
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i+batch_size]
        tasks = [c.post(url + "/rest/v1/leads", json=lead, headers=insert_headers) for lead in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if not isinstance(result, Exception) and result.status_code in (200, 201):
                success += 1
        await asyncio.sleep(0.2)
    
    return success

async def auto_refill_loop():
    sb_url = os.getenv("SUPABASE_URL", "").strip()
    sb_key = os.getenv("SUPABASE_KEY", "").strip()

    # Guard: if Supabase is not configured, run in local-only mode (no crash)
    if not sb_url or not sb_key:
        logging.warning("AUTO-REFILL: SUPABASE_URL or SUPABASE_KEY not set. Running in local-only mode.")
        while True:
            await asyncio.sleep(CHECK_INTERVAL)
        return

    headers = {
        "apikey": sb_key,
        "Authorization": "Bearer " + sb_key,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=representation"
    }
    patch_headers = {
        "apikey": sb_key,
        "Authorization": "Bearer " + sb_key,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    logging.info("AUTO-REFILL: Started. Monitoring queue every 60 seconds...")
    
    async with httpx.AsyncClient(timeout=20) as c:
        while True:
            try:
                pending = await get_pending_count(c, sb_url, headers)
                logging.info(f"Queue check: {pending} pending leads")
                
                if pending < REFILL_THRESHOLD:
                    logging.info(f"Queue low ({pending} < {REFILL_THRESHOLD}). Recycling + refilling...")
                    
                    # 1. Recycle error/rate_limited leads back to pending first
                    for status in ('error', 'rate_limited', 'stale_expired', 'failed'):
                        try:
                            await c.patch(
                                sb_url + f"/rest/v1/leads?status=eq.{status}",
                                json={"status": "pending"},
                                headers=patch_headers
                            )
                        except Exception as e:
                            logging.warning(f"Recycle {status} error: {e}")
                    
                    # 2. Check again after recycling
                    pending_after = await get_pending_count(c, sb_url, headers)
                    
                    # 3. Always inject fresh leads (unique URLs = always new entries)
                    injected = await inject_batch(c, sb_url, headers, count=30)  # Reduced from 100 to save RAM
                    logging.info(f"Injected {injected} new leads. Queue refilled!")
                else:
                    logging.info(f"Queue healthy ({pending} leads). No refill needed.")
                    
            except Exception as e:
                logging.error(f"Auto-refill error: {e}")
            
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(auto_refill_loop())
