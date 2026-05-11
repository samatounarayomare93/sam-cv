import os
from dotenv import load_dotenv
load_dotenv()
keys = ['OPENROUTER_API_KEY', 'HUGGINGFACE_API_KEY', 'DEEPSEEK_API_KEY']
for k in keys:
    v = os.getenv(k, '')
    status = (v[:15] + "...") if v else "NOT SET"
    print(f"{k}: {status}")
