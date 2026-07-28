<#
.SYNOPSIS
    Creates a new Genesis Harness session log from the template.

.DESCRIPTION
    Copies logs/SESSION_TEMPLATE.md to logs/sessions/YYYY-MM-DD_NN_<slug>.md, choosing
    the next available sequence number for today and stamping the header fields it can
    determine automatically.

    Refuses to overwrite an existing log. Session logs are append-only
    (CLAUDE.md section 7.3).

.PARAMETER Slug
    Short kebab-case description of the session. Required.

.PARAMETER Model
    Model identifier to record. Defaults to a placeholder for the operator to fill in.

.PARAMETER Agents
    Comma-separated list of agents used. Optional.

.EXAMPLE
    pwsh -File scripts/new_session_log.ps1 -Slug "foundation-architecture"

.EXAMPLE
    pwsh -File scripts/new_session_log.ps1 -Slug "benchmark-runner" -Model "claude-opus-5" -Agents "architect,coding,qa"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Slug,

    [string]$Model  = '<fill in: exact model id>',
    [string]$Agents = '<fill in>'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot     = Split-Path -Parent $PSScriptRoot
$TemplatePath = Join-Path $RepoRoot 'logs\SESSION_TEMPLATE.md'
$SessionsDir  = Join-Path $RepoRoot 'logs\sessions'

# Normalise the slug rather than rejecting near-misses; the operator's intent is clear.
$normalisedSlug = ($Slug.Trim().ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-')

if ([string]::IsNullOrWhiteSpace($normalisedSlug)) {
    Write-Host "FAIL  Slug '$Slug' contains no usable characters." -ForegroundColor Red
    Write-Host "      Use a short kebab-case description, e.g. -Slug 'foundation-architecture'" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path -LiteralPath $TemplatePath)) {
    Write-Host "FAIL  Template not found: logs/SESSION_TEMPLATE.md" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath $SessionsDir)) {
    New-Item -ItemType Directory -Path $SessionsDir -Force | Out-Null
    Write-Host "      Created logs/sessions/" -ForegroundColor DarkGray
}

$today = Get-Date -Format 'yyyy-MM-dd'

# Next sequence number for today. Existing logs are never renumbered.
$existing = @(Get-ChildItem -LiteralPath $SessionsDir -Filter "$today`_*.md" -File -ErrorAction SilentlyContinue)
$sequence = '{0:D2}' -f ($existing.Count + 1)

$fileName = "${today}_${sequence}_${normalisedSlug}.md"
$fullPath = Join-Path $SessionsDir $fileName

if (Test-Path -LiteralPath $fullPath) {
    Write-Host "FAIL  $fileName already exists." -ForegroundColor Red
    Write-Host "      Session logs are append-only. Use a different slug, or edit the existing log." -ForegroundColor Yellow
    exit 1
}

$sessionId = "${today}_${sequence}_${normalisedSlug}"

$content = Get-Content -LiteralPath $TemplatePath -Raw
$content = $content -replace '(?m)^# Session Log — <slug>$',                    "# Session Log — $normalisedSlug"
$content = $content -replace '(?m)^\*\*Session ID:\*\* YYYY-MM-DD_NN_<slug>$',  "**Session ID:** $sessionId"
$content = $content -replace '(?m)^\*\*Date:\*\* YYYY-MM-DD$',                  "**Date:** $today"
$content = $content -replace '(?m)^\*\*Model:\*\* <exact model id, e\.g\. claude-opus-5>$', "**Model:** $Model"
$content = $content -replace '(?m)^\*\*Agents used:\*\* <architect, coding, qa — or "none \(direct\)">$', "**Agents used:** $Agents"

Set-Content -LiteralPath $fullPath -Value $content -Encoding UTF8

Write-Host ''
Write-Host "Created logs/sessions/$fileName" -ForegroundColor Green
Write-Host ''
Write-Host 'Remember (CLAUDE.md section 7):' -ForegroundColor DarkGray
Write-Host '  - The reasoning summary is the point. Record why, including options rejected.' -ForegroundColor DarkGray
Write-Host '  - The tests section takes real command output. "Not run" is honest; invention is not.' -ForegroundColor DarkGray
Write-Host '  - Next actions must be executable by a fresh agent with no memory of this session.' -ForegroundColor DarkGray
Write-Host ''

exit 0
