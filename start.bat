@echo off
color 0A
echo ========================================
echo         DRISHTI-AI Starting...
echo ========================================
echo.

echo [1/2] Starting Backend API...
start cmd /k "cd C:\Drishti-AI && C:\Drishti-AI\.venv\Scripts\activate.bat && uvicorn main:app --reload"

echo Waiting for backend to load...
timeout /t 8 /nobreak

echo [2/2] Starting Streamlit UI...
start cmd /k "cd C:\Drishti-AI && C:\Drishti-AI\.venv\Scripts\activate.bat && streamlit run ui.py"

echo.
echo ========================================
echo  DRISHTI-AI is running!
echo  Open browser: http://localhost:8501
echo ========================================
timeout /t 3 /nobreak

start http://localhost:8501
```

---

## How to create the file:

**Step 1** — Open Notepad

**Step 2** — Paste the code above

**Step 3** — Click File → Save As

**Step 4** — Set filename as:
```
start.bat
```

**Step 5** — Set "Save as type" to:
```
All Files (*.*)