@echo off

where hugo >nul 2>nul
if %errorlevel% neq 0 (
    echo Hugo not found. Installing via winget...
    where winget >nul 2>nul
    if %errorlevel% neq 0 (
        echo Error: winget is not available. Install Hugo manually: https://gohugo.io/installation/
        exit /b 1
    )
    winget install Hugo.Hugo.Extended
    echo Hugo installed. You may need to restart your terminal, then re-run this script.
    exit /b 0
)

if not exist "themes\hugo-bearblog\theme.toml" (
    echo Initializing theme submodule...
    git submodule update --init --recursive
)

echo Starting Hugo dev server...
hugo server -D
