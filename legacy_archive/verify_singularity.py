import asyncio
import os
import logging
from core.db_client import RealityShapingDB
from core.ai_agent import OmniIntelligence
from core.scrapers.omni_crawler import OmniCrawler
from core.pdf_generator import create_personalized_pdf

async def verify_singularity():
    logging.info("🌌 PHASE SINGULARITY: SYSTEM ASCENSION AUDIT")
    
    db = RealityShapingDB()
    ai = OmniIntelligence()
    
    # 1. Verify Personality Archetype Sync
    print("\n1. INTELLIGENCE ARCHETYPE CHECK:")
    is_rel, reason, body, salary, score, adv, keywords, persona, variant, archetype = await ai.analyze_job(
        "Founding Ops Lead", 
        "We are a hyper-growth chaos startup looking for a disruptor."
    )
    print(f"   - Detected Archetype: {archetype}")
    print(f"   - Tone Variant: {variant}")
    if "CHAOTIC_STARTUP" in archetype:
        print("   OK: Archetype Mirroring logic verified.")
    else:
        print(f"   WARN: Unexpected Archetype detection: {archetype}")

    # 2. Verify Quantum PDF Evasion (Micro-Kerning)
    print("\n2. QUANTUM PDF EVASION CHECK:")
    lead = {
        "company_name": "Singularity Corp", 
        "job_title": "Infinite God-Tier Lead", 
        "custom_body": "This is a test of pixel-level jitter.",
        "personality_archetype": "VISIONARY_TECH"
    }
    path = create_personalized_pdf(lead)
    if path and os.path.exists(path):
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            content = f.read()
            if b"%%CHRONOS_SIG" in content:
                print(f"   - PDF Path: {path}")
                print(f"   - X-Ref Obfuscation: DETECTED")
                print("   OK: Quantum Evasion verified.")
            else:
                print("   FAIL: X-Ref Obfuscation missing.")

    # 3. Verify Self-Healing Registry
    print("\n3. SELF-HEALING REGISTRY CHECK:")
    await db.save_site_patch("test-broken-site.com", {"title": ".new-title-selector"})
    patch = await db.get_site_patch("test-broken-site.com")
    if patch and patch.get("title") == ".new-title-selector":
        print("   OK: AI Patch Infrastructure operational.")
    else:
        print("   FAIL: Site Patch storage failure.")

    print("\nDONE PHASE SINGULARITY: ASCENSION COMPLETE. System status: LIMITLESS.")

if __name__ == "__main__":
    asyncio.run(verify_singularity())
