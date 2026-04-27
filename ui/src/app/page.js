"use client";

import React, { useState, useEffect } from "react";

/**
 * 👑 PROJECT CHRONOS: COMMAND CENTER
 * The absolute remote control interface for Sam's Job Automator.
 * Features Glassmorphism design and real-time telemetry.
 */
export default function CommandCenter() {
  const [lang, setLang] = useState("en");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [metrics, setMetrics] = useState({
    total_strikes: 2453,
    success_rate: 98.4,
    live_nodes: 5,
    pending_deep_dives: 12
  });

  // Multilingual content dictionary
  const content = {
    en: {
      title: "PROJECT CHRONOS",
      subtitle: "ALPHA & OMEGA COMMAND CENTER",
      status: "SYSTEM STATUS: OPERATIONAL",
      killSwitch: "EMERGENCY KILL SWITCH",
      metrics: {
        strikes: "Total Strikes",
        success: "Success Rate",
        nodes: "Active Nodes",
        dives: "Pending Dives"
      },
      tabs: {
        dashboard: "📊 Dashboard",
        scrapers: "🕵️‍♂️ Scrapers",
        settings: "⚙️ Settings"
      },
      feeds: "ALPHA TELEMETRY FEED",
      noFeed: "Awaiting incoming sync from Orchestrator...",
      quickActions: "Quick Strike Protocols",
      actions: [
        { label: "Start Scrape", id: "scrape", icon: "🚀" },
        { label: "Check Health", id: "health", icon: "🩺" },
        { label: "Sync DB", id: "sync", icon: "🔄" },
        { label: "Deploy Healer", id: "heal", icon: "🩹" }
      ]
    },
    ar: {
      title: "مشروع كرونوس",
      subtitle: "مركز قيادة ألفا وأوميغا",
      status: "حالة النظام: يعمل بكفاءة",
      killSwitch: "مفتاح الإيقاف الطارئ",
      metrics: {
        strikes: "إجمالي الهجمات",
        success: "نسبة النجاح",
        nodes: "العقد النشطة",
        dives: "عمليات المعالجة"
      },
      tabs: {
        dashboard: "📊 لوحة التحكم",
        scrapers: "🕵️‍♂️ الكاشطات",
        settings: "⚙️ الإعدادات"
      },
      feeds: "بث نظام ألفا",
      noFeed: "في انتظار المزامنة من المحرك الرئيسي...",
      quickActions: "بروتوكولات الهجوم السريع",
      actions: [
        { label: "بدء المسح", id: "scrape", icon: "🚀" },
        { label: "فحص الصحة", id: "health", icon: "🩺" },
        { label: "مزامنة البيانات", id: "sync", icon: "🔄" },
        { label: "تشغيل المعالج", id: "heal", icon: "🩹" }
      ]
    }
  };

  const t = content[lang];

  // Logic to simulate live metrics
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        total_strikes: prev.total_strikes + (Math.random() > 0.7 ? 1 : 0),
        pending_deep_dives: Math.max(0, prev.pending_deep_dives + (Math.random() > 0.5 ? 1 : -1))
      }));
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main className={`min-h-screen p-8 transition-all duration-700 ${lang === "ar" ? "rtl" : "ltr"}`} dir={lang === "ar" ? "rtl" : "ltr"}>
      <div className="bg-drift"></div>

      {/* 👑 HEADER SECTION */}
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center mb-12">
        <div className="text-center md:text-left mb-6 md:mb-0">
          <h1 className="text-5xl md:text-6xl font-black neon-glow bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-purple-500 tracking-tighter">
            {t.title}
          </h1>
          <p className="text-[10px] md:text-xs font-light tracking-[0.5em] text-sky-300 opacity-80 mt-2 uppercase">
            {t.subtitle}
          </p>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={() => setLang(lang === "en" ? "ar" : "en")}
            className="glass-panel px-6 py-2 hover:bg-white/10 transition-all font-bold text-[10px] tracking-widest uppercase border-white/10"
          >
            {lang === "en" ? "العربية" : "English"}
          </button>
          <div className="flex items-center px-4 py-2 glass-panel border-emerald-500/20">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse mr-3 ml-3" />
            <span className="text-[10px] font-bold tracking-tighter text-emerald-400 uppercase">{t.status}</span>
          </div>
        </div>
      </div>

      {/* 📊 METRICS GRID */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[
          { key: "total_strikes", val: metrics.total_strikes, label: t.metrics.strikes },
          { key: "success_rate", val: `${metrics.success_rate}%`, label: t.metrics.success },
          { key: "live_nodes", val: metrics.live_nodes, label: t.metrics.nodes },
          { key: "pending_dives", val: metrics.pending_deep_dives, label: t.metrics.dives },
        ].map((item) => (
          <div key={item.key} className="glass-panel p-6 neon-border group hover:scale-[1.02] transition-transform">
            <div className="text-[10px] text-sky-300/60 font-medium uppercase tracking-widest mb-2">
              {item.label}
            </div>
            <div className="text-4xl font-black tabular-nums">
              {item.val.toLocaleString()}
            </div>
          </div>
        ))}
      </div>

      {/* 🕹️ MAIN WORKSPACE */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN: CONTROLS */}
        <div className="lg:col-span-1 space-y-6">
          {/* QUICK ACTIONS */}
          <div className="glass-panel p-6 border-white/5">
            <h3 className="text-[10px] font-bold tracking-widest uppercase mb-6 opacity-50">{t.quickActions}</h3>
            <div className="grid grid-cols-2 gap-3">
              {t.actions.map((action) => (
                <button 
                  key={action.id}
                  className="flex flex-col items-center justify-center p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 transition-all group"
                >
                  <span className="text-2xl mb-2 group-hover:scale-110 transition-transform">{action.icon}</span>
                  <span className="text-[10px] font-bold uppercase tracking-tighter">{action.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* EMERGENCY BLOCK */}
          <div className="glass-panel p-8 border-rose-500/10 flex flex-col justify-center items-center text-center">
            <div className="w-20 h-20 rounded-full border-4 border-rose-500/20 flex items-center justify-center mb-6 animate-pulse-slow">
               <div className="w-12 h-12 bg-rose-500 rounded-full blur-md opacity-40 shadow-[0_0_20px_#f43f5e]" />
            </div>
            <button className="w-full bg-rose-600 hover:bg-rose-500 text-white font-black py-4 rounded-xl shadow-[0_0_30px_rgba(225,29,72,0.4)] transition-all uppercase tracking-widest text-xs">
              {t.killSwitch}
            </button>
            <p className="mt-4 text-[9px] text-white/30 uppercase leading-relaxed tracking-wider">
              Authorized Personnel Only. Cascade global shutdown.
            </p>
          </div>
        </div>

        {/* RIGHT COLUMN: TELEMETRY FEED */}
        <div className="lg:col-span-2 glass-panel p-8 relative overflow-hidden flex flex-col min-h-[500px]">
          <div className="flex justify-between items-center mb-6 border-b border-white/5 pb-4">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-sky-500 rounded-full animate-ping" />
              <h3 className="text-xs font-bold tracking-[0.3em] uppercase">{t.feeds}</h3>
            </div>
            <span className="text-[8px] bg-sky-500/10 text-sky-300 px-2 py-1 rounded font-mono border border-sky-500/20">UPLINK_STABLE</span>
          </div>
          
          <div className="flex-1 flex flex-col justify-center items-center text-white/20 italic text-sm text-center">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-sky-500 mb-6 opacity-40"></div>
            <p className="max-w-xs">{t.noFeed}</p>
          </div>
          
          {/* Subtle noise pattern */}
          <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
        </div>

      </div>

      {/* 🏷️ FOOTER */}
      <div className="max-w-7xl mx-auto mt-12 text-center">
        <p className="text-[10px] text-white/10 tracking-[1em] uppercase">Sam Salameh - Royal Divine Supremacy v3.0</p>
      </div>
    </main>
  );
}
