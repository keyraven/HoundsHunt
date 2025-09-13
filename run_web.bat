CALL venv\Scripts\activate.bat
start "pygbag_hosting" pygbag --ume_block 0 main.py

IF "%~1"=="debug" (
     start "web_browser" "http://localhost:8000#debug"
    ) 
ELSE (
    start "web_browser" "http://localhost:8000"
 )
