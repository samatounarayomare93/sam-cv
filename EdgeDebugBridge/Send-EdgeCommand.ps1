# =============================================================================
# Send-EdgeCommand.ps1
# Network Controller — CDP WebSocket Command Dispatcher
#
# Treats the browser tab as a Remote Node and dispatches JSON-RPC payloads
# over the Chrome DevTools Protocol WebSocket channel.
#
# USAGE:
#   . .\Send-EdgeCommand.ps1          # Dot-source to load all functions
#   $tab = Select-EdgeTab             # Pick a target tab
#   Invoke-EdgeJS -Tab $tab -Script "document.title"
#   Invoke-EdgeClick -Tab $tab -Selector "#login-button"
#   Invoke-EdgeExtract -Tab $tab -Selector ".product-title"
# =============================================================================

$CDP_BASE = "http://localhost:9222"

# --- INTERNAL: WebSocket RPC Dispatcher ---

function Send-CDPMessage {
    <#
    .SYNOPSIS
        Core dispatcher. Opens a WebSocket to the target tab's debug URL,
        sends a JSON-RPC payload, and returns the parsed response.
    .PARAMETER WebSocketUrl
        The webSocketDebuggerUrl of the target tab.
    .PARAMETER Method
        CDP method name (e.g., "Runtime.evaluate", "DOM.querySelector").
    .PARAMETER Params
        Hashtable of parameters for the CDP method.
    #>
    param(
        [Parameter(Mandatory)][string]$WebSocketUrl,
        [Parameter(Mandatory)][string]$Method,
        [hashtable]$Params = @{},
        [int]$TimeoutMs = 8000
    )

    # Build JSON-RPC 2.0 payload
    $payload = @{
        id     = [int](Get-Date -UFormat %s)  # Unique message ID
        method = $Method
        params = $Params
    } | ConvertTo-Json -Depth 10 -Compress

    # Establish WebSocket connection
    $ws = [System.Net.WebSockets.ClientWebSocket]::new()
    $cts = [System.Threading.CancellationTokenSource]::new($TimeoutMs)

    try {
        $uri = [System.Uri]::new($WebSocketUrl)
        $connectTask = $ws.ConnectAsync($uri, $cts.Token)
        $connectTask.Wait($TimeoutMs) | Out-Null

        if ($ws.State -ne [System.Net.WebSockets.WebSocketState]::Open) {
            throw "WebSocket failed to open. State: $($ws.State)"
        }

        # Transmit payload
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
        $segment = [System.ArraySegment[byte]]::new($bytes)
        $ws.SendAsync($segment, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, $cts.Token).Wait() | Out-Null

        # Receive response (loop until full message received)
        $buffer = [byte[]]::new(65536)
        $responseBuilder = [System.Text.StringBuilder]::new()

        do {
            $recvSegment = [System.ArraySegment[byte]]::new($buffer)
            $result = $ws.ReceiveAsync($recvSegment, $cts.Token).GetAwaiter().GetResult()
            $chunk = [System.Text.Encoding]::UTF8.GetString($buffer, 0, $result.Count)
            $responseBuilder.Append($chunk) | Out-Null
        } while (-not $result.EndOfMessage)

        $rawResponse = $responseBuilder.ToString()
        return $rawResponse | ConvertFrom-Json

    } catch {
        Write-Error "CDP Dispatch Error: $_"
        return $null
    } finally {
        if ($ws.State -eq [System.Net.WebSockets.WebSocketState]::Open) {
            $ws.CloseAsync(
                [System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure,
                "Done", [System.Threading.CancellationToken]::None
            ).Wait() | Out-Null
        }
        $ws.Dispose()
        $cts.Dispose()
    }
}

# --- PUBLIC: Tab Selector ---

function Select-EdgeTab {
    <#
    .SYNOPSIS
        Lists all open page tabs and prompts the user to select one.
        Returns the selected tab object (including its WebSocket URL).
    .PARAMETER Index
        Optionally pass an index directly to skip the interactive prompt.
    #>
    param([int]$Index = -1)

    $tabs = Invoke-RestMethod -Uri "$CDP_BASE/json" | Where-Object { $_.type -eq "page" }

    if ($null -eq $tabs -or $tabs.Count -eq 0) {
        Write-Error "No active page tabs found on Remote Node."
        return $null
    }

    if ($Index -ge 0 -and $Index -lt $tabs.Count) {
        return $tabs[$Index]
    }

    Write-Host "`n[*] Available Tabs:" -ForegroundColor Cyan
    for ($i = 0; $i -lt $tabs.Count; $i++) {
        Write-Host "    [$i] $($tabs[$i].title)" -ForegroundColor White
        Write-Host "        $($tabs[$i].url)" -ForegroundColor DarkGray
    }

    $choice = Read-Host "`nSelect tab index"
    return $tabs[[int]$choice]
}

# --- PUBLIC: JavaScript Evaluator ---

function Invoke-EdgeJS {
    <#
    .SYNOPSIS
        Executes arbitrary JavaScript in the context of the target tab.
        This is the raw execution primitive — all higher-level functions use this.
    .EXAMPLE
        Invoke-EdgeJS -Tab $tab -Script "document.title"
        Invoke-EdgeJS -Tab $tab -Script "window.location.href"
    #>
    param(
        [Parameter(Mandatory)][PSCustomObject]$Tab,
        [Parameter(Mandatory)][string]$Script,
        [switch]$ReturnByValue
    )

    $params = @{
        expression            = $Script
        returnByValue         = [bool]$ReturnByValue
        awaitPromise          = $true
        userGesture           = $true   # Required for click() and focus() to work
    }

    $response = Send-CDPMessage `
        -WebSocketUrl $Tab.webSocketDebuggerUrl `
        -Method "Runtime.evaluate" `
        -Params $params

    if ($response.result.exceptionDetails) {
        Write-Warning "JS Exception: $($response.result.exceptionDetails.exception.description)"
        return $null
    }

    return $response.result.result
}

# --- PUBLIC: Element Clicker ---

function Invoke-EdgeClick {
    <#
    .SYNOPSIS
        Clicks a DOM element identified by a CSS selector on the target tab.
        Dispatches a real MouseEvent to bypass passive listeners.
    .EXAMPLE
        Invoke-EdgeClick -Tab $tab -Selector "#login-button"
        Invoke-EdgeClick -Tab $tab -Selector "button[type='submit']"
    #>
    param(
        [Parameter(Mandatory)][PSCustomObject]$Tab,
        [Parameter(Mandatory)][string]$Selector
    )

    # Escape single quotes in selector for safe JS embedding
    $safeSelector = $Selector -replace "'", "\'"

    $script = @"
(function() {
    const el = document.querySelector('$safeSelector');
    if (!el) return { success: false, error: 'Element not found: $safeSelector' };

    // Scroll into view first
    el.scrollIntoView({ behavior: 'instant', block: 'center' });

    // Dispatch a real MouseEvent (bypasses some JS guards)
    const rect = el.getBoundingClientRect();
    const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: rect.left + rect.width / 2,
        clientY: rect.top + rect.height / 2
    });
    el.dispatchEvent(clickEvent);

    return {
        success: true,
        element: el.tagName,
        text: el.innerText.trim().substring(0, 80),
        href: el.href || null
    };
})()
"@

    $result = Invoke-EdgeJS -Tab $Tab -Script $script -ReturnByValue
    if ($result.value.success) {
        Write-Host "[+] Clicked: <$($result.value.element)> `"$($result.value.text)`"" -ForegroundColor Green
    } else {
        Write-Warning "Click failed: $($result.value.error)"
    }
    return $result.value
}

