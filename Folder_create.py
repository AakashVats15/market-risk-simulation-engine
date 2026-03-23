import os

BASE_PATH = r"E:\Personal\GitHub\Python Code Repo\market-risk-simulation-engine"

# Folders to create
folders = [
    "config",
    "data/raw",
    "data/processed",
    "data/examples",
    "src",
    "src/utils",
    "scripts",
    "results/var_es_timeseries",
    "results/backtests",
    "results/stress_scenarios",
    "results/diagnostics",
    "results/plots",
    "tests",
    "docs",
]

# Files to create
files = [
    "README.md",
    "pyproject.toml",
    "setup.py",
    "requirements.txt",

    "config/default_config.yaml",
    "config/scenarios.yaml",
    "config/stress_tests.yaml",

    "src/__init__.py",
    "src/data_loader.py",
    "src/scenario_engine.py",
    "src/risk_measures.py",
    "src/backtesting.py",
    "src/stress_testing.py",
    "src/diagnostics.py",
    "src/portfolio.py",
    "src/reporting.py",

    "src/utils/__init__.py",
    "src/utils/math_utils.py",
    "src/utils/covariance_utils.py",
    "src/utils/distribution_utils.py",
    "src/utils/seed_control.py",

    "scripts/run_var_comparison.py",
    "scripts/run_backtests.py",
    "scripts/run_stress_tests.py",
    "scripts/run_diagnostics.py",
    "scripts/run_sensitivity_analysis.py",

    "tests/test_scenario_engine.py",
    "tests/test_risk_measures.py",
    "tests/test_backtesting.py",
    "tests/test_diagnostics.py",
    "tests/test_portfolio.py",

    "docs/architecture.md",
    "docs/assumptions.md",
    "docs/methodology.md",
    "docs/api_reference.md",
]

def create_structure():
    # Create folders
    for folder in folders:
        path = os.path.join(BASE_PATH, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Created folder: {path}")

    # Create files
    for file in files:
        path = os.path.join(BASE_PATH, file)
        # Ensure parent folder exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Create empty file if not exists
        if not os.path.exists(path):
            with open(path, "w") as f:
                pass
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")

if __name__ == "__main__":
    create_structure()
