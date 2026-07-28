<#
.SYNOPSIS
    Stages, commits, and pushes Genesis Harness changes with safety checks.

.DESCRIPTION
    Runs a sequence of gates before touching git history. Any failed gate aborts
    the whole operation without staging or committing anything.

    Gates, in order:
      1. Repository check      - are we in the expected git repository
      2. Change check          - is there anything to commit
      3. Secret scan           - do staged changes contain credential-shaped content
      4. Large file check      - is anything unexpectedly large being committed
      5. Structure check       - does verify_structure.ps1 pass
      6. Session log check     - does a log exist for today
      7. Branch check          - confirm before committing directly to main
      8. Commit
      9. Push                  - only with -Push, and only after upstream check

.PARAMETER Message
    Commit message. Required unless -DryRun. Should follow the conventional format
    documented in CLAUDE.md section 6.1.

.PARAMETER Push
    Push to the tracked remote after a successful commit. Off by default.

.PARAMETER DryRun
    Run every gate and report, but do not stage, commit, or push.

.PARAMETER SkipStructureCheck
    Skip gate 5. Use only when verify_structure.ps1 is itself being changed.

.PARAMETER AllowNoSessionLog
    Skip gate 6. CLAUDE.md section 7.1 requires a session log for every change;
    this exists for mechanical commits (typo fixes, .gitignore) only.

.PARAMETER Force
    Bypass the interactive confirmation on gate 7. Does NOT bypass any other gate.

.EXAMPLE
    pwsh -File scripts/auto_commit.ps1 -Message "docs: clarify handoff contract" -DryRun

.EXAMPLE
    pwsh -File scripts/auto_commit.ps1 -Message "feat: add benchmark runner" -Push

.NOTES
    This script never force-pushes, never rewrites history, and never uses --no-verify.
    Those are constitutional prohibitions (CLAUDE.md section 6.2).
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Message,

    [switch]$Push,
    [switch]$DryRun,
    [switch]$SkipStructureCheck,
    [switch]$AllowNoSessionLog,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot        = Split-Path -Parent $PSScriptRoot
$MaxFileSizeKB   = 512
$ProtectedBranch = 'main'

# Credential-shaped patterns. Deliberately conservative: this gate is a tripwire,
# not a substitute for a real secret scanner.
$SecretPatterns = @(
    @{ Name = 'AWS access key';      Pattern = 'AKIA[0-9A-Z]{16}' },
    @{ Name = 'Private key block';   Pattern = '-----BEGIN [A-Z ]*PRIVATE KEY-----' },
    @{ Name = 'GitHub token';        Pattern = 'gh[pousr]_[A-Za-z0-9]{36,}' },
    @{ Name = 'Slack token';         Pattern = 'xox[baprs]-[A-Za-z0-9-]{10,}' },
    @{ Name = 'Anthropic API key';   Pattern = 'sk-ant-[A-Za-z0-9_\-]{20,}' },
    @{ Name = 'Generic API key';     Pattern = '(?i)(api[_-]?key|apikey)\s*[:=]\s*["`''][A-Za-z0-9_\-]{16,}["`'']' },
    @{ Name = 'Generic secret';      Pattern = '(?i)(secret|password|passwd|pwd)\s*[:=]\s*["`''][^"`''\s]{8,}["`'']' },
    @{ Name = 'Bearer token';        Pattern = '(?i)bearer\s+[A-Za-z0-9_\-\.]{24,}' },
    @{ Name = 'Connection string';   Pattern = '(?i)(mongodb|postgres|postgresql|mysql|redis)://[^:\s]+:[^@\s]+@' }
)

# Paths whose contents legitimately contain the patterns above (they document them).
$SecretScanExclusions = @(
    'scripts/auto_commit.ps1',
    'configs/quality_gates.json'
)

$script:GateNumber = 0

function Write-Gate {
    param([string]$Name)
    $script:GateNumber++
    Write-Host ''
    Write-Host ("[{0}] {1}" -f $script:GateNumber, $Name) -ForegroundColor Cyan
}

