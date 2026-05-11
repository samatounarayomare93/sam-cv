'use client';

import { useEffect, useState, useCallback } from 'react';
import { supabase } from '@/lib/supabase';
import styles from './page.module.css';
import { Activity, Target, Zap, Waves, Terminal as TerminalIcon } from 'lucide-react';

type ToastType = 'success' | 'error' | 'info';

export default function Home() {
  const [stats, setStats] = useState({ nodes: 0, leads: 0, strikes: 0, heals: 0 });
  const [logs, setLogs] = useState<any[]>([]);
  const [missions, setMissions] = useState<any[]>([]);
  const [isPulsing, setIsPulsing] = useState(false);
  const [hoveredDescription, setHoveredDescription] = useState<string | null>(null);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);
  const [loadingBtn, setLoadingBtn] = useState<string | null>(null);
  const [killSwitchActive, setKillSwitchActive] = useState(false);

  // ── Toast helper ──────────────────────────────────────────
  const showToast = (msg: string, type: ToastType = 'info') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  };

  // ── Button descriptions ───────────────────────────────────
  const buttonDescriptions: Record<string, string> = {
    "Status":     "Live heartbeat and operational state of the Intelligence Swarm.",
    "Tasks":      "Neural queue of pending missions and strike schedules.",
    "Shield":     "Visualizes Evasion Tier, Proxy mesh health, and Blacklist status.",
    "Run Now":    "Emergency strike package: Bypasses human-jitter constraints.",
    "Stats":      "Conversion metrics, success rates, and empire growth telemetry.",
    "Leads":      "Feed of the most lucrative and high-probability job targets discovered.",
    "Pulse":      "Real-time system telemetry and raw neural processing logs.",
    "Prep":       "AI Interview Coach: STAR-method training and salary negotiation.",
    "Campaign":   "Deep-crawl mission: Scans 50+ sources for global dominance.",
    "Follow-up":  "Automated persistence: Neural reminders sent to pending recruiters.",
    "Companies":  "Global intelligence database of all encountered entities.",
    "Settings":   "Override Deck: Configure rate limits, AI creativity, and proxy tiers.",
    "Pause":      "HALT: Temporarily freeze all non-essential swarm activity.",
    "Resume":     "IGNITION: Rekindle the eternal job hunt cycle immediately.",
    "Track":      "RECON: Manual injection of high-value targets for immediate strike.",
    "Omega Halt": "FALLBACK: Emergency full-system shutdown and mission scrub.",
  };

  // ── Fetch live stats ──────────────────────────────────────
  const fetchStats = useCallback(async () => {
    try {
      const [
        { count: leadCount },
        { count: appCount },
        { count: nodeCount },
        { count: patchCount },
        { data: latestLogs },
        { data: activeMissions },
        { data: killData },
      ] = await Promise.all([
        supabase.from('leads').select('*', { count: 'exact', head: true }),
        supabase.from('applications').select('*', { count: 'exact', head: true }),
        supabase.from('nodes').select('*', { count: 'exact', head: true }),
        supabase.from('site_patches').select('*', { count: 'exact', head: true }),
        supabase.from('system_logs').select('*').order('timestamp', { ascending: false }).limit(12),
        supabase.from('tasks').select('*').eq('status', 'PENDING').order('created_at', { ascending: false }),
        supabase.from('system_settings').select('value').eq('key', 'kill_switch').limit(1),
      ]);

      setStats({ nodes: nodeCount || 0, leads: leadCount || 0, strikes: appCount || 0, heals: patchCount || 0 });

      if (latestLogs && latestLogs.length > 0) {
        setLogs(prev => {
          if (prev.length > 0 && latestLogs[0].timestamp !== prev[0].timestamp) {
            setIsPulsing(true);
            setTimeout(() => setIsPulsing(false), 2000);
          }
          return latestLogs;
        });
      }

      if (activeMissions) setMissions(activeMissions);

      // Sync kill switch state
      if (killData && killData.length > 0) {
        setKillSwitchActive(killData[0].value === 'true');
      }
    } catch (err) {
      console.error('fetchStats error:', err);
    }
  }, []);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, [fetchStats]);

  // ── Supabase action helper ────────────────────────────────
  const setSetting = async (key: string, value: string) => {
    const { error } = await supabase
      .from('system_settings')
      .upsert({ key, value, updated_at: new Date().toISOString() }, { onConflict: 'key' });
    if (error) throw error;
  };

  const addTask = async (type: string, target: string, meta: string = '') => {
    const { error } = await supabase
      .from('tasks')
      .insert({ type, target, meta, status: 'PENDING', created_at: new Date().toISOString() });
    if (error) throw error;
  };

  // ── Button action handlers ────────────────────────────────
  const handleButtonClick = async (btn: string) => {
    setLoadingBtn(btn);
    try {
      switch (btn) {
        case 'Pause':
          await setSetting('kill_switch', 'true');
          await setSetting('kill_switch_active', 'true');
          setKillSwitchActive(true);
          showToast('⏸️ Bot PAUSED — applications stopped', 'info');
          break;

        case 'Resume':
          await setSetting('kill_switch', 'false');
          await setSetting('kill_switch_active', 'false');
          setKillSwitchActive(false);
          showToast('▶️ Bot RESUMED — applications running!', 'success');
          break;

        case 'Omega Halt':
          if (!confirm('⚠️ OMEGA HALT: This will stop ALL operations. Are you sure?')) break;
          await setSetting('kill_switch', 'true');
          await setSetting('kill_switch_active', 'true');
          setKillSwitchActive(true);
          showToast('🛑 OMEGA HALT engaged — all operations stopped', 'error');
          break;

        case 'Run Now':
          await setSetting('kill_switch', 'false');
          await setSetting('kill_switch_active', 'false');
          await addTask('FORCE_RUN', 'IMMEDIATE_STRIKE', 'dashboard_trigger');
          setKillSwitchActive(false);
          showToast('🚀 Emergency strike queued — bot running now!', 'success');
          break;

        case 'Status':
          await fetchStats();
          showToast(`📊 Status refreshed — ${stats.strikes} total strikes, ${stats.leads} leads`, 'info');
          break;

        case 'Stats':
          await fetchStats();
          showToast(`📈 Stats: ${stats.strikes} applications sent, ${stats.leads} leads discovered`, 'info');
          break;

        case 'Tasks':
          await fetchStats();
          showToast(`🧬 ${missions.length} pending tasks in queue`, 'info');
          break;

        case 'Leads':
          await fetchStats();
          showToast(`🎯 ${stats.leads} verified leads in database`, 'info');
          break;

        case 'Campaign':
          await addTask('DEEP_CRAWL', 'ALL_SOURCES', 'dashboard_campaign');
          showToast('🌍 Deep-crawl campaign queued — scanning 50+ sources', 'success');
          break;

        case 'Follow-up':
          await addTask('FOLLOW_UP_SWEEP', 'ALL_PENDING', 'dashboard_followup');
          showToast('🔁 Follow-up sweep queued — nudging pending recruiters', 'success');
          break;

        case 'Track':
          const target = prompt('Enter company name or email to track:');
          if (target) {
            await addTask('TRACK_TARGET', target, 'dashboard_track');
            showToast(`🛰️ Tracking queued for: ${target}`, 'success');
          }
          break;

        case 'Shield':
          showToast('🛡️ Shield active — proxy mesh and anti-ban protection running', 'info');
          break;

        case 'Pulse':
          await fetchStats();
          showToast(`💓 System pulse: ${logs.length > 0 ? logs[0].message?.slice(0, 60) : 'No recent logs'}`, 'info');
          break;

        case 'Prep':
          showToast('🎓 Interview prep: Send /prep to @samcvbot on Telegram', 'info');
          break;

        case 'Companies':
          showToast(`🏢 ${stats.heals} companies tracked in intelligence database`, 'info');
          break;

        case 'Settings':
          showToast('⚙️ Settings: Use /settings on @samcvbot Telegram bot', 'info');
          break;

        default:
          showToast(`${btn} — command received`, 'info');
      }
    } catch (err: any) {
      showToast(`❌ Error: ${err.message || 'Unknown error'}`, 'error');
    } finally {
      setLoadingBtn(null);
      await fetchStats();
    }
  };

  // ── Mission complete ──────────────────────────────────────
  const completeMission = async (id: number, recruiterUrl: string | null, message: string) => {
    if (recruiterUrl) window.open(recruiterUrl, '_blank');
    const nudge = message.includes('Nudge: ') ? message.split('Nudge: ')[1] : message;
    try { await navigator.clipboard.writeText(nudge); } catch {}
    await supabase.from('tasks').update({ status: 'COMPLETED' }).eq('id', id);
    fetchStats();
    showToast('✅ Mission deployed — profile opened & nudge copied!', 'success');
  };

  return (
    <main className={styles.main}>
      {/* Toast notification */}
      {toast && (
        <div className={`${styles.toast} ${styles[`toast_${toast.type}`]}`}>
          {toast.msg}
        </div>
      )}

      {/* Kill switch banner */}
      {killSwitchActive && (
        <div className={styles.killBanner}>
          ⏸️ BOT IS PAUSED — Click <strong>Resume</strong> to restart applications
        </div>
      )}

      {/* Navigation */}
      <nav className={`${styles.nav} glass-panel`}>
        <div className={styles.logo}>
          <span className={styles.rc}>RC</span>
          <span className={styles.title}>
            Project Chronos <br/>
            <small className="text-gradient">God Mode Command Center</small>
          </span>
        </div>
        <div className={styles.navLinks}>
          <button className="btn-glass" onClick={() => fetchStats()}>↻ Refresh</button>
          <button
            className={killSwitchActive ? styles.btnDanger : 'btn-glow'}
            onClick={() => handleButtonClick(killSwitchActive ? 'Resume' : 'Pause')}
          >
            {killSwitchActive ? '▶ Resume' : '⏸ Pause'}
          </button>
        </div>
      </nav>

      {/* Hero */}
      <header className={styles.hero}>
        <h1 className="text-gradient animate-float">Global Intelligence Hub</h1>
        <p className={styles.subtitle}>Real-time telemetry for the OMNISCIENT Decentralized Swarm.</p>
      </header>

      {/* Mission Deck — all buttons wired */}
      <section className={styles.missionDeck}>
        <div className={styles.deckHeader}>
          <h2>Sovereign Mission Deck</h2>
          <div className={`${styles.tooltipArea} ${hoveredDescription ? styles.active : ''}`}>
            {hoveredDescription ? `⚡ [INTEL]: ${hoveredDescription}` : '📡 HOVER BUTTONS FOR INTEL — CLICK TO EXECUTE'}
          </div>
        </div>
        <div className={styles.buttonGrid}>
          {Object.keys(buttonDescriptions).map((btn) => (
            <button
              key={btn}
              className={`btn-glass ${loadingBtn === btn ? styles.btnLoading : ''} ${
                (btn === 'Pause' && !killSwitchActive) || (btn === 'Resume' && killSwitchActive)
                  ? styles.btnActive : ''
              } ${btn === 'Omega Halt' ? styles.btnHalt : ''}`}
              onMouseEnter={() => setHoveredDescription(buttonDescriptions[btn])}
              onMouseLeave={() => setHoveredDescription(null)}
              onClick={() => handleButtonClick(btn)}
              disabled={loadingBtn !== null}
            >
              {loadingBtn === btn ? '⏳' : btn}
            </button>
          ))}
        </div>
      </section>

      {/* Radar */}
      <section className={`${styles.radarSection} glass-panel`}>
        <div className={`${styles.radarContainer} ${isPulsing ? styles.activePulse : ''}`}>
          <div className={styles.radarSweep}></div>
          <div className={styles.radarGrid}></div>
          <div className={`${styles.radarPoint} ${styles.p1}`}></div>
          <div className={`${styles.radarPoint} ${styles.p2}`}></div>
          <div className={`${styles.radarPoint} ${styles.p3}`}></div>
          <div className={styles.radarCore}>
            <Activity size={32} className="text-gradient" />
            <span className={styles.radarLabel}>{killSwitchActive ? 'PAUSED' : 'SWARM ACTIVE'}</span>
          </div>
        </div>
        <div className={styles.radarStats}>
          <h2 className="text-gradient">
            Sovereign Presence: {killSwitchActive ? '⏸️ PAUSED' : '✅ ACTIVE'}
          </h2>
          <p>Scanning for strategic opportunities across 12 sectors...</p>
          <div className={styles.radarMeta}>
            <span>Lat: 33.8938° N</span>
            <span>Lon: 35.5018° E</span>
            <span>Alti: ASCENDING</span>
          </div>
        </div>
      </section>

      {/* Stats Grid */}
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

      {/* Mission Board */}
      <section className={styles.missionSection}>
        <h2 className="section-title">Manual Missions Required <small>(Click to Execute)</small></h2>
        <div className={styles.missionGrid}>
          {missions.length > 0 ? missions.map((m) => {
            const recruiterUrl = m.message?.includes('URL: ')
              ? m.message.split('\n')[0].replace('URL: ', '') : null;
            return (
              <div key={m.id} className={`${styles.missionCard} glass-panel animate-slide-in`}>
                <div className={styles.mHeader}>
                  <span className={styles.mType}>{m.type}</span>
                  <span className={styles.mTarget}>{m.target}</span>
                </div>
                <p className={styles.mMeta}>{m.message?.split('Nudge: ')[1] || m.message}</p>
                <div className={styles.mActions}>
                  <button
                    onClick={() => completeMission(m.id, recruiterUrl, m.message)}
                    className="btn-glow-small"
                  >
                    Confirm Deployment
                  </button>
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

      {/* Live Terminal */}
      <section className={`${styles.terminal} glass-panel`}>
        <div className={styles.terminalHeader}>
          <div className={styles.macControls}>
            <span></span><span></span><span></span>
          </div>
          <div className={styles.terminalTitle}>engine.log — live</div>
          <TerminalIcon size={14} className="terminal-icon" />
        </div>
        <div className={styles.terminalBody}>
          {logs.length > 0 ? logs.map((log, i) => (
            <p key={i}>
              <span className={styles.tTime}>[{new Date(log.timestamp).toLocaleTimeString()}]</span>
              <span className={log.level === 'ERROR' ? styles.tError : styles.tSuccess}> {log.level}</span>
              {' '}📡 {log.message}
            </p>
          )) : (
            <p>Initializing Heartbeat... Waiting for next strike signal.</p>
          )}
        </div>
      </section>
    </main>
  );
}
