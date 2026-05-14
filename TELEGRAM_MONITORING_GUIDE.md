# 📱 CHRONOS TELEGRAM BOT - المراقبة والتحكم

## 🤖 Bot Info

**Bot Username:** @sam_bot (أو اسم بوتك)  
**Bot Token:** من `TELEGRAM_BOT_TOKEN` في `.env`  
**استضافة:** Render (24/7)  
**الحالة:** ✅ Online

---

## 📋 الأوامر الرئيسية

### 1. `/start` - ابدأ المحادثة
```
أرسل: /start

الرد:
╔════════════════════════════════════════╗
║     🤖 CHRONOS BOT - WELCOME          ║
║   مرحباً بك في نظام المراقبة        ║
╠════════════════════════════════════════╣
║                                        ║
║  أوامر متاحة:                         ║
║  📊 /stats      - الإحصائيات          ║
║  📬 /queue      - الطابور              ║
║  ⚕️  /health     - الصحة              ║
║  📝 /logs       - السجلات             ║
║  🔧 /settings   - الإعدادات           ║
║                                        ║
╚════════════════════════════════════════╝
```

---

### 2. `/stats` - إحصائيات فورية
```
أرسل: /stats

الرد:
╔════════════════════════════════════════╗
║        📊 LIVE STATISTICS            ║
╠════════════════════════════════════════╣
║ 🎯 Applications Sent Today: 23         ║
║ 📊 Applications Total: 1,234           ║
║ 📬 Leads in Queue: 567                 ║
║ ✉️  Emails Sent: 89                    ║
║ ⏱️  Last Scrape: 2 min ago             ║
║ 🤖 Bot Status: ✅ ONLINE               ║
║ 💾 Storage: 2.3 GB / 5 GB             ║
║ ⏱️  Uptime: 142 hours 34 minutes      ║
╠════════════════════════════════════════╣
║ 🟢 All systems operational            ║
╚════════════════════════════════════════╝
```

---

### 3. `/queue` - حالة الطابور
```
أرسل: /queue

الرد:
╔════════════════════════════════════════╗
║        📬 QUEUE STATUS                ║
╠════════════════════════════════════════╣
║ Total Leads: 567                       ║
║                                        ║
║ By Status:                             ║
║  ⏳ Pending:  420                      ║
║  🚀 Queued:   89                       ║
║  ✅ Applied:  2,104                    ║
║  ⏸️  Skipped:  200                     ║
║  ❌ Failed:    15                      ║
║                                        ║
║ Next Auto-Run: in 5 minutes 23 seconds ║
╚════════════════════════════════════════╝
```

---

### 4. `/health` - صحة النظام
```
أرسل: /health

الرد:
╔════════════════════════════════════════╗
║      ⚕️ SYSTEM HEALTH CHECK           ║
╠════════════════════════════════════════╣
║ Supabase Connection: ✅ Online        ║
║ SQLite Mirror: ✅ Synced               ║
║ Telegram API: ✅ Connected             ║
║ Gemini AI: ✅ Online                   ║
║ Groq Fallback: ✅ Ready                ║
║ Email Engines:                         ║
║   • Brevo: ✅ Working                  ║
║   • Resend: ✅ Working                 ║
║   • Gmail: ✅ Working                  ║
║ Memory Usage: 245 MB / 512 MB          ║
║ CPU Usage: 12% (last 5 min)            ║
║                                        ║
║ Last Check: 2026-05-14 10:23:45        ║
╚════════════════════════════════════════╝
```

---

### 5. `/logs` - آخر السجلات
```
أرسل: /logs

الرد:
2026-05-14 10:25:34 [INFO] - SCRAPER-DALEEL found 23 new leads
2026-05-14 10:24:15 [INFO] - Email sent to: jane@company.com
2026-05-14 10:23:45 [INFO] - Leadership pulse: Master alive
2026-05-14 10:22:30 [INFO] - AI analysis: score=78 (High Match)
2026-05-14 10:21:10 [INFO] - Auto-refill queue: +50 leads
2026-05-14 10:20:00 [WARNING] - Gemini rate limit, using Groq fallback
2026-05-14 10:19:45 [INFO] - Database sync complete
2026-05-14 10:18:20 [INFO] - Sent application to: hr@techcorp.com
2026-05-14 10:17:00 [INFO] - Queue processing cycle started
2026-05-14 10:15:30 [INFO] - Render heartbeat: alive

[📄 Page 1 of 3] [◀️ Previous] [Next ▶️]
```

---

### 6. `/settings` - الإعدادات
```
أرسل: /settings

الرد:
╔════════════════════════════════════════╗
║         ⚙️ SETTINGS MENU              ║
╠════════════════════════════════════════╣
║ 🎯 Min Match Score: 55%                ║
║ ⏱️  Queue Check Interval: 5 min         ║
║ 📧 Email Batch Size: 8                 ║
║ 🔄 Auto-Refill Threshold: 50 leads     ║
║ 🤖 AI Model: Gemini 2.0 Flash          ║
║ 🌍 Fallback AI: Groq Llama-3.3-70b    ║
║ 🚫 Kill Switch: OFF                    ║
║                                        ║
║ [⚙️ Edit]  [🔄 Reset]  [✅ Close]     ║
╚════════════════════════════════════════╝
```

