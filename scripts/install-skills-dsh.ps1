# Install pickled-fish skills into the DSH user skill root (~/.dsh/skills) on Windows.
# DSH discovers directory-bundle skills at <root>/<name>/SKILL.md, so each skill
# gets its own entry. Junctions keep a single source of truth: edits and
# `git pull` in this repo take effect immediately, with a copy fallback.
#
# Usage:  pwsh -File scripts/install-skills-dsh.ps1 [-Dest <dir>]
param(
    [string]$Dest = (Join-Path $HOME ".dsh\skills")
)

$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $PSScriptRoot
New-Item -ItemType Directory -Force -Path $Dest | Out-Null

# name -> source. "knowledge" is an entry point only (no SKILL.md), so the packs
# stay reachable when kb-rag is loaded without the pickled-fish umbrella skill.
$links = [ordered]@{
    "pickled-fish"         = $ROOT
    "wechat-mac-export"    = Join-Path $ROOT "skills\wechat-mac-export"
    "wechat-win-export"    = Join-Path $ROOT "skills\wechat-win-export"
    "wechat-win-export-v4" = Join-Path $ROOT "skills\wechat-win-export-v4"
    "qingsheng"            = Join-Path $ROOT "skills\qingsheng"
    "kb-rag"               = Join-Path $ROOT "skills\kb-rag"
    "knowledge"            = Join-Path $ROOT "knowledge"
}

foreach ($name in $links.Keys) {
    $source = $links[$name]
    $target = Join-Path $Dest $name
    if (-not (Test-Path -LiteralPath $source)) {
        Write-Warning "Skipped (missing source): $source"
        continue
    }
    if (Test-Path -LiteralPath $target) {
        # Removes the link/copy itself; Remove-Item does not follow the junction.
        Remove-Item -Force -Recurse -LiteralPath $target
    }
    try {
        New-Item -ItemType Junction -Path $target -Target $source | Out-Null
        Write-Host "Linked: $target"
    }
    catch {
        Copy-Item -Recurse -Force -LiteralPath $source -Destination $target
        Write-Host "Copied (junction unavailable): $target"
    }
}

Write-Host "Installed into: $Dest"
Write-Host "Verify: read <Dest>\pickled-fish\SKILL.md, then call the 'pickled-fish' skill."
