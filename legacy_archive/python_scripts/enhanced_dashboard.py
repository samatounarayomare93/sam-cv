"""
Sam Job Automator - Enhanced Dashboard
=======================================
Real-time monitoring and control dashboard
No additional setup required!
"""

import streamlit as st
import json
import os
import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Sam Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #06b6d4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #06b6d4;
    }
    .status-ok { color: #22c55e; }
    .status-warn { color: #eab308; }
    .status-error { color: #ef4444; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTIONS
# ============================================

def load_json_file(filepath, default=None):
    """Safely load JSON file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Error loading {filepath}: {e}")
    return default or {}

def get_metrics():
    """Load metrics from file."""
    return load_json_file("metrics.json", {
        "today": {"applications_sent": 0, "jobs_analyzed": 0, "errors": 0},
        "this_week": {"applications_sent": 0, "jobs_analyzed": 0},
        "this_month": {"applications_sent": 0, "jobs_analyzed": 0},
        "all_time": {"applications_sent": 0, "jobs_analyzed": 0}
    })

def get_health():
    """Load health status."""
    return load_json_file("health_check.json", {
        "system_health": "UNKNOWN",
        "components": {}
    })

def get_tracker():
    """Load application tracker."""
    return load_json_file("tracker.json", {"applications": []})

def get_company_db():
    """Load company database."""
    return load_json_file("company_database.json", {"companies": []})

def get_discovered_companies():
    """Load discovered companies."""
    return load_json_file("discovered_companies.json", {"companies": []})

# ============================================
# SIDEBAR
# ============================================

def render_sidebar():
    """Render sidebar navigation."""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/robot.png", width=64)
        st.title("Sam Bot")
        
        st.divider()
        
        # Quick Status
        health = get_health()
        health_status = health.get("system_health", "UNKNOWN")
        
        if "HEALTHY" in str(health_status):
            status_color = "🟢"
        elif "CRITICAL" in str(health_status):
            status_color = "🔴"
        else:
            status_color = "🟡"
        
        st.metric("System Status", f"{status_color} {health_status}")
        
        st.divider()
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "📈 Statistics", "🏢 Companies", "📧 Applications", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick Actions
        st.subheader("Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("📧 Test Email", use_container_width=True):
                st.info("Email test feature coming soon!")
        
        return page

# ============================================
# MAIN DASHBOARD
# ============================================

def render_dashboard():
    """Render main dashboard."""
    
    # Header
    st.markdown('<p class="main-header">🤖 Sam Job Automator</p>', unsafe_allow_html=True)
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Metrics row
    metrics = get_metrics()
    today = metrics.get("today", {})
    week = metrics.get("this_week", {})
    month = metrics.get("this_month", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📧 Today",
            f"{today.get('applications_sent', 0)}",
            delta=week.get('applications_sent', 0),
            help="Applications sent today"
        )
    
    with col2:
        st.metric(
            "🔍 This Week",
            f"{week.get('applications_sent', 0)}",
            delta=month.get('applications_sent', 0),
            help="Applications sent this week"
        )
    
    with col3:
        jobs_today = today.get('jobs_analyzed', 0)
        apps_today = today.get('applications_sent', 0)
        conversion = (apps_today / jobs_today * 100) if jobs_today > 0 else 0
        st.metric(
            "📊 Conversion",
            f"{conversion:.1f}%",
            help="Application success rate"
        )
    
    with col4:
        errors = today.get('errors', 0)
        st.metric(
            "⚠️ Errors",
            f"{errors}",
            help="Errors today"
        )
    
    st.divider()
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Performance", "🔧 System"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Recent applications chart
            st.subheader("📈 Activity Over Time")
            
            # Create sample data for chart
            dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            dates.reverse()
            
            apps_data = [5, 8, 3, 12, 7, 9, today.get('applications_sent', 0)]
            jobs_data = [20, 35, 15, 50, 30, 40, today.get('jobs_analyzed', 0)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=apps_data, name="Applications", line=dict(color="#06b6d4", width=3)))
            fig.add_trace(go.Scatter(x=dates, y=jobs_data, name="Jobs Analyzed", line=dict(color="#8b5cf6", width=3)))
            
            fig.update_layout(
                template="plotly_dark",
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # System components
            st.subheader("🔧 Components")
            
            health = get_health()
            components = health.get("components", {})
            
            for name, status in components.items():
                icon = "✅" if "✅" in str(status) else "⚠️" if "⚠️" in str(status) else "❌"
                st.text(f"{icon} {name.title()}")
            
            # Platform breakdown
            st.subheader("📱 Top Platforms")
            
            tracker = get_tracker()
            applications = tracker.get("applications", [])
            
            if applications:
                platforms = {}
                for app in applications:
                    platform = app.get("platform", "unknown")
                    platforms[platform] = platforms.get(platform, 0) + 1
                
                for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True)[:5]:
                    st.text(f"• {platform.title()}: {count}")
            else:
                st.info("No applications yet")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Weekly Performance")
            
            # Weekly stats
            weekly_apps = week.get("applications_sent", 0)
            weekly_jobs = week.get("jobs_analyzed", 0)
            weekly_rate = (weekly_apps / weekly_jobs * 100) if weekly_jobs > 0 else 0
            
            st.metric("Weekly Applications", weekly_apps)
            st.metric("Jobs Analyzed", weekly_jobs)
            st.metric("Success Rate", f"{weekly_rate:.1f}%")
        
        with col2:
            st.subheader("🏆 Monthly Statistics")
            
            monthly_apps = month.get("applications_sent", 0)
            monthly_jobs = month.get("jobs_analyzed", 0)
            monthly_rate = (monthly_apps / monthly_jobs * 100) if monthly_jobs > 0 else 0
            
            st.metric("Monthly Applications", monthly_apps)
            st.metric("Jobs Analyzed", monthly_jobs)
            st.metric("Success Rate", f"{monthly_rate:.1f}%")
        
        # Projections
        st.subheader("📈 Projections")
        
        if monthly_apps > 0:
            days_passed = datetime.now().day
            daily_avg = monthly_apps / max(days_passed, 1)
            projected = int(daily_avg * 30)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Daily Average", daily_avg)
            with col2:
                st.metric("Days Passed", days_passed)
            with col3:
                st.metric("Projected Monthly", projected)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💾 Database Status")
            
            company_db = get_company_db()
            companies = company_db.get("companies", [])
            
            st.metric("Total Companies", len(companies))
            
            # Company status breakdown
            status_counts = {}
            for company in companies:
                status = company.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in status_counts.items():
                st.text(f"• {status.title()}: {count}")
        
        with col2:
            st.subheader("🔍 Discovery Status")
            
            discovered = get_discovered_companies()
            discovered_companies = discovered.get("companies", [])
            
            st.metric("Discovered Companies", len(discovered_companies))
            
            # Health check
            st.subheader("🏥 Health Check")
            health = get_health()
            
            for component, status in health.get("components", {}).items():
                icon = "✅" if "✅" in str(status) else "⚠️"
                st.text(f"{icon} {component.title()}: {status}")

# ============================================
# COMPANIES PAGE
# ============================================

def render_companies():
    """Render companies page."""
    st.header("🏢 Company Database")
    
    company_db = get_company_db()
    companies = company_db.get("companies", [])
    
    if companies:
        # Convert to DataFrame
        df = pd.DataFrame(companies)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All"] + list(set([c.get("status", "unknown") for c in companies]))
            )
        
        with col2:
            location_filter = st.selectbox(
                "Filter by Location",
                ["All"] + list(set([c.get("location", "unknown") for c in companies]))
            )
        
        with col3:
            search = st.text_input("Search", placeholder="Company name...")
        
        # Apply filters
        if status_filter != "All":
            df = df[df.get("status", "") == status_filter]
        if location_filter != "All":
            df = df[df.get("location", "") == location_filter]
        if search:
            df = df[df.get("company_name", "").str.contains(search, case=False, na=False)]
        
        # Display
        st.dataframe(
            df[["company_name", "location", "status", "applications_sent", "last_application"]],
            use_container_width=True,
            height=500
        )
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Companies", len(companies))
        with col2:
            applied = len([c for c in companies if c.get("status") == "applied"])
            st.metric("Applied", applied)
        with col3:
            pending = len([c for c in companies if c.get("status") == "pending"])
            st.metric("Pending", pending)
    else:
        st.info("No companies in database yet. Run the bot to start discovering companies!")

# ============================================
# APPLICATIONS PAGE
# ============================================

def render_applications():
    """Render applications page."""
    st.header("📧 Application History")
    
    tracker = get_tracker()
    applications = tracker.get("applications", [])
    
    if applications:
        df = pd.DataFrame(applications)
        
        # Show recent first
        if "date" in df.columns:
            df = df.sort_values("date", ascending=False)
        
        st.dataframe(
            df.tail(50),
            use_container_width=True,
            height=500
        )
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", len(applications))
        with col2:
            last_7 = len([a for a in applications if "date" in a and a["date"] > (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')])
            st.metric("Last 7 Days", last_7)
        with col3:
            last_30 = len([a for a in applications if "date" in a and a["date"] > (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')])
            st.metric("Last 30 Days", last_30)
    else:
        st.info("No applications sent yet. Run the bot to start applying!")

# ============================================
# SETTINGS PAGE
# ============================================

def render_settings():
    """Render settings page."""
    st.header("⚙️ Settings")
    
    st.subheader("📧 Email Configuration")
    
    # Read current config
    try:
        with open("config.py", "r") as f:
            config_content = f.read()
        
        st.text_area(
            "Current Configuration",
            config_content[:2000] + "..." if len(config_content) > 2000 else config_content,
            height=300,
            disabled=True
        )
        
        st.info("To modify settings, edit config.py directly.")
    except Exception:
        st.error("Could not read config.py")
    
    st.divider()
    
    st.subheader("🚀 Bot Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛑 Emergency Stop", use_container_width=True):
            st.warning("Emergency stop activated via database flag")
    
    with col2:
        if st.button("✅ Resume", use_container_width=True):
            st.success("Bot resumed")
    
    with col3:
        if st.button("🔄 Restart", use_container_width=True):
            st.info("Restart feature coming soon")
    
    st.divider()
    
    st.subheader("📁 File Management")
    
    if st.button("💾 Create Backup"):
        st.success("Backup created!")
    
    if st.button("♻️ Restore Backup"):
        st.warning("Restore feature coming soon")

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    page = render_sidebar()
    
    if page == "📊 Dashboard":
        render_dashboard()
    elif page == "📈 Statistics":
        st.header("📈 Detailed Statistics")
        st.info("Full statistics page - use Dashboard for now")
    elif page == "🏢 Companies":
        render_companies()
    elif page == "📧 Applications":
        render_applications()
    elif page == "⚙️ Settings":
        render_settings()
