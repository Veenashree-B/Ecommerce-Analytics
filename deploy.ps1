# =================================================================
# E-COMMERCE ANALYTICS - GIT UPDATE SCRIPT (PowerShell)
# =================================================================
# Run this script to verify and deploy the project to GitHub

Write-Host "`n" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  E-COMMERCE ANALYTICS - DEPLOYMENT SCRIPT" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# ==================== STEP 1: VERIFY PROJECT ====================
Write-Host "`n📋 STEP 1: VERIFYING PROJECT SETUP" -ForegroundColor Yellow
Write-Host "────────────────────────────────────" -ForegroundColor Yellow

if (Test-Path "verify_setup.py") {
    python verify_setup.py
    $verifyResult = $?
} else {
    Write-Host "❌ verify_setup.py not found!" -ForegroundColor Red
    $verifyResult = $false
}

if (-not $verifyResult) {
    Write-Host "`n⚠️  Verification failed. Please fix issues before deploying." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# ==================== STEP 2: CHECK GIT STATUS ====================
Write-Host "`n📋 STEP 2: CHECKING GIT STATUS" -ForegroundColor Yellow
Write-Host "────────────────────────────────" -ForegroundColor Yellow

git status

# ==================== STEP 3: STAGE CHANGES ====================
Write-Host "`n📝 STEP 3: STAGING ALL CHANGES" -ForegroundColor Yellow
Write-Host "───────────────────────────────" -ForegroundColor Yellow

git add -A
Write-Host "✅ All changes staged!" -ForegroundColor Green

# Ask for confirmation
Write-Host "`nReady to commit and push?" -ForegroundColor Cyan
Write-Host "Review changes above (if any). Continue? (Y/N)" -ForegroundColor Cyan
$response = Read-Host

if ($response -ne "Y" -and $response -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

# ==================== STEP 4: COMMIT ====================
Write-Host "`n💾 STEP 4: COMMITTING CHANGES" -ForegroundColor Yellow
Write-Host "──────────────────────────────" -ForegroundColor Yellow

$commitMessage = @"
Fix: Update dependencies for Python 3.13 compatibility and fix dashboard paths

- Update pandas 2.0.3 to 2.2.0+ for Python 3.13 support
- Update numpy 1.24.3 to 2.0.0+ (removes distutils dependency)
- Add pyproject.toml for better pip dependency resolution
- Add .streamlit/config.toml for Streamlit Cloud configuration
- Add .gitignore to exclude unnecessary files
- Fix dashboard app.py to use absolute paths for file loading
- Add verify_setup.py script for project verification
- Add comprehensive deployment and documentation guides
"@

git commit -m $commitMessage

$commitResult = $?

if (-not $commitResult) {
    Write-Host "⚠️  No changes to commit or commit failed." -ForegroundColor Yellow
} else {
    Write-Host "✅ Changes committed!" -ForegroundColor Green
}

# ==================== STEP 5: PUSH ====================
Write-Host "`n🚀 STEP 5: PUSHING TO GITHUB" -ForegroundColor Yellow
Write-Host "────────────────────────────" -ForegroundColor Yellow

git push origin main

$pushResult = $?

if ($pushResult) {
    Write-Host "`n✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Go to https://share.streamlit.io" -ForegroundColor Cyan
    Write-Host "2. Find 'ecommerce-analytics' app" -ForegroundColor Cyan
    Write-Host "3. Click ⋯ menu → Reboot app" -ForegroundColor Cyan
    Write-Host "4. Wait 2-3 minutes for rebuild" -ForegroundColor Cyan
    Write-Host "5. Your app will be live! 🎉" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Push failed. Check your GitHub credentials." -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "- Run: git remote -v (check remote URL)" -ForegroundColor Yellow
    Write-Host "- Run: git pull origin main (sync first)" -ForegroundColor Yellow
    Write-Host "- Check GitHub credentials are configured" -ForegroundColor Yellow
}

# ==================== FINAL MESSAGE ====================
Write-Host "`n" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  DEPLOYMENT PROCESS COMPLETE" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
