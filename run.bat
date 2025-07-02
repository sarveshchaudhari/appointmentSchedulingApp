@ECHO OFF
CLS
ECHO.
ECHO ===============================================
ECHO   Appointment Agent Application Launcher
ECHO ===============================================
ECHO.

:: --- Prerequisite Check: Python ---
ECHO [STEP 1] Checking for Python installation...
python --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERROR] Python is not installed or not found in your system's PATH.
    ECHO Please install Python 3.9+ from python.org and ensure it's added to PATH.
    ECHO.
    PAUSE
    EXIT /B
)
ECHO [SUCCESS] Python found.
ECHO.

:: --- Virtual Environment Setup ---
ECHO [STEP 2] Setting up Python virtual environment...
IF NOT EXIST venv (
    ECHO  - Virtual environment not found. Creating one...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        ECHO [ERROR] Failed to create virtual environment.
        PAUSE
        EXIT /B
    )
) ELSE (
    ECHO  - Virtual environment already exists.
)

:: Activate the virtual environment
CALL venv\Scripts\activate

ECHO [SUCCESS] Virtual environment is active.
ECHO.

:: --- Dependency Installation ---
ECHO [STEP 3] Installing required packages from requirements.txt...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERROR] Failed to install required packages. Check your internet connection.
    PAUSE
    EXIT /B
)
ECHO [SUCCESS] All packages are installed.
ECHO.

:: --- API Key Input ---
ECHO [STEP 4] Please provide your API Key.
SET /P "GOOGLE_API_KEY=Enter your GOOGLE_API_KEY and press Enter: "

IF "%GOOGLE_API_KEY%"=="" (
    ECHO.
    ECHO [ERROR] No API key was entered. Aborting.
    PAUSE
    EXIT /B
)
ECHO.

:: --- Run the Application ---
ECHO [STEP 5] Starting the Appointment Scheduling Assistant...
ECHO The application will open in your web browser.
ECHO Close this window or press CTRL+C to stop the application.
ECHO.

:: The GOOGLE_API_KEY is now set as an environment variable for this session.
:: The python script will be able to access it with os.getenv()
python main.py

ECHO.
ECHO Application has been closed.
PAUSE