function Write-Pass { param([string]$Text) Write-Host "    PASS  $Text" -ForegroundColor Green }
function Write-Warn { param([string]$Text) Write-Host "    WARN  $Text" -ForegroundColor Yellow }
function Write-Skip { param([string]$Text) Write-Host "    SKIP  $Text" -ForegroundColor DarkGray }

function Stop-WithFailure {
    param([string]$Gate, [string]$Reason, [string]$Remedy)
    Write-Host "    FAIL  $Reason" -ForegroundColor Red
    Write-Host ''
    Write-Host "ABORTED at gate: $Gate" -ForegroundColor Red
    Write-Host "Nothing was staged, committed, or pushed." -ForegroundColor Red
    if ($Remedy) { Write-Host "Remedy: $Remedy" -ForegroundColor Yellow }
    exit 1
}

function Invoke-Git {
    param([string[]]$Arguments)
    $output = & git -C $RepoRoot @Arguments 2>&1
    return [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output   = ($output | Out-String).TrimEnd()
    }
}

Write-Host ''
Write-Host '=== Genesis Harness - auto_commit ===' -ForegroundColor White
Write-Host "Repository: $RepoRoot"
if ($DryRun) { Write-Host 'Mode: DRY RUN (no changes will be made)' -ForegroundColor Yellow }

# ---------------------------------------------------------------- Gate 1: repository
Write-Gate 'Repository check'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Stop-WithFailure 'Repository check' 'git is not available on PATH.' 'Install git, or add it to PATH.'
}

$insideRepo = Invoke-Git @('rev-parse', '--is-inside-work-tree')
if ($insideRepo.ExitCode -ne 0 -or $insideRepo.Output.Trim() -ne 'true') {
    Stop-WithFailure 'Repository check' "$RepoRoot is not a git repository." 'Run this script from within the Genesis Harness repository.'
}
Write-Pass "git repository confirmed"

# ---------------------------------------------------------------- Gate 2: changes exist
Write-Gate 'Change check'

# --untracked-files=all expands new directories into individual files. Without it, git
# reports "?? newdir/" and the secret scan in gate 3 never opens anything inside it.
$status = Invoke-Git @('status', '--porcelain', '--untracked-files=all')
if ([string]::IsNullOrWhiteSpace($status.Output)) {
    Write-Host '    Nothing to commit. Working tree is clean.' -ForegroundColor DarkGray
    Write-Host ''
    Write-Host 'DONE — no action taken.' -ForegroundColor Green
    exit 0
}

$changedLines = $status.Output -split "`r?`n" | Where-Object { $_ -ne '' }
Write-Pass "$($changedLines.Count) changed path(s)"
foreach ($line in $changedLines | Select-Object -First 20) {
    Write-Host "          $line" -ForegroundColor DarkGray
}
if ($changedLines.Count -gt 20) {
    Write-Host "          ... and $($changedLines.Count - 20) more" -ForegroundColor DarkGray
}

if (-not $DryRun -and [string]::IsNullOrWhiteSpace($Message)) {
    Stop-WithFailure 'Change check' 'No commit message supplied.' 'Pass -Message "<type>: <description>" (see CLAUDE.md section 6.1).'
}

# ---------------------------------------------------------------- Gate 3: secret scan
Write-Gate 'Secret scan'

# Resolve the set of files that would be committed, without staging them.
$candidateFiles = @()
foreach ($line in $changedLines) {
    if ($line.Length -lt 4) { continue }
    $indicator = $line.Substring(0, 2)
    $path      = $line.Substring(3).Trim('"')

    # Renames appear as "old -> new"; only the destination exists on disk.
    if ($path -match '^(?<old>.+?)\s+->\s+(?<new>.+)$') { $path = $Matches['new'] }
    # Deletions have nothing to scan.
    if ($indicator -match 'D') { continue }

    $candidateFiles += $path
}
$candidateFiles = $candidateFiles | Sort-Object -Unique

$secretFindings = @()
$scannedCount   = 0

