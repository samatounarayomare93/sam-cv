import resend
resend.api_key = "re_9hviZvvj_NHBwnZarfmnYfKszJaP4bivu"

# Test send
params = {
    "from": "Sam Salameh <onboarding@resend.dev>",
    "to": ["samsalameh.cv@gmail.com"],
    "subject": "✅ Test Email - Resend Working!",
    "html": "<h2 style='color:green'>✅ EMAIL DELIVERY WORKING!</h2><p>This email was sent via Resend API. If you see this in your inbox, everything is fixed!</p>"
}

email = resend.Emails.send(params)
print("Result:", email)
