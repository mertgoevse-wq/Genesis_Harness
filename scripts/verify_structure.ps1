<#
.SYNOPSIS
    Verifies that the Genesis Harness repository structure is intact.

.DESCRIPTION
    Checks that every required directory and file exists, that every registered agent
    has both a charter and a runtime adapter, that every registered skill has a SKILL.md,
    and that no markdown file exceeds the size limit in CLAUDE.md section 8.1.

    Exit code 0 = all checks passed. Exit code 1 = at least one check failed.

    This script is gate 5 of scripts/auto_commit.ps1.

.PARAMETER Quiet
    Print only failures and the final summary line.

.EXAMPLE
    pwsh -File scripts/verify_structure.ps1

.EXAMPLE
    pwsh -File scripts/verify_structure.ps1 -Quiet
#>

[CmdletBinding()]
param(
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot     = Split-Path -Parent $PSScriptRoot
$MaxMarkdownLines = 800

$script:Passed = 0
$script:Failed = 0
$script:Warned = 0

function Write-Section {
    param([string]$Name)
    if (-not $Quiet) {
        Write-Host ''
        Write-Host "-- $Name" -ForegroundColor Cyan
    }
}

function Test-Item {
    param(
        [string]$Description,
        [bool]$Condition,
        [string]$Detail = ''
    )
    if ($Condition) {
        $script:Passed++
        if (-not $Quiet) { Write-Host "   PASS  $Description" -ForegroundColor Green }
    } else {
        $script:Failed++
        Write-Host "   FAIL  $Description" -ForegroundColor Red
        if ($Detail) { Write-Host "         $Detail" -ForegroundColor DarkGray }
    }
}

function Write-Warning-Item {
    param([string]$Description)
    $script:Warned++
    Write-Host "   WARN  $Description" -ForegroundColor Yellow
}

function Test-PathExists {
    param([string]$RelativePath, [string]$Type = 'Any')
    $full = Join-Path $RepoRoot $RelativePath
    if ($Type -eq 'Any') { return Test-Path -LiteralPath $full }
    return Test-Path -LiteralPath $full -PathType $Type
}

if (-not $Quiet) {
    Write-Host ''
    Write-Host '=== Genesis Harness — structure verification ===' -ForegroundColor White
    Write-Host "Repository: $RepoRoot"
}

# ------------------------------------------------------------------ Directories
Write-Section 'Required directories'

$RequiredDirectories = @(
    '.claude',
    '.claude/agents',
    'agents',
    'skills',
    'prompts',
    'prompts/system_layers',
    'prompts/master_prompts',
    'prompts/generators',
    'prompts/benchmarks',
    'logs',
    'logs/sessions',
    'docs',
    'scripts',
    'configs',
    'templates',
    'orchestration',
    'core',
    'core/model_router',
    'branding',
    'harvester/connectors',
    'harvester/knowledge_graph',
    'harvester/recommendation',
    'tests',
    'control-center',
    'control-center/backend',
    'control-center/events',
    'control-center/frontend',
    'genesis_runtime',
    'genesis_runtime/runtime',
    'genesis_runtime/planner',
    'genesis_runtime/agent_execution',
    'genesis_runtime/skill_system',
    'genesis_runtime/memory',
    'genesis_runtime/events',
    'memory_system',
    'memory_system/storage',
    'memory_system/retrieval',
    'memory_system/learning',
    'evolution',
    'evolution/evaluation',
    'evolution/optimization',
    'evolution/experiments',
    'evolution/proposals',
    'docs/evolution',
    'tool_intelligence',
    'tool_intelligence/registry',
    'tool_intelligence/discovery',
    'tool_intelligence/evaluator',
    'tool_intelligence/adapters',
    'tool_intelligence/recommendations',
    'mcp',
    'mcp/registry',
    'mcp/discovery',
    'mcp/adapters',
    'mcp/security',
    'product_factory',
    'product_factory/discovery',
    'product_factory/validation',
    'product_factory/strategy',
    'product_factory/product_management',
    'product_factory/ux',
    'product_factory/architecture',
    'product_factory/development',
    'product_factory/deployment',
    'product_factory/marketing',
    'product_factory/analytics',
    'product_factory/evaluation',
    'product_factory/pipeline',
    'docs/products',
    'founder_intelligence',
    'founder_intelligence/market_scanner',
    'founder_intelligence/idea_engine',
    'founder_intelligence/startup_analysis',
    'founder_intelligence/investor_engine',
    'founder_intelligence/validation',
    'docs/intelligence/trends',
    'docs/products/candidates',
    'docs/investment_reviews',
    'venture_pipeline',
    'venture_pipeline/pipeline',
    'venture_pipeline/discovery',
    'venture_pipeline/validation',
    'venture_pipeline/business',
    'venture_pipeline/investment',
    'venture_pipeline/decisions',
    'knowledge_graph',
    'agent_factory',
    'branding',
    'docs/intelligence/discoveries',
    'venture_execution',
    'venture_execution/orchestrator',
    'venture_execution/workflows',
    'venture_execution/checkpoints',
    'venture_execution/reports',
    'agent_collaboration',
    'skill_intelligence',
    'quality_intelligence',
    'execution_tools',
    'memory_system/project_memory',
    'software_factory',
    'software_factory/factory',
    'software_factory/planning',
    'software_factory/development',
    'software_factory/testing',
    'software_factory/review',
    'software_factory/deployment',
    'engineering_team',
    'coding_pipeline',
    'github_engine',
    'code_intelligence',
    'testing_intelligence',
    'security_intelligence',
    'memory_system/engineering_memory',
    'research_intelligence',
    'research_intelligence/research_engine',
    'research_intelligence/discovery',
    'research_intelligence/analysis',
    'research_intelligence/hypothesis',
    'research_intelligence/experiments',
    'research_intelligence/reports',
    'research_connectors',
    'research_benchmarks',
    'memory_system/research_memory',
    'docs/evolution/research_discoveries',
    'orchestrator'
)

foreach ($dir in $RequiredDirectories) {
    Test-Item "$dir/" (Test-PathExists $dir 'Container') "Expected directory not found."
}

# ------------------------------------------------------------------ Root files
Write-Section 'Root files'

$RequiredRootFiles = @(
    'CLAUDE.md',
    'README.md'
)

foreach ($file in $RequiredRootFiles) {
    Test-Item $file (Test-PathExists $file 'Leaf') "Expected file not found."
}

# ------------------------------------------------------------------ Documentation
Write-Section 'Documentation'

$RequiredDocs = @(
    'docs/ARCHITECTURE.md',
    'docs/AGENTS.md',
    'docs/WORKFLOW.md',
    'docs/ROADMAP.md'
)

foreach ($doc in $RequiredDocs) {
    $exists = Test-PathExists $doc 'Leaf'
    Test-Item $doc $exists "Expected documentation file not found."
    if ($exists) {
        $full = Join-Path $RepoRoot $doc
        if ((Get-Item -LiteralPath $full).Length -eq 0) {
            Write-Warning-Item "$doc exists but is empty."
        }
    }
}

# ------------------------------------------------------------------ Prompts
Write-Section 'Prompt framework'

$RequiredPrompts = @(
    'prompts/README.md',
    'prompts/system_layers/L0_identity.md',
    'prompts/system_layers/L1_operating_principles.md',
    'prompts/system_layers/L2_domain_context.md',
    'prompts/system_layers/L3_task_contract.md',
    'prompts/system_layers/L4_output_contract.md',
    'prompts/system_layers/L5_reasoning_layer.md',
    'prompts/master_prompts/project_analysis.md',
    'prompts/master_prompts/architecture.md',
    'prompts/master_prompts/coding.md',
    'prompts/master_prompts/research.md',
    'prompts/master_prompts/review.md',
    'prompts/generators/agent_generator.md',
    'prompts/generators/skill_generator.md',
    'prompts/generators/prompt_generator.md',
    'prompts/benchmarks/README.md',
    'prompts/benchmarks/rubric.md',
    'prompts/benchmarks/cases.md'
)

foreach ($p in $RequiredPrompts) {
    Test-Item $p (Test-PathExists $p 'Leaf') "Expected prompt file not found."
}

# ------------------------------------------------------------------ Logging
Write-Section 'Logging system'

Test-Item 'logs/SESSION_TEMPLATE.md' (Test-PathExists 'logs/SESSION_TEMPLATE.md' 'Leaf') "Session template missing."
Test-Item 'logs/README.md'           (Test-PathExists 'logs/README.md' 'Leaf')           "Logging README missing."

# ------------------------------------------------------------------ Templates
Write-Section 'Templates'

$RequiredTemplates = @(
    'templates/AGENT_TEMPLATE.md',
    'templates/SKILL_TEMPLATE.md',
    'templates/ADR_TEMPLATE.md',
    'templates/HANDOFF_TEMPLATE.md'
)

foreach ($t in $RequiredTemplates) {
    Test-Item $t (Test-PathExists $t 'Leaf') "Expected template not found."
}

# ------------------------------------------------------------------ Configs
Write-Section 'Configuration'

$RequiredConfigs = @(
    'configs/harness.config.json',
    'configs/quality_gates.json',
    'configs/model_routing.json'
)

foreach ($c in $RequiredConfigs) {
    $exists = Test-PathExists $c 'Leaf'
    Test-Item $c $exists "Expected config not found."
    if ($exists) {
        $full = Join-Path $RepoRoot $c
        try {
            Get-Content -LiteralPath $full -Raw | ConvertFrom-Json -ErrorAction Stop | Out-Null
            $script:Passed++
            if (-not $Quiet) { Write-Host "   PASS  $c parses as JSON" -ForegroundColor Green }
        } catch {
            $script:Failed++
            Write-Host "   FAIL  $c is not valid JSON" -ForegroundColor Red
            Write-Host "         $($_.Exception.Message)" -ForegroundColor DarkGray
        }
    }
}

# ------------------------------------------------------------------ Agents (registry-driven)
Write-Section 'Agents'

$configPath = Join-Path $RepoRoot 'configs/harness.config.json'
$registry   = $null

if (Test-Path -LiteralPath $configPath) {
    try { $registry = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json } catch { $registry = $null }
}

if ($null -eq $registry) {
    Write-Warning-Item 'harness.config.json unreadable — agent and skill checks skipped.'
} else {
    Test-Item 'agents/README.md' (Test-PathExists 'agents/README.md' 'Leaf') "Agent registry README missing."

    foreach ($agent in $registry.agents) {
        $charter = "agents/$($agent.id)/AGENT.md"
        $adapter = ".claude/agents/$($agent.id).md"
        Test-Item "$($agent.id): charter"  (Test-PathExists $charter 'Leaf') "Missing $charter"
        Test-Item "$($agent.id): adapter"  (Test-PathExists $adapter 'Leaf') "Missing $adapter"

        # The adapter must carry YAML frontmatter or Claude Code will not discover it.
        if (Test-PathExists $adapter 'Leaf') {
            $head = Get-Content -LiteralPath (Join-Path $RepoRoot $adapter) -TotalCount 1
            Test-Item "$($agent.id): adapter frontmatter" ($head -eq '---') "First line of $adapter must be '---'"
        }
    }

    # ------------------------------------------------------------------ Skills
    Write-Section 'Skills'

    Test-Item 'skills/README.md' (Test-PathExists 'skills/README.md' 'Leaf') "Skill registry README missing."

    foreach ($skill in $registry.skills) {
        $skillFile = "skills/$($skill.id)/SKILL.md"
        Test-Item "$($skill.id): SKILL.md" (Test-PathExists $skillFile 'Leaf') "Missing $skillFile"
    }
}

# ------------------------------------------------------------------ Scripts
Write-Section 'Scripts'

$RequiredScripts = @(
    'scripts/auto_commit.ps1',
    'scripts/verify_structure.ps1',
    'scripts/new_session_log.ps1'
)

foreach ($s in $RequiredScripts) {
    $exists = Test-PathExists $s 'Leaf'
    Test-Item $s $exists "Expected script not found."
    if ($exists) {
        # A syntax error here would abort a commit at gate 5, so check it explicitly.
        $full   = Join-Path $RepoRoot $s
        $tokens = $null
        $errors = $null
        [System.Management.Automation.Language.Parser]::ParseFile($full, [ref]$tokens, [ref]$errors) | Out-Null
        if ($errors.Count -gt 0) {
            $script:Failed++
            Write-Host "   FAIL  $s has $($errors.Count) syntax error(s)" -ForegroundColor Red
            Write-Host "         $($errors[0].Message)" -ForegroundColor DarkGray
        } else {
            $script:Passed++
            if (-not $Quiet) { Write-Host "   PASS  $s parses cleanly" -ForegroundColor Green }
        }
    }
}

# ------------------------------------------------------------------ Size limits
Write-Section 'Size limits'

$oversized = @()
$markdownFiles = Get-ChildItem -LiteralPath $RepoRoot -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' }

foreach ($md in $markdownFiles) {
    $lineCount = (Get-Content -LiteralPath $md.FullName | Measure-Object -Line).Lines
    if ($lineCount -gt $MaxMarkdownLines) {
        $relative = $md.FullName.Substring($RepoRoot.Length + 1).Replace('\', '/')
        $oversized += [pscustomobject]@{ File = $relative; Lines = $lineCount }
    }
}

if ($oversized.Count -eq 0) {
    $script:Passed++
    if (-not $Quiet) { Write-Host "   PASS  no markdown file exceeds $MaxMarkdownLines lines" -ForegroundColor Green }
} else {
    foreach ($f in $oversized) {
        Write-Warning-Item ("{0} is {1} lines (limit {2}) - CLAUDE.md section 8.1" -f $f.File, $f.Lines, $MaxMarkdownLines)
    }
}

# ------------------------------------------------------------------ Summary
Write-Host ''
$summary = "Structure verification: $script:Passed passed, $script:Failed failed, $script:Warned warning(s)."

if ($script:Failed -gt 0) {
    Write-Host $summary -ForegroundColor Red
    exit 1
}

Write-Host $summary -ForegroundColor Green
exit 0