foreach ($relativePath in $candidateFiles) {
    if ($SecretScanExclusions -contains $relativePath) {
        Write-Skip "$relativePath (documents the patterns it would match)"
        continue
    }

    $fullPath = Join-Path $RepoRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) { continue }

    # Skip binaries by extension — scanning them produces noise, not findings.
    if ($relativePath -match '\.(png|jpg|jpeg|gif|ico|pdf|zip|gz|7z|exe|dll|so|dylib|bin|woff2?|ttf|mp[34]|wav)$') { continue }

    $item = Get-Item -LiteralPath $fullPath
    if ($item.Length -gt 5MB) {
        Write-Skip "$relativePath (over 5 MB, not scanned)"
        continue
    }

    $content = Get-Content -LiteralPath $fullPath -Raw -ErrorAction SilentlyContinue
    if ($null -eq $content) { continue }
    $scannedCount++

    foreach ($rule in $SecretPatterns) {
        $match = [regex]::Match($content, $rule.Pattern)
        if ($match.Success) {
            # Report the line number, never the matched value.
            $prefix     = $content.Substring(0, $match.Index)
            $lineNumber = ($prefix -split "`n").Count
            $secretFindings += [pscustomobject]@{
                File = $relativePath
                Line = $lineNumber
                Rule = $rule.Name
            }
        }
    }
}

if ($secretFindings.Count -gt 0) {
    Write-Host '    Potential secrets detected:' -ForegroundColor Red
    foreach ($f in $secretFindings) {
        Write-Host ("          {0}:{1}  [{2}]" -f $f.File, $f.Line, $f.Rule) -ForegroundColor Red
    }
    Stop-WithFailure 'Secret scan' "$($secretFindings.Count) potential secret(s) found." 'Remove the credential and rotate it. If this is a false positive, add the path to $SecretScanExclusions with a comment explaining why.'
}
Write-Pass "$scannedCount file(s) scanned, no credential patterns found"

# ---------------------------------------------------------------- Gate 4: large files
Write-Gate 'Large file check'

$largeFiles = @()
foreach ($relativePath in $candidateFiles) {
    $fullPath = Join-Path $RepoRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) { continue }
    $sizeKB = [math]::Round((Get-Item -LiteralPath $fullPath).Length / 1KB, 1)
    if ($sizeKB -gt $MaxFileSizeKB) {
        $largeFiles += [pscustomobject]@{ File = $relativePath; SizeKB = $sizeKB }
    }
}

if ($largeFiles.Count -gt 0) {
    foreach ($f in $largeFiles) {
        Write-Warn ("{0} is {1} KB (threshold {2} KB)" -f $f.File, $f.SizeKB, $MaxFileSizeKB)
    }
    Write-Warn 'Large files are not blocked, but confirm they belong in version control.'
} else {
    Write-Pass "no file exceeds $MaxFileSizeKB KB"
}

# ---------------------------------------------------------------- Gate 5: structure
Write-Gate 'Structure check'

$verifyScript = Join-Path $PSScriptRoot 'verify_structure.ps1'
if ($SkipStructureCheck) {
    Write-Skip 'skipped by -SkipStructureCheck'
} elseif (-not (Test-Path -LiteralPath $verifyScript)) {
    Write-Warn 'verify_structure.ps1 not found — structure was not verified.'
} else {
    & pwsh -NoProfile -File $verifyScript -Quiet
    if ($LASTEXITCODE -ne 0) {
        Stop-WithFailure 'Structure check' 'verify_structure.ps1 reported failures.' 'Run: pwsh -File scripts/verify_structure.ps1  — then fix what it reports.'
    }
    Write-Pass 'repository structure verified'
}

# ---------------------------------------------------------------- Gate 6: session log
Write-Gate 'Session log check'

$today       = Get-Date -Format 'yyyy-MM-dd'
$sessionsDir = Join-Path $RepoRoot 'logs\sessions'

if ($AllowNoSessionLog) {
    Write-Skip 'skipped by -AllowNoSessionLog'
} elseif (-not (Test-Path -LiteralPath $sessionsDir)) {
    Stop-WithFailure 'Session log check' 'logs/sessions does not exist.' 'Run: pwsh -File scripts/new_session_log.ps1 -Slug "<slug>"'
} else {
    $todaysLogs = @(Get-ChildItem -LiteralPath $sessionsDir -Filter "$today*.md" -File -ErrorAction SilentlyContinue)
    if ($todaysLogs.Count -eq 0) {
        Stop-WithFailure 'Session log check' "No session log for $today." 'Run: pwsh -File scripts/new_session_log.ps1 -Slug "<slug>"   (CLAUDE.md section 7.1 requires one per session.)'
    }
    Write-Pass "$($todaysLogs.Count) session log(s) for $today"
}

