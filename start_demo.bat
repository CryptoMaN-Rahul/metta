@echo off
echo Domain-Specific FAQ Chatbot with Knowledge Graph Integration
echo =========================================================

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file...
    echo Please enter your Gemini API key:
    set /p API_KEY=
    echo GEMINI_API_KEY=%API_KEY%> .env
)

REM Start the demo
echo Starting demo...
python start_demo.py

pause 