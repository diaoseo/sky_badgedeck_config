@echo off
setlocal EnableDelayedExpansion
pushd "%~dp0"

set "GIT=C:\Program Files\Git\cmd\git.exe"
set "CURL=C:\Windows\System32\curl.exe"

rem --- locate python (gen_manifest.py needs it) ---
set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY ( where py >nul 2>&1 && set "PY=py" )
if not defined PY ( if exist "C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" set "PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" )
if not defined PY ( if exist "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe" set "PY=C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe" )
if not defined PY ( echo [ERR] python not found; pause; exit /b 1 )

echo [1/4] regenerate manifest.json
"%PY%" gen_manifest.py
if errorlevel 1 ( echo [ERR] manifest regen failed; pause; exit /b 1 )

echo [2/4] stage changes
"%GIT%" add -A

rem --- commit only if there is something staged ---
"%GIT%" diff --cached --quiet
if errorlevel 1 (
  for /f "delims=" %%t in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmmss"') do set TS=%%t
  "%GIT%" commit -m "release !TS!"
) else (
  echo [2/4] nothing new to commit
)

echo [3/4] push to main (enter your SSH passphrase when prompted)
"%GIT%" push origin main
if errorlevel 1 ( echo [ERR] push failed; pause; exit /b 1 )

echo [4/4] purge jsDelivr CDN cache for instant propagation
"%CURL%" -s -m 20 -o nul "https://purge.jsdelivr.net/gh/diaoseo/sky_badgedeck_config@main/resources/manifest.json"

echo.
echo [DONE] Pushed to main. Device URL (set this once in sys.html):
echo https://cdn.jsdelivr.net/gh/diaoseo/sky_badgedeck_config@main/
echo.
pause
