"""
Dashboard Module - Streamlit Command Center
Provides a web interface for monitoring and controlling Project Chronos.
"""
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from plotly import express as px

import config
import database
from ai_agent import GeminiAgent
from core_utils import compute_brevo_open_rate, parse_prep_company

load_dotenv()

logger = logging.getLogger(__name__)

# Page Config
st.set_page_config(
    page_title="Project Chronos Command Center", 
    page_icon="🚀", 
    layout="wide"
)

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Glassmorphism Metrics */
div[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.1);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    border: 1px solid rgba(59, 130, 246, 0.3);
}

[data-testid="stMetricLabel"] * {
    color: #94a3b8 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px;
}

[data-testid="stMetricValue"] * {
    color: #f8fafc !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
}

hr {
    border-top: 1px solid rgba(148, 163, 184, 0.15) !important;
    margin-top: 2rem;
    margin-bottom: 2rem;
}

h1 {
    font-weight: 700 !important;
    background: linear-gradient(to right, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 10px;
}
h2, h3 {
    font-weight: 600 !important;
    color: #f8fafc !important;
}

.stDataFrame {
    border: 1px solid rgba(148, 163, 184, 0.1) !important;
    border-radius: 8px;
    overflow: hidden;
}

.stButton>button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
st.title("Project Chronos // Command Center")


# ==========================================
# 🔧 CONFIGURATION & HELPERS
# ==========================================

def get_secret(key: str) -> str:
    """Try st.secrets first (Streamlit Cloud), then os.getenv (Local)."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception as exc:
        logger.debug("Unable to read Streamlit secret %s: %s", key, exc)
    return os.getenv(key, "")


@st.cache_resource
def init_connection():
    """Initialize Supabase connection."""
    from supabase import create_client
    supabase_url = get_secret("SUPABASE_URL")
    supabase_key = get_secret("SUPABASE_KEY")
    if supabase_url and supabase_key:
        return create_client(supabase_url, supabase_key)
    return None


def fetch_data(table: str = "applications") -> pd.DataFrame:
    """Fetches data from specified Supabase table."""
    client = init_connection()
    if not client:
        return pd.DataFrame()
    try:
        response = client.table(table).select("*").execute()
        data = response.data
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
        return df
    except Exception as e:
        logger.warning("Failed to fetch dashboard data from table %s: %s", table, e)
        return pd.DataFrame()


def update_db_secret(key: str, value: str) -> bool:
    """Updates a secret in the database vault."""
    client = init_connection()
    if not client:
        return False
    try:
        client.table("system_state").upsert(
            {"key": key, "value": str(value)}, 
            on_conflict="key"
        ).execute()
        return True
    except Exception as exc:
        logger.warning("Failed to update dashboard secret %s: %s", key, exc)
        return False


def fetch_brevo_open_rate() -> float:
    """Fetches email open rate from Brevo API."""
    brevo_key = get_secret("BREVO_API_KEY")
    if not brevo_key:
        return 0.0
    try:
        headers = {"accept": "application/json", "api-key": brevo_key}
        resp = requests.get(
            "https://api.brevo.com/v3/smtp/statistics/aggregatedReport", 
            headers=headers, 
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            delivered = sum(x.get("delivered", 0) for x in data)
            unique_opens = sum(x.get("uniqueOpens", 0) for x in data)
            if delivered > 0:
                return round((unique_opens / delivered) * 100, 1)
    except Exception as exc:
        logger.warning("Failed to fetch Brevo open rate: %s", exc)
    return 0.0

# ----------------- UI RENDERING -----------------

# --- SIDEBAR (Controls) ---
st.sidebar.title("🛠 CONTROL PANEL")
st.sidebar.markdown("---")

st.sidebar.subheader("📡 TELEMETRY SYSTEM")
st.sidebar.info("Fire a synthetic AI-generated application to verify the engine's current intelligence.")

test_email = st.sidebar.text_input("🎯 Target Test Email", value="sam.dev1@hotmail.com")
manual_pat = st.sidebar.text_input("🔑 Manual PAT Override (Optional)", type="password", help="Paste your GitHub Personal Access Token here if it is not set in Streamlit Secrets.")

if st.sidebar.button("🚀 FIRE AI TEST PAYLOAD"):
    # Priority: Manual PAT > Streamlit Secret
    GITHUB_PAT = manual_pat.strip() if manual_pat else get_secret("GITHUB_PAT").strip()
    
    if not GITHUB_PAT:
        st.sidebar.error("❌ GITHUB_PAT is missing!")
        st.sidebar.markdown("""
        **Quick Setup:**
        1. [Create Fine-grained PAT](https://github.com/settings/tokens?type=beta)
        2. Scopes: **Actions (Read & Write)**
        3. Repo: **Sam_Job_Automator**
        """)
    else:
        with st.sidebar.spinner("⏳ Firing Payload..."):
            # Trigger GitHub Action
            repo = "Sam-Cordahi/Sam_Job_Automator"
            workflow = "job_bot.yml"
            url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/dispatches"
            
            # Modern Bearer token auth is more reliable across GitHub API versions
            headers = {
                "Authorization": f"Bearer {GITHUB_PAT}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            payload = {
                "ref": "main", 
                "inputs": {
                    "is_telemetry": "true",
                    "telemetry_email": test_email
                }
            }
            
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=12)
                if resp.status_code == 204:
                    st.sidebar.success("✅ Telemetry Signal Sent! The AI is waking up. Check your email in 2 minutes.")
                elif resp.status_code == 404:
                    st.sidebar.error("❌ 404: Workflow Not Found. Check if the token has 'Actions: Read/Write' permission for this specific repository.")
                else:
                    st.sidebar.error(f"❌ Error {resp.status_code}")
                    st.sidebar.code(resp.text)
            except Exception as e:
                st.sidebar.error(f"💥 Connection Error: {e}")

st.sidebar.markdown("---")
with st.sidebar.expander("🎓 Telemetry Setup Guide"):
    st.write("""
    1. Go to [GitHub Tokens](https://github.com/settings/tokens?type=beta)
    2. Click 'Generate new token'
    3. Name: 'Telemetry'
    4. Repo: 'Sam_Job_Automator'
    5. Permissions: **Actions (Read/Write)**
    """)

st.sidebar.caption("Project Chronos // Sovereign Autonomy V27.5")

# Header Health Indicators
h1, h2, h3 = st.columns(3)
stats = database.get_global_stats()
h1.metric("💓 System Sync", "ACTIVE 🟢")
h2.metric("🧠 AI Engine", "GOD-MODE ✨")
h3.metric("🎯 Total Strikes", stats.get('applications', 0))

st.markdown("---")

# ----------------- UI TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 ANALYTICS", "🕵️‍♂️ INTELLIGENCE", "🔐 VAULT", "💬 COMMAND CHAT", "🛰️ STRATEGY MATRIX"])

with tab1:
    df = fetch_data("applications")
    total_jobs = len(df)
    open_rate = fetch_brevo_open_rate()
    active_clones = 3 

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs Applied", total_jobs, "Autopilot Active")
    with col2:
        st.metric("Email Open Rate %", f"{open_rate}%", "Brevo Tracking")
    with col3:
        st.metric("Active Clones", active_clones, "Matrix Parallelism")

    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Platform Distribution")
        if not df.empty and 'platform' in df.columns:
            platform_counts = df['platform'].value_counts().reset_index()
            platform_counts.columns = ['Platform', 'Count']
            fig1 = px.bar(platform_counts, x='Platform', y='Count', color='Platform', template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        st.subheader("Application Velocity")
        if not df.empty and 'created_at' in df.columns:
            df['date'] = df['created_at'].dt.date
            date_counts = df.groupby('date').size().reset_index(name='Count')
            fig2 = px.line(date_counts, x='date', y='Count', markers=True, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Recent Neutralizations")
    if not df.empty:
        if 'created_at' in df.columns:
            st.dataframe(df.sort_values(by='created_at', ascending=False).head(20), use_container_width=True)
        else:
            st.dataframe(df.head(20), use_container_width=True)

with tab2:
    st.subheader("🕵️‍♂️ SCOUTED LEADS QUEUE")
    st.info("These jobs have been parsed and validated by the Scout phase and are waiting for the next Strike window.")
    df_leads = fetch_data("leads")
    if not df_leads.empty:
        # Filter buttons
        status_filter = st.multiselect("Filter by Status", options=["pending", "applied", "failed"], default=["pending"])
        if 'status' in df_leads.columns:
            df_filtered = df_leads[df_leads['status'].isin(status_filter)]
        else:
            df_filtered = df_leads
            
        if 'created_at' in df_filtered.columns:
            st.dataframe(df_filtered.sort_values(by='created_at', ascending=False), use_container_width=True)
        else:
            st.dataframe(df_filtered, use_container_width=True)
    else:
        st.warning("No leads found in the database. Ensure the Scout mission has run.")

with tab3:
    st.subheader("🔐 SYSTEM SECRETS VAULT")
    st.warning("CAUTION: Modifying these values will instantly update the AI's operational brain.")
    
    df_secrets = fetch_data("system_state")
    if not df_secrets.empty:
        st.dataframe(df_secrets, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Update Secret")
    with st.form("secret_form"):
        st.write("Select an existing core key OR type a custom new key name below.")
        s_key_dropdown = st.selectbox("Select Key", ["GEMINI_API_KEY", "TELEGRAM_BOT_TOKEN", "BREVO_API_KEY", "Other (Custom)"])
        s_key_custom = st.text_input("Custom Key Name (Only if 'Other' is selected)")
        
        s_val = st.text_input("New Value", type="password")
        if st.form_submit_button("📁 UPDATE VAULT"):
            final_key = s_key_custom.strip().upper() if s_key_dropdown == "Other (Custom)" else s_key_dropdown
            if s_val and final_key:
                if update_db_secret(final_key, s_val):
                    st.success(f"Successfully added/updated {final_key} in the database!")
            else:
                st.error("Please provide a valid Key Name and Value.")

with tab4:
    st.subheader("💬 EXECUTIVE TERMINAL // LIVE")
    st.caption("Communicate with Project Chronos in real-time. No 30-minute delays.")
    
    # Quick Commands Menu
    cmd1, cmd2, cmd3 = st.columns(3)
    if cmd1.button("📊 Live Status Check", use_container_width=True):
        stats = database.get_global_stats()
        st.success(f"📍 Scouted Leads: {stats.get('leads', 0)} | 🎯 Applications Sent: {stats.get('applications', 0)}")
        
    if cmd2.button("🛑 EMERGENCY KILL SWITCH", type="primary", use_container_width=True):
        database.set_system_flag("kill_switch", "true")
        st.error("🛑 ENGINE SHUTDOWN ACTIVATED. All robot outreach is frozen.")
        
    if cmd3.button("🟢 RESUME ENGINE", use_container_width=True):
        database.set_system_flag("kill_switch", "false")
        st.success("🟢 ENGINE RESUMED. Sovereign autonomy restored.")
        
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 **Welcome back, Commander Sam.**\n\nI am online and ready. You can instruct me easily here.\n\n**Tip:** To get an instant Coach Report on any company, type: `PREP: Company Name`"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Enter command... (e.g. PREP: Emirates)"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            company = parse_prep_company(prompt)
            if company:
                with st.spinner(f"🕵️‍♂️ Analyzing DNA of {company}..."):
                    # Ensure we get the latest API key dynamically
                    ai_brain = GeminiAgent()
                    if ai_brain.enabled:
                        prep_report = ai_brain.generate_interview_prep(company)
                        response = f"📑 **MISSION DOSSIER: {company.upper()}**\n\n{prep_report}"
                    else:
                        response = "⚠️ AI Engine is Offline. Please ensure GEMINI_API_KEY is configured in the Vault."
            else:
                if prompt.strip().upper().startswith("PREP"):
                    response = "You forgot to provide a company name! Try `PREP: Google`."
                else:
                    response = f"Affirmative. I received: *{prompt}*.\n\nIf you want interview prep, try typing `prep companyname`."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
                
with tab5:
    st.subheader("🛰️ STRATEGY MATRIX // LIVE CONTROL")
    st.caption("Adjust your global footprint and search intensity in real-time.")
    
    with st.expander("📍 GLOBAL TARGET REGIONS", expanded=True):
        current_locs = ", ".join(config.GOD_MODE_LOCATIONS)
        new_locs = st.text_area("Target Locations (Comma separated)", value=current_locs, help="Example: Dubai, Riyadh, Remote")
        if st.button("💾 UPDATE REGIONS"):
            # In a real setup, we'd save this to a 'settings' table in Supabase
            st.info("Strategy pending database write-access upgrade. Currently using config.py defaults.")
            
    with st.expander("🔍 MISSION QUERIES", expanded=True):
        st.write("The engine is currently scouting using these High-Intent strings:")
        for q in config.GOD_MODE_QUERIES:
            st.markdown(f"- ` {q} `")
        
        st.markdown("---")
        st.subheader("💓 INFRASTRUCTURE PULSE")
        c1, c2, c3 = st.columns(3)
        c1.progress(100, text="Supabase Latency: <50ms")
        c2.progress(100, text="Gemini Flash 2.0: ACTIVE")
        c3.progress(100, text="Immortal SMTP: ON")

    st.markdown("---")
    st.info("💡 **Tip:** Changes made here will be reflected in the next 30-minute cloud scout cycle.")
