# GitHub Repository Commands

Create a new GitHub repository, for example:

```text
thermal-control-qa-framework
```

Then run the following commands from the project root:

```bash
git init
git add .
git commit -m "Add Robot Framework thermal control QA validation framework"
git branch -M main
git remote add origin https://github.com/<your-github-username>/thermal-control-qa-framework.git
git push -u origin main
```

## Local validation before pushing

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
ruff check src tests
robot -d results/robot robot_tests
pytest -v
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="src"
ruff check src tests
robot -d results/robot robot_tests
pytest -v
```
