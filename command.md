active venv: .\.venv\Scripts\activate (root repo)
pip install -r server/requirements.txt


$env:DATABASE_URL = "postgresql://postgres:mypassword@db:5432/customc2"