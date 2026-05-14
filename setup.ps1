#Requires -Version 5.1
<#
.SYNOPSIS
    Complete Setup Script for Rita Job Automator
.DESCRIPTION
    Automatically configures GitHub, Render, and all services
.NOTES
    Author: Sam Salameh
    Version: 2.0 (Secure - No hardcoded tokens)
#>

[CmdletBinding()]
param()

# Error handling
$ErrorActionPreference = "Stop"
$ProgressPreference = "Continue"

# Colors
$Green = "`e[32m"
$Red = "`e[31m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"

function Write-Status($Message, $Type = "Info") {
    $prefix = switch ($Type) {
        "Success" { "${Green}✅" }
        "Error"   { "${Red}❌" }
        "Warning" { "${Yellow}⚠️" }
        "Info"    { "${Blue}ℹ️" }
        default   { "ℹ️" }
    }
    Write-Host "$prefix $Message${Reset}"
}

function Write-Section($Title) {
    Write-Host ""
    Write-Host "${Blue}══════════════════════════════════════════════════════════════${Reset}"
    Write-Host "${Blue}  $Title${Reset}"
    Write-Host "${Blue}══════════════════════════════════════════════════════════════${Reset}"
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

$Config = @{
    GitHubRepo = "samatounarayomare93/sam-cv"
    GitHubToken = ""
    RenderAPIKey1 = ""
    RenderAPIKey2 = ""
    ProjectPath = $PSScriptRoot
}

# Load tokens from config file if exists
$ConfigFile = Join-Path $PSScriptRoot "tokens.config"
if (Test-Path $ConfigFile) {
    try {
        $Tokens = Get-Content $ConfigFile | ConvertFrom-Json
        $Config.GitHubToken = $Tokens.GitHubToken
        $Config.RenderAPIKey1 = $Tokens.RenderAPIKey1
        $Config.RenderAPIKey2 = $Tokens.RenderAPIKey2
        Write-Status "Loaded tokens from config file" "Success"
    } catch {
        Write-Status "Could not load config file" "Warning"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: CHECK REQUIREMENTS
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 1: Checking Requirements"

# Check GitHub CLI
Write-Status "Checking GitHub CLI..." "Info"
try {
    $ghVersion = gh --version 2>$null | Select-Object -First 1
    if ($ghVersion) {
        Write-Status "GitHub CLI found: $ghVersion" "Success"
    } else {
        Write-Status "GitHub CLI not found. Installing..." "Warning"
        winget install --id GitHub.cli -e --source winget
        Write-Status "GitHub CLI installed" "Success"
    }
} catch {
    Write-Status "GitHub CLI check failed: $_" "Error"
    Write-Host "Please install GitHub CLI manually from: https://cli.github.com/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Git
Write-Status "Checking Git..." "Info"
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Status "Git found: $gitVersion" "Success"
    } else {
        Write-Status "Git not found. Please install Git first." "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Status "Git check failed" "Error"
    exit 1
}

# Check if in correct directory
Write-Status "Checking project directory..." "Info"
if (-not (Test-Path "$($Config.ProjectPath)\swarm_orchestrator.py")) {
    Write-Status "Not in project directory! Please run from project folder." "Error"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Status "Project directory verified" "Success"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: GET TOKENS
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 2: Authentication Tokens"

if (-not $Config.GitHubToken) {
    Write-Status "GitHub token not found in config" "Warning"
    Write-Host "${Yellow}Please enter your GitHub Personal Access Token:${Reset}"
    Write-Host "(Get from: https://github.com/settings/tokens)"
    Write-Host "(Needs 'repo' and 'workflow' scopes)"
    $secureToken = Read-Host "GitHub Token" -AsSecureString
    $Config.GitHubToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken))
}

if (-not $Config.RenderAPIKey1) {
    Write-Status "Render API keys not found in config" "Warning"
    Write-Host "${Yellow}Please enter your Render API Key (optional):${Reset}"
    Write-Host "(Get from: https://dashboard.render.com/settings#api-keys)"
    $Config.RenderAPIKey1 = Read-Host "Render API Key 1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: GITHUB AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 3: GitHub Authentication"

Write-Status "Authenticating with GitHub..." "Info"
try {
    $env:GH_TOKEN = $Config.GitHubToken
    
    $authStatus = gh auth status 2>&1
    if ($authStatus -match "Logged in") {
        Write-Status "Already authenticated" "Success"
    } else {
        Write-Status "Authenticating with token..." "Info"
        $Config.GitHubToken | gh auth login --with-token
        Write-Status "Authentication successful" "Success"
    }
} catch {
    Write-Status "GitHub authentication failed: $_" "Error"
    Write-Host "Please check your GitHub token and try again."
    Read-Host "Press Enter to exit"
    exit 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: GET API KEYS FROM USER
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 4: API Keys Configuration"

Write-Host "${Yellow}Please enter your API keys (get them from the links below):${Reset}"
Write-Host ""

# Gemini API Key
Write-Host "${Blue}1. Gemini API Key${Reset} (Free - https://aistudio.google.com/apikey)"
$GeminiKey = Read-Host "   Enter Gemini API Key (or press Enter to skip)"

# Groq API Key
Write-Host ""
Write-Host "${Blue}2. Groq API Key${Reset} (Free - https://console.groq.com/keys)"
$GroqKey = Read-Host "   Enter Groq API Key (or press Enter to skip)"

# Telegram Bot Token
Write-Host ""
Write-Host "${Blue}3. Telegram Bot Token${Reset} (Get from @BotFather)"
$TelegramToken = Read-Host "   Enter Telegram Bot Token (or press Enter to skip)"

# Telegram Chat ID
Write-Host ""
Write-Host "${Blue}4. Telegram Chat ID${Reset} (Get from @userinfobot)"
$TelegramChatID = Read-Host "   Enter Telegram Chat ID (or press Enter to skip)"

# Brevo SMTP
Write-Host ""
Write-Host "${Blue}5. Brevo SMTP${Reset} (Free - https://www.brevo.com)"
$BrevoLogin = Read-Host "   Enter Brevo SMTP Login (or press Enter to skip)"
$BrevoPassword = Read-Host "   Enter Brevo SMTP Password (or press Enter to skip)"

# Gmail
Write-Host ""
Write-Host "${Blue}6. Gmail SMTP${Reset} (Optional - for backup)"
$GmailUser = Read-Host "   Enter Gmail Address (or press Enter to skip)"
$GmailPassword = Read-Host "   Enter Gmail App Password (or press Enter to skip)"

# Candidate Info
Write-Host ""
Write-Host "${Blue}7. Candidate Information${Reset}"
$CandidateName = Read-Host "   Enter Candidate Name (e.g., Rita Salameh)"
$CandidateEmail = Read-Host "   Enter Candidate Email"

# Supabase (Optional)
Write-Host ""
Write-Host "${Blue}8. Supabase${Reset} (Optional - https://supabase.com)"
$SupabaseURL = Read-Host "   Enter Supabase URL (or press Enter to skip)"
$SupabaseKey = Read-Host "   Enter Supabase Key (or press Enter to skip)"

Write-Host ""
Write-Status "API keys collected" "Success"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: SET GITHUB SECRETS
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 5: Setting GitHub Secrets"

$Secrets = @{
    "GEMINI_API_KEY" = $GeminiKey
    "GROQ_API_KEY" = $GroqKey
    "TELEGRAM_BOT_TOKEN" = $TelegramToken
    "TELEGRAM_CHAT_ID" = $TelegramChatID
    "BREVO_SMTP_LOGIN" = $BrevoLogin
    "BREVO_SMTP_PASSWORD" = $BrevoPassword
    "GMAIL_SMTP_USER" = $GmailUser
    "GMAIL_APP_PASSWORD" = $GmailPassword
    "CANDIDATE_NAME" = $CandidateName
    "CANDIDATE_EMAIL" = $CandidateEmail
    "SUPABASE_URL" = $SupabaseURL
    "SUPABASE_KEY" = $SupabaseKey
}

foreach ($Secret in $Secrets.GetEnumerator()) {
    if ($Secret.Value) {
        try {
            Write-Status "Setting secret: $($Secret.Key)..." "Info"
            $Secret.Value | gh secret set $Secret.Key --repo $Config.GitHubRepo
            Write-Status "Secret set: $($Secret.Key)" "Success"
        } catch {
            Write-Status "Failed to set $($Secret.Key): $_" "Warning"
        }
    } else {
        Write-Status "Skipping empty secret: $($Secret.Key)" "Warning"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: ENABLE GITHUB ACTIONS
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 6: Enabling GitHub Actions"

try {
    Write-Status "Checking GitHub Actions status..." "Info"
    
    $workflows = gh workflow list --repo $Config.GitHubRepo 2>$null
    if ($workflows) {
        Write-Status "Workflows found:" "Success"
        Write-Host $workflows
        
        Write-Status "Enabling workflows..." "Info"
        $workflowNames = @("swarm-scout", "swarm-writer", "swarm-sender", "swarm-tracker", "unlimited-swarm")
        foreach ($wf in $workflowNames) {
            try {
                gh workflow enable --repo $Config.GitHubRepo $wf 2>$null
                Write-Status "Enabled: $wf" "Success"
            } catch {
                Write-Status "Could not enable $wf (may not exist)" "Warning"
            }
        }
    } else {
        Write-Status "No workflows found. Make sure .github/workflows/ exists." "Warning"
    }
} catch {
    Write-Status "Workflow setup failed: $_" "Warning"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7: VERIFY SETUP
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 7: Verification"

try {
    Write-Status "Verifying GitHub secrets..." "Info"
    $secretList = gh secret list --repo $Config.GitHubRepo 2>$null
    if ($secretList) {
        Write-Status "Secrets configured:" "Success"
        Write-Host $secretList
    }
} catch {
    Write-Status "Could not verify secrets (permissions)" "Warning"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8: RENDER SETUP INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "STEP 8: Render Setup (Manual)"

Write-Host "${Yellow}Render setup requires manual configuration:${Reset}"
Write-Host ""
Write-Host "1. Go to: https://dashboard.render.com"
Write-Host "2. Sign in with your account"
Write-Host "3. Click 'New +' → 'Web Service'"
Write-Host "4. Connect your GitHub repo: $($Config.GitHubRepo)"
Write-Host "5. Add these environment variables:"
Write-Host ""

foreach ($Secret in $Secrets.GetEnumerator()) {
    if ($Secret.Value) {
        $maskedValue = $Secret.Value.Substring(0, [Math]::Min(8, $Secret.Value.Length)) + "***"
        Write-Host "   $($Secret.Key) = $maskedValue"
    }
}

Write-Host ""
Write-Host "6. Click 'Create Web Service'"
Write-Host "7. Wait for deployment"
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9: TELEGRAM BOT SETUP
# ═══════════════════════════════════════════════════════════════════════════════

if ($TelegramToken -and $TelegramChatID) {
    Write-Section "STEP 9: Testing Telegram Bot"
    
    try {
        Write-Status "Sending test message..." "Info"
        $message = "🚀 Rita Job Automator Setup Complete!%0A%0ASystem is ready to run 24/7 ☁️"
        $url = "https://api.telegram.org/bot$TelegramToken/sendMessage?chat_id=$TelegramChatID&text=$message&parse_mode=HTML"
        
        $response = Invoke-RestMethod -Uri $url -Method Get
        if ($response.ok) {
            Write-Status "Telegram test message sent!" "Success"
        }
    } catch {
        Write-Status "Telegram test failed: $_" "Warning"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "✅ SETUP COMPLETE!"

Write-Host "${Green}Your Rita Job Automator is configured!${Reset}"
Write-Host ""
Write-Host "${Blue}Next Steps:${Reset}"
Write-Host "1. ✅ GitHub secrets configured"
Write-Host "2. ✅ GitHub Actions enabled"
Write-Host "3. ⏳ Complete Render setup manually (see Step 8)"
Write-Host "4. ⏳ Test the system"
Write-Host ""
Write-Host "${Blue}Monitoring:${Reset}"
Write-Host "- GitHub Actions: https://github.com/$($Config.GitHubRepo)/actions"
Write-Host "- Telegram Bot: Send /start to your bot"
Write-Host ""
Write-Host "${Blue}Support:${Reset}"
Write-Host "- Check SWARM_SETUP_GUIDE.md for details"
Write-Host "- Check logs in GitHub Actions"
Write-Host ""

Read-Host "Press Enter to exit"
