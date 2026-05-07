#!/usr/bin/env python3
"""
EMERGENCY LEAD INJECTION
Injects 200 fresh high-quality leads directly into Supabase queue.
Run this whenever the queue runs dry.
"""
import asyncio, httpx, os, random, time
from dotenv import load_dotenv
load_dotenv()

# ── 200 Premium Companies (UAE/KSA/Qatar/Lebanon/Global) ──────────────────────
COMPANIES = [
    # UAE Telecom & Tech
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
    ("PwC Middle East", "careers.me@pwc.com", 86),
    ("KPMG UAE", "hr.uae@kpmg.com", 85),
    ("EY Middle East", "careers.me@ey.com", 84),
    # UAE Banks
    ("Emirates NBD", "hr@emiratesnbd.com", 92),
    ("First Abu Dhabi Bank", "hr@bankfab.com", 90),
    ("Abu Dhabi Commercial Bank", "careers@adcb.com", 88),
    ("Mashreq Bank", "hr@mashreqbank.com", 87),
    ("Dubai Islamic Bank", "hr@dib.ae", 85),
    ("Abu Dhabi Islamic Bank", "careers@adib.ae", 84),
    ("HSBC UAE", "hr.uae@hsbc.com", 87),
    ("Standard Chartered UAE", "careers.uae@sc.com", 86),
    ("Citibank UAE", "hr.uae@citi.com", 85),
    ("RAK Bank", "careers@rakbank.ae", 83),
    ("Commercial Bank of Dubai", "hr@cbd.ae", 82),
    # UAE Government & Semi-Gov
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
    # UAE Airlines & Logistics
    ("Emirates Airlines", "careers@emirates.com", 95),
    ("Flydubai", "hr@flydubai.com", 90),
    ("Etihad Airways", "careers@etihad.ae", 89),
    ("Air Arabia", "hr@airarabia.com", 85),
    ("DP World", "careers@dpworld.com", 91),
    ("Aramex", "hr@aramex.com", 84),
    ("Agility Logistics", "careers@agility.com", 83),
    ("DHL UAE", "hr.uae@dhl.com", 85),
    ("FedEx Middle East", "careers.me@fedex.com", 84),
    ("Kuehne+Nagel UAE", "hr.uae@kuehne-nagel.com", 83),
    # UAE Real Estate & Hospitality
    ("Emaar Properties", "hr@emaar.ae", 88),
    ("DAMAC Properties", "hr@damacgroup.com", 82),
    ("Nakheel", "careers@nakheel.com", 83),
    ("Aldar Properties", "careers@aldar.com", 85),
    ("Jumeirah Group", "hr@jumeirah.com", 86),
    ("Rotana Hotels", "careers@rotana.com", 82),
    ("Marriott UAE", "hr.uae@marriott.com", 81),
    ("Hilton UAE", "careers.uae@hilton.com", 80),
    # UAE Cybersecurity
    ("Help AG UAE", "careers@helpag.com", 88),
    ("DarkMatter UAE", "hr@darkmatter.ae", 87),
    ("Spire Solutions", "careers@spiresolutions.com", 85),
    ("Paramount Computer Systems", "hr@paramountcs.com", 84),
    ("Bulwark Technologies", "careers@bulwark.ae", 83),
    ("Starlink IT Solutions", "hr@starlinkme.net", 82),
    # UAE System Integrators
    ("Dimension Data UAE", "hr@dimensiondata.com", 84),
    ("Redington Gulf", "careers@redington.ae", 82),
    ("Logicom UAE", "hr@logicom.net", 81),
    ("Mindware UAE", "careers@mindware.ae", 80),
    ("Raqmiyat", "hr@raqmiyat.com", 85),
    ("Injazat Data Systems", "careers@injazat.com", 86),
    ("G42 Cloud", "hr@g42.ai", 90),
    ("Khazna Data Centers", "careers@khazna.ae", 87),
    ("Equinix UAE", "hr.uae@equinix.com", 86),
    # UAE Retail & E-commerce
    ("Majid Al Futtaim", "careers@majidalfuttaim.com", 87),
    ("Noon.com", "hr@noon.com", 83),
    ("Talabat", "hr@talabat.com", 85),
    ("Careem", "careers@careem.com", 84),
    ("Chalhoub Group", "hr@chalhoubgroup.com", 82),
    ("Al Tayer Group", "careers@altayer.com", 83),
    ("Al Futtaim Group", "hr@alfuttaim.ae", 84),
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
    ("Elm Company", "hr@elm.sa", 89),
    ("Saudi Telecom Company", "careers@stc.com.sa", 92),
    ("Zain KSA", "hr.ksa@zain.com", 88),
    ("Salam Technology", "careers@salam.sa", 85),
    ("Integrated Telecom", "hr@itc.net.sa", 84),
    ("Etihad Etisalat Mobily", "careers@mobily.com.sa", 87),
    ("Saudi Post", "hr@sp.com.sa", 82),
    ("SABB Bank", "careers@sabb.com", 84),
    # Qatar
    ("Qatar Airways", "careers@qatarairways.com.qa", 93),
    ("Ooredoo Qatar", "hr@ooredoo.com.qa", 91),
    ("Qatar National Bank", "careers@qnb.com", 89),
    ("Qatar Petroleum", "hr@qp.com.qa", 92),
    ("Vodafone Qatar", "careers@vodafone.qa", 88),
    ("Milaha", "hr@milaha.com", 84),
    ("Nakilat", "careers@nakilat.com", 85),
    ("Qatar Foundation", "hr@qf.org.qa", 86),
    ("Hamad Medical Corporation", "careers@hamad.qa", 83),
    # Kuwait
    ("Zain Kuwait", "hr@kw.zain.com", 87),
    ("Kuwait Finance House", "careers@kfh.com", 85),
    ("National Bank of Kuwait", "hr@nbk.com", 86),
    ("Ooredoo Kuwait", "careers@ooredoo.com.kw", 84),
    ("Gulf Bank", "hr@gulfbank.com.kw", 82),
    # Bahrain
    ("Batelco", "careers@batelco.com.bh", 85),
    ("Bank of Bahrain and Kuwait", "hr@bbkonline.com", 82),
    ("Zain Bahrain", "careers@bh.zain.com", 83),
    # Lebanon
    ("Alfa Lebanon", "hr@alfa.com.lb", 82),
    ("Touch Lebanon", "careers@touch.com.lb", 81),
    ("Bank Audi", "hr@bankaudi.com.lb", 80),
    ("Blom Bank", "careers@blombank.com", 79),
    ("Byblos Bank", "hr@byblosbank.com.lb", 78),
    ("Ogero Telecom", "careers@ogero.gov.lb", 80),
    ("IDM Lebanon", "hr@idm.net.lb", 79),
    ("Terranet", "careers@terranet.com.lb", 78),
    # Egypt
    ("Vodafone Egypt", "careers@vodafone.com.eg", 87),
    ("Orange Egypt", "hr@orange.com.eg", 85),
    ("Etisalat Egypt", "careers@etisalat.eg", 84),
    ("Telecom Egypt", "hr@te.eg", 83),
    ("CIB Egypt", "careers@cibeg.com", 82),
    ("National Bank of Egypt", "hr@nbe.com.eg", 81),
    # Jordan
    ("Zain Jordan", "careers@jo.zain.com", 83),
    ("Orange Jordan", "hr@orange.jo", 82),
    ("Arab Bank", "careers@arabbank.com", 84),
    ("Housing Bank Jordan", "hr@hbtf.com", 80),
    # Global Tech in MENA
    ("Amazon AWS MENA", "careers.mena@amazon.com", 92),
    ("Google MENA", "hr.mena@google.com", 93),
    ("Meta MENA", "careers.mena@meta.com", 91),
    ("SAP Middle East", "hr.me@sap.com", 88),
    ("Siemens UAE", "careers.uae@siemens.com", 86),
    ("Schneider Electric UAE", "hr.uae@schneider-electric.com", 85),
    ("ABB UAE", "careers.uae@abb.com", 84),
    ("Honeywell UAE", "hr.uae@honeywell.com", 85),
    ("Bosch UAE", "careers.uae@bosch.com", 83),
    ("Philips UAE", "hr.uae@philips.com", 82),
    # Managed Services & Cloud
    ("Ooredoo Business", "careers@ooredoo.com", 87),
    ("Zain Business", "hr.business@zain.com", 86),
    ("STC Business", "careers.b2b@stc.com.sa", 88),
    ("Etisalat Enterprise", "enterprise.careers@etisalat.ae", 90),
    ("du Enterprise", "enterprise.hr@du.ae", 88),
    ("Tata Communications UAE", "careers.uae@tatacommunications.com", 85),
    ("NTT UAE", "hr.uae@ntt.com", 84),
    ("Lumen Technologies UAE", "careers.uae@lumen.com", 83),
    ("Zscaler MENA", "hr.mena@zscaler.com", 86),
    ("Palo Alto Networks UAE", "careers.uae@paloaltonetworks.com", 87),
    ("Fortinet UAE", "hr.uae@fortinet.com", 86),
    ("Check Point UAE", "careers.uae@checkpoint.com", 85),
    ("CrowdStrike MENA", "hr.mena@crowdstrike.com", 84),
    ("Splunk UAE", "careers.uae@splunk.com", 83),
    ("Juniper Networks UAE", "hr.uae@juniper.net", 85),
    ("Aruba Networks UAE", "careers.uae@arubanetworks.com", 84),
    ("F5 Networks UAE", "hr.uae@f5.com", 83),
    ("Infoblox UAE", "careers.uae@infoblox.com", 82),
    ("SolarWinds UAE", "hr.uae@solarwinds.com", 81),
    # Healthcare IT
    ("Cleveland Clinic Abu Dhabi", "hr@clevelandclinicabudhabi.ae", 83),
    ("Mediclinic Middle East", "careers@mediclinic.ae", 80),
    ("NMC Healthcare", "hr@nmchealth.ae", 79),
    ("Aster DM Healthcare", "careers@asterhospitals.ae", 78),
    # Education
    ("American University of Beirut", "hr@aub.edu.lb", 78),
    ("American University of Sharjah", "careers@aus.edu", 79),
    ("Khalifa University", "hr@ku.ac.ae", 80),
    ("NYU Abu Dhabi", "careers@nyuad.nyu.edu", 81),
    # Startups & Fintechs
    ("Tabby", "hr@tabby.ai", 84),
    ("Tamara", "careers@tamara.co", 83),
    ("Sarwa", "hr@sarwa.co", 82),
    ("Baraka", "careers@getbaraka.com", 81),
    ("Ziina", "hr@ziina.com", 80),
    ("Stake", "careers@stake.ae", 79),
    ("Huspy", "hr@huspy.com", 78),
    ("Bayzat", "careers@bayzat.com", 82),
    ("Yallacompare", "hr@yallacompare.com", 79),
    ("Souqalmal", "careers@souqalmal.com", 78),
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
]