# --- PUBLIC: Data Extractor ---

function Invoke-EdgeExtract {
    <#
    .SYNOPSIS
        Extracts text content from all elements matching a CSS selector.
    .EXAMPLE
        Invoke-EdgeExtract -Tab $tab -Selector ".product-title"
        Invoke-EdgeExtract -Tab $tab -Selector "table tr td:first-child"
    #>
    param(
        [Parameter(Mandatory)][PSCustomObject]$Tab,
        [Parameter(Mandatory)][string]$Selector,
        [ValidateSet("text", "html", "value", "href", "src", "all")]
        [string]$Property = "text"
    )

    $safeSelector = $Selector -replace "'", "\'"

    $script = @"
(function() {
    const elements = Array.from(document.querySelectorAll('$safeSelector'));
    if (elements.length === 0) return { count: 0, data: [] };

    const data = elements.map((el, i) => ({
        index: i,
        tag: el.tagName,
        text: el.innerText?.trim() || '',
        html: el.innerHTML?.trim() || '',
        value: el.value || '',
        href: el.href || '',
        src: el.src || '',
        id: el.id || '',
        className: el.className || ''
    }));

    return { count: elements.length, data: data };
})()
"@

    $result = Invoke-EdgeJS -Tab $Tab -Script $script -ReturnByValue

    if ($result.value.count -eq 0) {
        Write-Warning "No elements matched selector: '$Selector'"
        return $null
    }

    Write-Host "[+] Extracted $($result.value.count) element(s) matching '$Selector':" -ForegroundColor Cyan
    foreach ($item in $result.value.data) {
        Write-Host "    [$($item.index)] <$($item.tag)> $($item.text.Substring(0, [Math]::Min(100, $item.text.Length)))" -ForegroundColor White
    }

    return $result.value.data
}

