import os
import re
import asyncio

file_path = 'core/scrapers/omni_crawler.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will write a regex to find all blocks:
#             with DDGS() as ddgs:
#                 <anything>
# and replace them with:
#             def _sync():
#                 with DDGS() as ddgs:
#                     return <anything>
#             results = await asyncio.to_thread(_sync)
# BUT wait, the block might be multiple lines, and there's logic inside!

# 1. get_latest_news
content = content.replace('''            with DDGS() as ddgs:
                results = list(ddgs.text(f"{company} news 2024", max_results=3))
                if results:
                    return f"{results[0]['title']}: {results[0]['body'][:100]}..."''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(f"{company} news 2024", max_results=3))
            results = await asyncio.to_thread(_sync)
            if results:
                return f"{results[0]['title']}: {results[0]['body'][:100]}..."''')

# 2. get_news_pulse
content = content.replace('''            with DDGS() as ddgs:
                # Search for specific strategic signals
                query = f'"{company}" (layoffs OR growth OR "new CEO" OR acquisition OR expansion)'
                results = list(ddgs.text(query, max_results=5))
                
                content = " ".join([r['body'].lower() for r in results])
                
                if any(x in content for x in ["layoff", "job cuts", "downsizing", "restructuring"]):
                    pulse = {"sentiment": "negative", "event": "Restructuring", "strategy": "Efficiency & Stability"}
                elif any(x in content for x in ["funding", "raised", "acquisition", "opening", "growth"]):
                    pulse = {"sentiment": "positive", "event": "Rapid Expansion", "strategy": "Scaling & Automation"}
                elif "ceo" in content or "leadership" in content:
                    pulse = {"sentiment": "neutral", "event": "Leadership Change", "strategy": "Culture Alignment"}''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(f'"{company}" (layoffs OR growth OR "new CEO" OR acquisition OR expansion)', max_results=5))
            results = await asyncio.to_thread(_sync)
            
            content = " ".join([r['body'].lower() for r in results])
            
            if any(x in content for x in ["layoff", "job cuts", "downsizing", "restructuring"]):
                pulse = {"sentiment": "negative", "event": "Restructuring", "strategy": "Efficiency & Stability"}
            elif any(x in content for x in ["funding", "raised", "acquisition", "opening", "growth"]):
                pulse = {"sentiment": "positive", "event": "Rapid Expansion", "strategy": "Scaling & Automation"}
            elif "ceo" in content or "leadership" in content:
                pulse = {"sentiment": "neutral", "event": "Leadership Change", "strategy": "Culture Alignment"}''')

# 3. run_discovery_cycle
content = content.replace('''            with DDGS() as ddgs:
                for query in PlatformDiscovery.DISCOVERY_QUERIES:
                    logging.info(f"🔎 Scanning for new platforms: {query[:40]}...")
                    results = list(ddgs.text(query, max_results=20))
                    for res in results:
                        url = res.get('href')
                        if url:
                            # [🚫 SOVEREIGN EXCLUSION]: Skip Israel-related platforms
                            if ".il" in url.lower() or "israel" in url.lower():
                                continue
                            # Log as a discovered link
                            await db_manager.client.add_discovered_link(url, source=f"Discovery: {query}")
                            discovered.append(url)
                    await asyncio.sleep(5) # Jitter''', '''            for query in PlatformDiscovery.DISCOVERY_QUERIES:
                logging.info(f"🔎 Scanning for new platforms: {query[:40]}...")
                def _sync(q=query):
                    with DDGS() as ddgs: return list(ddgs.text(q, max_results=20))
                results = await asyncio.to_thread(_sync)
                for res in results:
                    url = res.get('href')
                    if url:
                        if ".il" in url.lower() or "israel" in url.lower(): continue
                        await db_manager.client.add_discovered_link(url, source=f"Discovery: {query}")
                        discovered.append(url)
                await asyncio.sleep(5)''')

# 4. get_culture_values
content = content.replace('''            with DDGS() as ddgs:
                results = list(ddgs.text(f"{company} mission values culture", max_results=3))
                if results:
                    return f"Values Found: {' '.join([r['body'][:100] for r in results])}"''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(f"{company} mission values culture", max_results=3))
            results = await asyncio.to_thread(_sync)
            if results:
                return f"Values Found: {' '.join([r['body'][:100] for r in results])}"''')

# 5. get_competitor_disruption
content = content.replace('''            with DDGS() as ddgs:
                results = list(ddgs.text(f"{company} top competitors", max_results=2))
                rival = "a top competitor"
                if results: 
                    rival = results[0]['title'].split()[0]
                
                fail_res = list(ddgs.text(f"{rival} layoff or failure or lawsuit 2024", max_results=1))
                if fail_res:
                    return f"{rival} recently faced: {fail_res[0]['title']}"''', '''            def _sync_comp():
                with DDGS() as ddgs: return list(ddgs.text(f"{company} top competitors", max_results=2))
            results = await asyncio.to_thread(_sync_comp)
            rival = "a top competitor"
            if results: rival = results[0]['title'].split()[0]
            def _sync_fail(r=rival):
                with DDGS() as ddgs: return list(ddgs.text(f"{r} layoff or failure or lawsuit 2024", max_results=1))
            fail_res = await asyncio.to_thread(_sync_fail)
            if fail_res:
                return f"{rival} recently faced: {fail_res[0]['title']}"''')

