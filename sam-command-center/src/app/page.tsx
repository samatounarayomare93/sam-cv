'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import styles from './page.module.css';
import { Activity, Target, Zap, Waves, Terminal as TerminalIcon } from 'lucide-react';

export default function Home() {
  const [stats, setStats] = useState({
    nodes: 0,
    leads: 0,
    strikes: 0,
    heals: 0
  });
  const [logs, setLogs] = useState<any[]>([]);
  const [missions, setMissions] = useState<any[]>([]);
  const [isPulsing, setIsPulsing] = useState(false);
  const [hoveredDescription, setHoveredDescription] = useState<string | null>(null);

  const buttonDescriptions: Record<string, string> = {
    "Status": "Live heartbeat and operational state of the Intelligence Swarm.",
    "Tasks": "Neural queue of pending missions and strike schedules.",
    "Shield": "Visualizes Evasion Tier, Proxy mesh health, and Blacklist status.",
    "Run Now": "Emergency strike package: Bypasses human-jitter constraints.",
    "Stats": "Conversion metrics, success rates, and empire growth telemetry.",
    "Leads": "Feed of the most lucrative and high-probability job targets discovered.",
    "Pulse": "Real-time system telemetry and raw neural processing logs.",
    "Prep": "AI Interview Coach: STAR-method training and salary negotiation.",
    "Campaign": "Deep-crawl mission: Scans 50+ sources for global dominance.",
    "Follow-up": "Automated persistence: Neural reminders sent to pending recruiters.",
    "Companies": "Global intelligence database of all encountered entities.",
    "Settings": "Override Deck: Configure rate limits, AI creativity, and proxy tiers.",
    "Pause": "HALT: Temporarily freeze all non-essential swarm activity.",
    "Resume": "IGNITION: Rekindle the eternal job hunt cycle immediately.",
    "Track": "RECON: Manual injection of high-value targets for immediate strike.",
    "Omega Halt": "FALLBACK: Emergency full-system shutdown and mission scrub."
  };

  const fetchStats = async () => {
    // 🕵️ OMNISCIENT: Fetch live telemetry
    const { count: leadCount } = await supabase.from('leads').select('*', { count: 'exact', head: true });
    const { count: appCount } = await supabase.from('applications').select('*', { count: 'exact', head: true });
    const { count: nodeCount } = await supabase.from('nodes').select('*', { count: 'exact', head: true });
    const { count: patchCount } = await supabase.from('site_patches').select('*', { count: 'exact', head: true });

    setStats({
      nodes: nodeCount || 0,
      leads: leadCount || 0,
      strikes: appCount || 0,
      heals: patchCount || 0
    });
    
    // ⚡ ZENITH: Fetch latest SYSTEM logs for the Live Terminal
    const { data: latestLogs } = await supabase
      .from('system_logs')
      .select('*')
      .order('timestamp', { ascending: false })
      .limit(10);
      
    if (latestLogs && latestLogs.length > 0) {
      if (logs.length > 0 && latestLogs[0].timestamp !== logs[0].timestamp) {
        setIsPulsing(true);
        setTimeout(() => setIsPulsing(false), 2000);
      }
      setLogs(latestLogs);
    }

    // 🧠 NEURAL: Fetch pending missions
    const { data: activeMissions } = await supabase
      .from('tasks')
      .select('*')
      .eq('status', 'PENDING')
      .order('created_at', { ascending: false });
    
    if (activeMissions) setMissions(activeMissions);
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000); // 5s heartbeat for true live feel
    return () => clearInterval(interval);
  }, []);

  const completeMission = async (id: number, recruiterUrl: string | null, message: string) => {
    // 🚀 ZENITH: ZERO-CLICK EXECUTION
    if (recruiterUrl) {
      window.open(recruiterUrl, '_blank');
    }
    
    // Copy nudge to clipboard
    const nudge = message.includes('Nudge: ') ? message.split('Nudge: ')[1] : message;
    await navigator.clipboard.writeText(nudge);
    
    // Mark as completed in Hive-Mind
    await supabase.from('tasks').update({ status: 'COMPLETED' }).eq('id', id);
    fetchStats();
    alert('Mission Initialized: Profile opened and Nudge copied to clipboard.');
  };

  return (
    <main className={styles.main}>
      {/* Navigation / Header */}
      <nav className={`${styles.nav} glass-panel`}>
        <div className={styles.logo}>
          <span className={styles.rc}>RC</span>
          <span className={styles.title}>Project Chronos <br/><small className="text-gradient">God Mode Command Center</small></span>
        </div>
        <div className={styles.navLinks}>
          <button className="btn-glass">Live Terminal</button>
          <button className="btn-glow">Node Control</button>
        </div>
      </nav>

      {/* Hero Analytics */}
      <header className={styles.hero}>
        <h1 className="text-gradient animate-float">Global Intelligence Hub</h1>
        <p className={styles.subtitle}>Real-time telemetry for the OMNISCIENT Decentralized Swarm.</p>
      </header>

      {/* 🌌 ZENITH: GLOBAL STRIKE RADAR [INFINITE ASCENSION] */}
      <section className={styles.missionDeck}>
        <div className={styles.deckHeader}>
          <h2>Sovereign Mission Deck</h2>
          <div className={`${styles.tooltipArea} ${hoveredDescription ? styles.active : ''}`}>
             {hoveredDescription ? `⚡ [INTEL]: ${hoveredDescription}` : '📡 PASS MOUSE OVER BUTTONS FOR SYSTEM TELEMETRY'}
          </div>
        </div>
        
        <div className={styles.buttonGrid}>
          {Object.keys(buttonDescriptions).map((btn) => (
            <button 
              key={btn}
              className="btn-glass"
              onMouseEnter={() => setHoveredDescription(buttonDescriptions[btn])}
              onMouseLeave={() => setHoveredDescription(null)}
            >
              {btn}
            </button>
          ))}
        </div>
      </section>

      {/* Hero Analytics */}
      <section className={`${styles.radarSection} glass-panel`}>
        <div className={`${styles.radarContainer} ${isPulsing ? styles.activePulse : ''}`}>
          <div className={styles.radarSweep}></div>
          <div className={styles.radarGrid}></div>
          <div className={`${styles.radarPoint} ${styles.p1}`}></div>
          <div className={`${styles.radarPoint} ${styles.p2}`}></div>
          <div className={`${styles.radarPoint} ${styles.p3}`}></div>
          <div className={styles.radarCore}>
            <Activity size={32} className="text-gradient" />
            <span className={styles.radarLabel}>SWARM ACTIVE</span>
          </div>
        </div>
        <div className={styles.radarStats}>
          <h2 className="text-gradient">Sovereign Presence: ACTIVE</h2>
          <p>Scanning for strategic opportunities across 12 sectors...</p>
          <div className={styles.radarMeta}>
            <span>Lat: 33.8938° N</span>
            <span>Lon: 35.5018° E</span>
            <span>Alti: ASCENDING</span>
          </div>
        </div>
      </section>

      {/* Dashboard Grid */}
      <div className={styles.grid}>
        <div className={`${styles.card} glass-panel`}>
          <div className={styles.cardHeader}>
            <div className={styles.pulseIndicator}></div>
            <Activity className="card-icon" />
            <h3>Active Swarm Nodes</h3>
          </div>
          <div className={styles.statGroup}>
            <span className={styles.statValue}>{stats.nodes || 1}</span>
            <span className={styles.statLabel}>Syncing EU & MENA</span>
          </div>
        </div>

        <div className={`${styles.card} glass-panel`}>
          <div className={styles.cardHeader}>
            <div className={`${styles.pulseIndicator} ${styles.blue}`}></div>
            <Target className="card-icon" />
            <h3>Sovereign Leads</h3>
          </div>
          <div className={styles.statGroup}>
            <span className={styles.statValue}>{stats.leads}</span>
            <span className={styles.statLabel}>Verified Targets</span>
          </div>
        </div>

        <div className={`${styles.card} glass-panel`}>
          <div className={styles.cardHeader}>
            <div className={`${styles.pulseIndicator} ${styles.purple}`}></div>
            <Zap className="card-icon" />
            <h3>Command Strikes</h3>
          </div>
          <div className={styles.statGroup}>
            <span className={styles.statValue}>{stats.strikes}</span>
            <span className={styles.statLabel}>Portfolios Delivered</span>
          </div>
        </div>

        <div className={`${styles.card} glass-panel`}>
          <div className={styles.cardHeader}>
            <div className={`${styles.pulseIndicator} ${styles.pink}`}></div>
            <Waves className="card-icon" />
            <h3>Regenerative Heals</h3>
          </div>
          <div className={styles.statGroup}>
            <span className={styles.statValue}>{stats.heals}</span>
            <span className={styles.statLabel}>Automated Scraper Repairs</span>
          </div>
        </div>
      </div>

      {/* 🧠 MISSION BOARD: High-Priority Neural Connection Tasks */}
      <section className={styles.missionSection}>
        <h2 className="section-title">Manual Missions Required <small>(Click to Execute)</small></h2>
        <div className={styles.missionGrid}>
          {missions.length > 0 ? missions.map((m) => {
            const recruiterUrl = m.message.includes('URL: ') ? m.message.split('\n')[0].replace('URL: ', '') : null;
            return (
              <div key={m.id} className={`${styles.missionCard} glass-panel animate-slide-in`}>
                <div className={styles.mHeader}>
                  <span className={styles.mType}>{m.type}</span>
                  <span className={styles.mTarget}>{m.target}</span>
                </div>
                <p className={styles.mMeta}>{m.message.split('Nudge: ')[1] || m.message}</p>
                <div className={styles.mActions}>
                  <button onClick={() => completeMission(m.id, recruiterUrl, m.message)} className="btn-glow-small">Confirm Deployment</button>
                </div>
              </div>
            );
          }) : (
            <div className={`${styles.missionCard} glass-panel empty-state`}>
              <p>No manual connection tasks currently logged by the Neural engine.</p>
            </div>
          )}
        </div>
      </section>

      {/* Live Terminal Log */}
      <section className={`${styles.terminal} glass-panel`}>
        <div className={styles.terminalHeader}>
          <div className={styles.macControls}>
            <span></span><span></span><span></span>
          </div>
          <div className={styles.terminalTitle}>engine.log — zsh</div>
          <TerminalIcon size={14} className="terminal-icon" />
        </div>
        <div className={styles.terminalBody}>
          {logs.length > 0 ? logs.map((log, i) => (
            <p key={i}>
              <span className={styles.tTime}>[{new Date(log.timestamp).toLocaleTimeString()}]</span> 
              <span className={log.level === 'ERROR' ? styles.tError : styles.tSuccess}> {log.level}</span> 📡 
              {log.message}
            </p>
          )) : (
            <p>Initializing Heartbeat... Waiting for next strike signal.</p>
          )}
        </div>
      </section>

    </main>
  );
}
