@echo off
REM Build Jarvis.exe on Windows. Requires Python 3.10 (64-bit) on PATH.
REM Run from the project folder:  build_exe.bat

where py >nul 2>nul
if %errorlevel%==0 (
    py -3.10 -m venv buildenv
) else (
    python -m venv buildenv
)
if errorlevel 1 goto :fail

call buildenv\Scripts\activate.bat
python -m pip install --upgrade pip wheel "setuptools<70"
pip install -r requirements-build.txt
if errorlevel 1 goto :fail

REM enum34 is an obsolete backport that breaks PyInstaller
pip uninstall -y enum34

pyinstaller --noconfirm Jarvis.spec
if errorlevel 1 goto :fail

echo.
echo Done. Your app is in dist\Jarvis\Jarvis.exe
echo Set GROQ_API_KEY (setx GROQ_API_KEY "your_key") for AI answers.
goto :eof

:fail
echo Build failed. Scroll up to see the error.
exit /b 1
