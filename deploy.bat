@echo off
REM =================================================================
REM E-COMMERCE ANALYTICS - GIT UPDATE SCRIPT
REM =================================================================

echo.
echo ======================================================================
echo   STEP 1: VERIFY PROJECT
echo ======================================================================
python verify_setup.py

echo.
echo ======================================================================
echo   STEP 2: CHECK GIT STATUS
echo ======================================================================
git status

echo.
echo ======================================================================
echo   STEP 3: STAGE ALL CHANGES
echo ======================================================================
git add -A
echo ✅ All changes staged!

echo.
echo ======================================================================
echo   STEP 4: COMMIT CHANGES
echo ======================================================================
git commit -m "Fix: Update dependencies for Python 3.13 compatibility

- Update pandas 2.0.3 to 2.2.0+ for Python 3.13 support
- Update numpy 1.24.3 to 2.0.0+ (removes distutils dependency)
- Add pyproject.toml for better pip dependency resolution
- Add .streamlit/config.toml for Streamlit Cloud configuration
- Add .gitignore to exclude unnecessary files
- Fix dashboard app.py to use absolute paths for file loading
- Add verify_setup.py script for project verification
- Add comprehensive deployment guide"

echo.
echo ======================================================================
echo   STEP 5: PUSH TO GITHUB
echo ======================================================================
echo Ready to push? Press Enter to continue or Ctrl+C to cancel...
pause

git push origin main

echo.
echo ======================================================================
echo   ✨ DEPLOYMENT COMPLETE!
echo ======================================================================
echo.
echo Next steps:
echo 1. Go to https://share.streamlit.io
echo 2. Find your app "ecommerce-analytics"
echo 3. Click menu (⋯) → Reboot app
echo 4. Wait 2-3 minutes for rebuild
echo 5. Your app should be live!
echo.
pause
