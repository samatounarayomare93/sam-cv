# 🚀 QUICK START GUIDE - 2 MINUTES TO RUNNING BOT

## Step 1: Double-click this file
```
START_BOT.bat
```

## Step 2: Open Telegram
Message your bot: **@samcvbot**

Send:
```
/start
```

## Step 3: Watch it work!
The bot will:
1. ✅ Connect to database
2. 🔍 Start discovering jobs
3. 🧠 Analyze with AI
4. 📧 Send applications
5. 📱 Notify you on Telegram

---

## 📱 Essential Telegram Commands

```
/status    - Check if bot is running
/pause     - Stop sending applications
/resume    - Resume sending applications
/stats     - See how many applications sent
```

---

## 🛑 How to Stop

Press `Ctrl + C` in the console window

Or send on Telegram:
```
/pause
```

---

## ⚠️ If Something Goes Wrong

1. **Bot won't start?**
   - Run: `diagnostic.py`
   - Check the output

2. **No jobs found?**
   - Wait 5 minutes (scraping takes time)
   - Check internet connection

3. **Emails not sending?**
   - Check `.env` file has email credentials
   - Run: `health_check.py`

---

## 📊 What to Expect

**First 10 minutes:**
- Bot discovers 10-50 jobs
- AI analyzes each one
- Sends 2-5 applications (high-quality matches only)

**First hour:**
- 50-200 jobs discovered
- 10-30 applications sent
- You'll get Telegram notification for each

**First day:**
- 200-500 jobs discovered
- 30-100 applications sent
- 1-3 responses expected (2-5% response rate)

---

## ✅ Success Indicators

You'll know it's working when you see:

**In Console:**
```
✅ Target Locked [85%]: Google - HR Manager
🚀 STRIKE SUCCESS: Application beamed to Google
```

**On Telegram:**
```
🎯 SINGULARITY STRIKE LOCKED (85%) - Google
✅ STRIKE SUCCESS - Google
```

**In Your Email:**
- Sent emails in your Zoho outbox
- Possible responses from recruiters

---

## 🎯 Pro Tips

1. **Let it run overnight** - Bot works 24/7
2. **Check Telegram in morning** - See overnight applications
3. **Review `/stats` daily** - Track progress
4. **Adjust filters in `.env`** - If too many/few applications

---

## 🆘 Emergency Stop

**Method 1:** Press `Ctrl + C` in console

**Method 2:** Telegram command:
```
/emergency
```

**Method 3:** Edit `.env` file:
```
KILL_SWITCH_ACTIVE=true
```

---

## 📈 Next Steps

Once bot is running smoothly:

1. **Read**: `SYSTEM_STATUS_REPORT.md` - Full system overview
2. **Customize**: `.env` file - Adjust job filters
3. **Monitor**: Telegram commands - Track performance
4. **Optimize**: Based on results after 1 week

---

**That's it! You're ready to go! 🚀**

Double-click `START_BOT.bat` and watch the magic happen!
