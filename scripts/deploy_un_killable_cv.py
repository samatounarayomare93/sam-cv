import os
import subprocess
import logging
import random
import string
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [MIRROR] %(levelname)s - %(message)s")

def generate_ghost_domain() -> str:
    """Generates a random, high-entropy subdomain."""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"sam-impact-{random_str}.surge.sh"

def deploy_to_surge(file_path: str) -> List[str]:
    """
    [🕵️ PHASE MIRROR: THE ETERNAL CV]
    Deploys the CV to multiple un-killable Surge mirrors.
    Uses 'npx surge' to avoid global installation requirements.
    """
    if not os.path.exists(file_path):
        logging.error(f"FATAL: {file_path} not found. Cannot mirror.")
        return []

    deployed_urls = []
    
    # We create 3 different mirrors for absolute redundancy
    for _ in range(3):
        domain = generate_ghost_domain()
        logging.info(f"🚀 MIRROR: Deploying to {domain}...")
        
        try:
            # We use --project for the folder and --domain for the target
            # Surge expects a folder, so we copy the CV to a temp folder
            temp_dir = "temp_mirror"
            os.makedirs(temp_dir, exist_ok=True)
            # Surge needs index.html by default
            target_file = os.path.join(temp_dir, "index.html")
            import shutil
            shutil.copy2(file_path, target_file)
            
            cmd = f"npx surge {temp_dir} {domain}"
            # Note: This might require INTERACTIVE approval the first time, 
            # but we'll try to execute it as a background process.
            subprocess.run(cmd, shell=True, check=True, timeout=60)
            
            deployed_urls.append(f"https://{domain}")
            logging.info(f"✅ MIRROR: Successfully deployed to https://{domain}")
            
        except Exception as e:
            logging.error(f"Mirror deployment to {domain} failed: {e}")

    return deployed_urls

if __name__ == "__main__":
    cv_path = "Sam_Cordahi_CV.html"
    urls = deploy_to_surge(cv_path)
    if urls:
        print("\n".join(urls))