---

## 🎮 الأوامر المتقدمة (Admin فقط)

### 7. `/scrape_now` - فعّل الكاشف اليدوي
```
أرسل: /scrape_now

الرد:
╔════════════════════════════════════════╗
║      🌍 SCRAPING INITIATED            ║
╠════════════════════════════════════════╣
║                                        ║
║ Activating all scrapers...             ║
║ • SCRAPER-DALEEL ............. ▓▓▓░░  ║
║ • SCRAPER-OMNI ............... ▓▓▓▓░  ║
║ • SCRAPER-TELEGRAM ........... ▓▓▓▓▓  ║
║                                        ║
║ Found 145 new leads                    ║
║                                        ║
║ Results will appear in Queue            ║
║ within 2-3 minutes.                    ║
║                                        ║
╚════════════════════════════════════════╝
```

---

### 8. `/force_strike` - أرسل أفضل lead يدوياً
```
أرسل: /force_strike

الرد:
╔════════════════════════════════════════╗
║      🎯 FORCE STRIKE ACTIVE           ║
╠════════════════════════════════════════╣
║ Company: TechCorp Inc                  ║
║ Position: HR Manager                   ║
║ Email: jane@techcorp.com               ║
║ Score: 89/100 (HIGH)                   ║
║                                        ║
║ 📧 Sending personalized email...       ║
║ ✅ Email sent successfully!            ║
║                                        ║
║ Timestamp: 2026-05-14 10:26:30         ║
║ Next Strike: Ready                     ║
╚════════════════════════════════════════╝
```

---

### 9. `/kill_switch` - إيقاف النظام بالكامل
```
أرسل: /kill_switch

الرد:
🛑 KILL SWITCH ACTIVATED

All operations suspended:
✋ Scrapers: STOPPED
✋ Email Engine: STOPPED
✋ AI Analysis: STOPPED
✋ Leadership Elections: STOPPED

Bot remains responsive for emergency commands.
To resume: /resume
```

---

### 10. `/resume` - استئناف التشغيل
```
أرسل: /resume

الرد:
▶️ SYSTEM RESUMING

All operations restarting:
✅ Scrapers: ONLINE
✅ Email Engine: ONLINE
✅ AI Analysis: ONLINE
✅ Leadership Elections: ONLINE

Ready for full operation.
```

---

## 📊 لوحة التحكم التفاعلية

### `/dashboard` (Admin فقط)
```
أرسل: /dashboard

الرد: (لوحة تحكم تفاعلية كاملة مع أزرار)

╔════════════════════════════════════════╗
║  🎛️ CHRONOS CONTROL DASHBOARD         ║
╠════════════════════════════════════════╣
║                                        ║
║ [📊 Stats]  [📬 Queue]  [⚕️ Health]   ║
║ [🌍 Scrape] [🎯 Strike] [📝 Logs]    ║
║                                        ║
║ [⚙️ Settings] [🛑 Kill] [✅ Resume]   ║
║                                        ║
║ [📱 Notify]  [🔄 Refresh] [❌ Close]  ║
║                                        ║
╚════════════════════════════════════════╝
```

---

## 🔔 النوتيفيكيشنات التلقائية

يرسل البوت تحديثات تلقائية عند:

```
✅ تطبيق جديد تم إرساله
  "📧 Sent application to: hr@company.com (Score: 87/100)"

✅ lead جديد تم إيجاده
  "🌍 New lead found: Senior HR @ Google (Cairo, Egypt)"

⚠️ خطأ أو تحذير
  "⚠️ Gemini rate limit exceeded. Falling back to Groq."

🔄 إعادة تشغيل
  "🔄 System restart initiated. Back online in 30 seconds."

📊 تقرير يومي
  "📈 Daily Report - 45 apps sent, 234 leads found, 98% accuracy"
```

---

## 💡 نصائح للاستخدام

1. **للمراقبة اليومية:**
   - استخدم `/stats` كل ساعة
   - استخدم `/health` عند الشك

2. **للتحقق من المشاكل:**
   - استخدم `/logs` لرؤية الأخطاء
   - استخدم `/health` للتشخيص

3. **للتحكم اليدوي:**
   - استخدم `/scrape_now` لتفعيل فوري
   - استخدم `/force_strike` لإرسال فوري

4. **للطوارئ:**
   - استخدم `/kill_switch` لإيقاف فوري
   - استخدم `/resume` لاستئناف التشغيل

---

## 🔐 الأمان

- جميع الأوامر محمية بـ Admin verification
- الأوامر الحساسة تطلب تأكيد إضافي
- جميع العمليات يتم تسجيلها في الـ database
- لا تشارك tokens أو credentials عبر Telegram

---

**آخر تحديث**: 14 مايو 2026