# ---------------------------------------------------------------- Gate 7: branch
Write-Gate 'Branch check'

$branchResult = Invoke-Git @('rev-parse', '--abbrev-ref', 'HEAD')
$branch = $branchResult.Output.Trim()
Write-Host "    Current branch: $branch"

if ($branch -eq $ProtectedBranch -and -not $Force -and -not $DryRun) {
    Write-Warn "Committing directly to '$ProtectedBranch'."
    $answer = Read-Host "    Continue? (y/N)"
    if ($answer -notmatch '^[Yy]') {
        Write-Host ''
        Write-Host 'ABORTED by operator. Nothing was staged or committed.' -ForegroundColor Yellow
        exit 1
    }
    Write-Pass 'confirmed by operator'
} elseif ($branch -eq $ProtectedBranch -and $Force) {
    Write-Skip "confirmation bypassed by -Force"
} else {
    Write-Pass "on '$branch'"
}

# ---------------------------------------------------------------- Dry run exit
if ($DryRun) {
    Write-Host ''
    Write-Host 'DRY RUN COMPLETE - all gates evaluated, nothing was changed.' -ForegroundColor Yellow
    if ($Message) { Write-Host "Would commit with message: $Message" -ForegroundColor DarkGray }
    else { Write-Host 'No -Message supplied; a real run would abort at gate 2.' -ForegroundColor DarkGray }
    exit 0
}

# ---------------------------------------------------------------- Gate 8: commit
Write-Gate 'Commit'

$addResult = Invoke-Git @('add', '--all')
if ($addResult.ExitCode -ne 0) {
    Stop-WithFailure 'Commit' "git add failed: $($addResult.Output)" 'Resolve the git error and retry.'
}

$staged = Invoke-Git @('diff', '--cached', '--name-only')
if ([string]::IsNullOrWhiteSpace($staged.Output)) {
    Write-Warn 'Nothing staged after git add (all changes may be ignored). No commit made.'
    exit 0
}

$commitResult = Invoke-Git @('commit', '-m', $Message)
if ($commitResult.ExitCode -ne 0) {
    Stop-WithFailure 'Commit' "git commit failed: $($commitResult.Output)" 'If a hook failed, fix the cause. Never use --no-verify (CLAUDE.md section 6.2).'
}

$sha = (Invoke-Git @('rev-parse', '--short', 'HEAD')).Output.Trim()
Write-Pass "committed $sha"
Write-Host "          $Message" -ForegroundColor DarkGray

# ---------------------------------------------------------------- Gate 9: push
Write-Gate 'Push'

if (-not $Push) {
    Write-Skip 'not requested (pass -Push to push)'
    Write-Host ''
    Write-Host "DONE - committed $sha, not pushed." -ForegroundColor Green
    exit 0
}

$remotes = Invoke-Git @('remote')
if ([string]::IsNullOrWhiteSpace($remotes.Output)) {
    Write-Warn 'No remote configured. Commit succeeded; nothing to push.'
    exit 0
}

$upstream = Invoke-Git @('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')
if ($upstream.ExitCode -ne 0) {
    Write-Host "    No upstream for '$branch'. Setting it on push." -ForegroundColor DarkGray
    $pushResult = Invoke-Git @('push', '--set-upstream', 'origin', $branch)
} else {
    $pushResult = Invoke-Git @('push')
}

if ($pushResult.ExitCode -ne 0) {
    Write-Host "    FAIL  git push failed:" -ForegroundColor Red
    Write-Host "          $($pushResult.Output)" -ForegroundColor Red
    Write-Host ''
    Write-Host "The commit ($sha) is intact locally. Resolve the push error and retry." -ForegroundColor Yellow
    Write-Host 'Do not force-push (CLAUDE.md section 6.2).' -ForegroundColor Yellow
    exit 1
}

Write-Pass 'pushed'
Write-Host ''
Write-Host "DONE - committed $sha and pushed to origin/$branch." -ForegroundColor Green
exit 0