# 6. get_internal_lingo
content = content.replace('''            with DDGS() as ddgs:
                results = list(ddgs.text(f"site:glassdoor.com \\"{company}\\" interview questions culture", max_results=3))
                if results:
                    return f"Lingo Tags: {' '.join([r['body'][:50] for r in results])}"''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(f"site:glassdoor.com \\"{company}\\" interview questions culture", max_results=3))
            results = await asyncio.to_thread(_sync)
            if results:
                return f"Lingo Tags: {' '.join([r['body'][:50] for r in results])}"''')

# 7. get_leadership_team
content = content.replace('''            with DDGS() as ddgs:
                results = list(ddgs.text(f"{company} board of directors leadership team names", max_results=3))
                if results:
                    return ", ".join([r['title'].split("-")[0].strip() for r in results[:2]])''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(f"{company} board of directors leadership team names", max_results=3))
            results = await asyncio.to_thread(_sync)
            if results:
                return ", ".join([r['title'].split("-")[0].strip() for r in results[:2]])''')

# 8. get_recruiter_info
content = content.replace('''            with DDGS() as ddgs:
                query = f"{company} {job_title} recruiter linkedin"
                results = list(ddgs.text(query, max_results=3))
                if results:
                    best = results[0]
                    # Logic to extract name from title: "John Doe - Talent Acquisition - LinkedIn"
                    name_raw = best['title'].split("-")[0].split("|")[0].strip()
                    return {
                        "name": name_raw,
                        "url": best['href']
                    }''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(f"{company} {job_title} recruiter linkedin", max_results=3))
            results = await asyncio.to_thread(_sync)
            if results:
                best = results[0]
                name_raw = best['title'].split("-")[0].split("|")[0].strip()
                return {"name": name_raw, "url": best['href']}''')

# 9. hunt_expansion_signals
content = content.replace('''            with DDGS() as ddgs:
                queries = [
                    'site:crunchbase.com "raised funding" 2024',
                    'site:globenewswire.com "new headquarters" 2024',
                    'startup "received seed funding" "Riyadh"',
                    'company "expanding office" "Dubai"',
                    '"new office opening" "London" 2024'
                ]
                for query in queries:
                    results = list(ddgs.text(query, max_results=5))
                    for r in results:
                        # Extract company name from title
                        company_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', r['title'])
                        if company_match:
                            company = company_match.group(1)
                            leads.append({
                                "company_name": company,
                                "job_title": "Strategic Operations Lead", # Predictive targeting
                                "email": f"hr@{company.lower().replace(' ', '')}.com", # Guess
                                "description": r['body'],
                                "link": r['href'],
                                "mission_type": "PRE_HIRING_SIGNAL",
                                "location": "Global Focus",
                                "platform": "expansion_recon"
                            })''', '''            queries = [
                'site:crunchbase.com "raised funding" 2024',
                'site:globenewswire.com "new headquarters" 2024',
                'startup "received seed funding" "Riyadh"',
                'company "expanding office" "Dubai"',
                '"new office opening" "London" 2024'
            ]
            for query in queries:
                def _sync(q=query):
                    with DDGS() as ddgs: return list(ddgs.text(q, max_results=5))
                results = await asyncio.to_thread(_sync)
                for r in results:
                    company_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', r['title'])
                    if company_match:
                        company = company_match.group(1)
                        leads.append({
                            "company_name": company,
                            "job_title": "Strategic Operations Lead",
                            "email": f"hr@{company.lower().replace(' ', '')}.com",
                            "description": r['body'],
                            "link": r['href'],
                            "mission_type": "PRE_HIRING_SIGNAL",
                            "location": "Global Focus",
                            "platform": "expansion_recon"
                        })''')

# 10. hunt_registered_platforms
content = content.replace('''                    with DDGS() as ddgs:
                        results = list(ddgs.text(q, max_results=10))
                        for r in results:
                            all_leads.append({
                                "company_name": "Automatic Target",
                                "job_title": r['title'],
                                "url": r['href'],
                                "email": None, # Will be sniped later
                                "source": platform['name']
                            })''', '''                    def _sync(qu=q):
                        with DDGS() as ddgs: return list(ddgs.text(qu, max_results=10))
                    results = await asyncio.to_thread(_sync)
                    for r in results:
                        all_leads.append({
                            "company_name": "Automatic Target",
                            "job_title": r['title'],
                            "url": r['href'],
                            "email": None,
                            "source": platform['name']
                        })''')

# 11. resolve_manager_name
content = content.replace('''            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if results:
                    text = " ".join([r['body'] for r in results])
                    match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", text)
                    if match:
                        found_name = match.group(1)
                        logging.info(f"🕵️ IDENTITY FOUND: {found_name} at {company}")
                        return found_name''', '''            def _sync():
                with DDGS() as ddgs: return list(ddgs.text(query, max_results=3))
            results = await asyncio.to_thread(_sync)
            if results:
                text = " ".join([r['body'] for r in results])
                match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", text)
                if match:
                    found_name = match.group(1)
                    logging.info(f"🕵️ IDENTITY FOUND: {found_name} at {company}")
                    return found_name''')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