# --- PUBLIC: Form Filler ---

function Invoke-EdgeFill {
    <#
    .SYNOPSIS
        Sets the value of an input field and triggers React/Vue-compatible change events.
    .EXAMPLE
        Invoke-EdgeFill -Tab $tab -Selector "#username" -Value "admin"
        Invoke-EdgeFill -Tab $tab -Selector "input[name='password']" -Value "secret"
    #>
    param(
        [Parameter(Mandatory)][PSCustomObject]$Tab,
        [Parameter(Mandatory)][string]$Selector,
        [Parameter(Mandatory)][string]$Value
    )

    $safeSelector = $Selector -replace "'", "\'"
    $safeValue    = $Value    -replace "'", "\'"

    $script = @"
(function() {
    const el = document.querySelector('$safeSelector');
    if (!el) return { success: false, error: 'Element not found' };

    // Native input value setter (works with React's synthetic events)
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;
    nativeInputValueSetter.call(el, '$safeValue');

    el.dispatchEvent(new Event('input',  { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));

    return { success: true, element: el.tagName, name: el.name || el.id };
})()
"@

    $result = Invoke-EdgeJS -Tab $Tab -Script $script -ReturnByValue
    if ($result.value.success) {
        Write-Host "[+] Filled <$($result.value.element)> name='$($result.value.name)' with value." -ForegroundColor Green
    } else {
        Write-Warning "Fill failed: $($result.value.error)"
    }
    return $result.value
}

# --- PUBLIC: Page Navigator ---

function Invoke-EdgeNavigate {
    <#
    .SYNOPSIS
        Navigates the target tab to a new URL using the Page.navigate CDP method.
    .EXAMPLE
        Invoke-EdgeNavigate -Tab $tab -Url "https://example.com"
    #>
    param(
        [Parameter(Mandatory)][PSCustomObject]$Tab,
        [Parameter(Mandatory)][string]$Url
    )

    $response = Send-CDPMessage `
        -WebSocketUrl $Tab.webSocketDebuggerUrl `
        -Method "Page.navigate" `
        -Params @{ url = $Url }

    if ($response.result.frameId) {
        Write-Host "[+] Navigated to: $Url" -ForegroundColor Green
    } else {
        Write-Warning "Navigation may have failed. Response: $($response | ConvertTo-Json)"
    }
    return $response.result
}

# --- PUBLIC: Screenshot Capture ---

function Invoke-EdgeScreenshot {
    <#
    .SYNOPSIS
        Captures a full-page screenshot of the target tab and saves it as PNG.
    .EXAMPLE
        Invoke-EdgeScreenshot -Tab $tab -OutputPath "C:\temp\screenshot.png"
    #>
    param(
        [Parameter(Mandatory)][PSCustomObject]$Tab,
        [string]$OutputPath = "C:\temp\edge_screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"
    )

    $response = Send-CDPMessage `
        -WebSocketUrl $Tab.webSocketDebuggerUrl `
        -Method "Page.captureScreenshot" `
        -Params @{ format = "png"; captureBeyondViewport = $true }

    if ($response.result.data) {
        $bytes = [Convert]::FromBase64String($response.result.data)
        [IO.File]::WriteAllBytes($OutputPath, $bytes)
        Write-Host "[+] Screenshot saved: $OutputPath" -ForegroundColor Green
        return $OutputPath
    } else {
        Write-Warning "Screenshot capture failed."
        return $null
    }
}

Write-Host "[*] Edge CDP Network Controller loaded." -ForegroundColor Cyan
Write-Host "    Functions available:" -ForegroundColor DarkGray
Write-Host "      Select-EdgeTab       — Pick a target tab" -ForegroundColor White
Write-Host "      Invoke-EdgeJS        — Execute raw JavaScript" -ForegroundColor White
Write-Host "      Invoke-EdgeClick     — Click by CSS selector" -ForegroundColor White
Write-Host "      Invoke-EdgeExtract   — Extract data by CSS selector" -ForegroundColor White
Write-Host "      Invoke-EdgeFill      — Fill input fields" -ForegroundColor White
Write-Host "      Invoke-EdgeNavigate  — Navigate to URL" -ForegroundColor White
Write-Host "      Invoke-EdgeScreenshot — Capture screenshot`n" -ForegroundColor White
