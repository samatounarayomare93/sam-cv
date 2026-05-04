# 🚀 HOW TO REACH 10,000 EMAILS/DAY (ALL FREE)

## Current Capacity: ~900/day
## Target: 10,000/day

---

## STEP 1: Create 10 Zoho Accounts (5000/day)

Each Zoho account = 500 emails/day FREE

### How to create each account (5 minutes each):
1. Go to: https://www.zoho.com/mail/
2. Click "Sign Up Free"
3. Use a different email each time (e.g., samsalameh2@zohomail.com, samsalameh3@zohomail.com...)
4. After signup, go to: accounts.zoho.com → Security → App Passwords
5. Create an App Password
6. Add to Render environment variables:

```
ZOHO_SMTP_USER_2=samsalameh2@zohomail.com
ZOHO_APP_PASSWORD_2=your_app_password

ZOHO_SMTP_USER_3=samsalameh3@zohomail.com
ZOHO_APP_PASSWORD_3=your_app_password

... up to ZOHO_SMTP_USER_10
```

**10 Zoho accounts = 5,000 emails/day**

---

## STEP 2: Create 10 Resend Accounts (1000/day)

Each Resend account = 100 emails/day FREE (3000/month)

### How to create each account (2 minutes each):
1. Go to: https://resend.com/signup
2. Sign up with different email
3. Get API key from dashboard
4. Add to Render:

```
RESEND_API_KEY_2=re_xxxxx
RESEND_API_KEY_3=re_xxxxx
... up to RESEND_API_KEY_10
```

**10 Resend accounts = 1,000 emails/day**

---

## STEP 3: Activate Yahoo (500/day)

1. Go to: https://mail.yahoo.com
2. Create account: samsalameh.cv@yahoo.com
3. Enable App Password: account.yahoo.com → Security → App Passwords
4. Add to Render:
```
YAHOO_SMTP_USER=samsalameh.cv@yahoo.com
YAHOO_APP_PASSWORD=your_app_password
```

---

## TOTAL CAPACITY AFTER SETUP:

| Provider | Accounts | Daily |
|----------|----------|-------|
| Resend | 10 | 1,000 |
| Brevo | 1 | 300 |
| Zoho | 10 | 5,000 |
| Gmail | 1 | 500 |
| Yahoo | 1 | 500 |
| Outlook | 1 | 300 |
| **TOTAL** | **24** | **7,600/day** |

For 10,000/day: Add 5 more Zoho accounts = 2,500 more = **10,100/day** ✅

---

## The bot already supports all of this!
Just add the environment variables to Render and it works automatically.
