# Install skills into ~/.cursor/skills for Cursor discovery (Windows).
# Mirrors scripts/install-skills.sh, using junctions (no admin needed) with copy fallback.
$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $PSScriptRoot
$DEST = Join-Path $HOME ".cursor\skills"
New-Item -ItemType Directory -Force -Path $DEST | Out-Null

$links = [ordered]@{
    "pickled-fish"         = $ROOT
    "wechat-mac-export"    = Join-Path $ROOT "skills\wechat-mac-export"
    "wechat-win-export"    = Join-Path $ROOT "skills\wechat-win-export"
    "wechat-win-export-v4" = Join-Path $ROOT "skills\wechat-win-export-v4"
    "qingsheng"            = Join-Path $ROOT "skills\qingsheng"
    "kb-rag"               = Join-Path $ROOT "skills\kb-rag"
}

foreach ($name in $links.Keys) {
    $target = Join-Path $DEST $name
    $source = $links[$name]
    if (Test-Path $target) {
        Remove-Item -Force -Recurse $target -ErrorAction SilentlyContinue
    }
    try {
        New-Item -ItemType Junction -Path $target -Target $source | Out-Null
        Write-Host "Linked: $target"
    }
    catch {
        Copy-Item -Recurse -Force $source $target
        Write-Host "Copied (junction unavailable): $target"
    }
}

Write-Host "Knowledge packs live under: $ROOT\knowledge\"
Write-Host "Done."