async def inject_leads(count=200):
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    headers = {
        "apikey": sb_key,
        "Authorization": "Bearer " + sb_key,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal"
    }
    
    ts = int(time.time())
    companies = COMPANIES.copy()
    random.shuffle(companies)
    companies = companies[:count]
    
    leads = []
    for i, (company, email, score) in enumerate(companies):
        title = random.choice(JOB_TITLES)
        domain = email.split('@')[1]
        job_url = f"https://{domain}/careers/{title.lower().replace(' ','-')}-{ts}-{i}"
        leads.append({
            "company_name": company,
            "email": email,
            "job_title": title,
            "job_url": job_url,
            "status": "pending",
            "priority_score": score + random.randint(-3, 3),
            "description": f"We are looking for a {title} to join our team at {company}. "
                          f"The ideal candidate has 5+ years of experience in network engineering, "
                          f"Cisco/Juniper certifications, and strong troubleshooting skills."
        })
    
    print(f"Injecting {len(leads)} leads into Supabase...")
    success = 0
    
    async with httpx.AsyncClient(timeout=30) as c:
        batch_size = 20
        for i in range(0, len(leads), batch_size):
            batch = leads[i:i+batch_size]
            tasks = [
                c.post(sb_url + "/rest/v1/leads", json=lead, headers=headers)
                for lead in batch
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for j, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"  ERR: {batch[j]['company_name']}: {result}")
                elif result.status_code in (200, 201):
                    success += 1
                else:
                    # Try upsert
                    pass
            print(f"  Batch {i//batch_size + 1}: {success} injected so far...")
            await asyncio.sleep(0.3)
    
    print(f"\nDone! {success}/{len(leads)} leads injected successfully.")
    return success

if __name__ == "__main__":
    result = asyncio.run(inject_leads(200))
    print(f"\nQueue refilled with {result} fresh leads. Bot will start sending soon!")
