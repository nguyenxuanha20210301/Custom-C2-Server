.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\src"
uvicorn app.main:app --reload --port 8000
