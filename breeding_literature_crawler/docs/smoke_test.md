# Smoke Test

This smoke test provides a minimal local validation path that does not trigger full crawling or require large datasets.

It checks that dependencies are installed, Python files compile, entry scripts can be imported safely, and the documentation site can build.

## Prerequisites

- Python 3.10 or later
- Repository root as the current working directory
- Virtual environment created and activated

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

For documentation checks:

```powershell
pip install -r requirements-docs.txt
```

## Step 1: Python Compile Check

This check compiles files under `src/` and `scripts/`. It does not run retrieval jobs.

```powershell
@'
from pathlib import Path
import py_compile

root = Path(".")
for path in list((root / "src").rglob("*.py")) + list((root / "scripts").glob("*.py")):
    py_compile.compile(str(path), doraise=True)
print("py_compile ok")
'@ | .\.venv\Scripts\python.exe -
```

Expected result:

```text
py_compile ok
```

## Step 2: Entry Script Import Check

This check imports entry scripts with a non-main run name. It should not call `main()` and should not start full retrieval.

```powershell
@'
import runpy

scripts = [
    "scripts/run_pubmed.py",
    "scripts/run_arxiv.py",
    "scripts/download_biorxiv_dump.py",
    "scripts/run_biorxiv_local.py",
    "scripts/download_medrxiv_dump.py",
    "scripts/run_medrxiv_local.py",
    "scripts/download_chemrxiv_dump.py",
    "scripts/run_chemrxiv_local.py",
    "scripts/run_cleaning.py",
    "scripts/run_report.py",
]

for script in scripts:
    runpy.run_path(script, run_name="__smoke_test__")
    print(f"import ok: {script}")
'@ | .\.venv\Scripts\python.exe -
```

Expected result: each script prints `import ok: ...`.

## Step 3: Documentation Build

```powershell
python -m mkdocs build
```

or:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build
```

This validates the MkDocs navigation and Markdown page discovery.

## Optional Downstream Orientation

If you already have a small local raw JSONL sample, you can inspect downstream behavior with:

```powershell
.\.venv\Scripts\python.exe scripts\run_cleaning.py
.\.venv\Scripts\python.exe scripts\run_report.py
```

Do not treat this as a full data quality test. It only confirms that downstream scripts can run against available local inputs.

## Boundaries

This smoke test does not validate:

- API availability
- full online retrieval success
- xRxiv dump download stability
- relevance filtering quality
- cleaned corpus quality
