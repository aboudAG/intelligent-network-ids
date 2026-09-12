from __future__ import annotations

import importlib
import sys


REQUIRED_MODULES = [
    "pandas",
    "numpy",
    "sklearn",
    "sklearn.model_selection",
    "sklearn.ensemble",
    "sklearn.svm",
    "sklearn.neural_network",
    "joblib",
    "matplotlib",
    "seaborn",
    "streamlit",
    "pytest",
]


def main() -> None:
    print(f"Python: {sys.version}")
    failed = []
    for module_name in REQUIRED_MODULES:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "installed")
            print(f"[OK] {module_name}: {version}")
        except Exception as exc:
            failed.append(module_name)
            print(f"[FAILED] {module_name}: {exc}")

    if failed:
        print()
        print("Some scientific Python modules could not be imported.")
        print("On Windows, this can be caused by Application Control blocking downloaded DLL/PYD files.")
        print("Try running PowerShell from the project root:")
        print("Get-ChildItem -LiteralPath .\\.venv -Recurse -File | Unblock-File")
        raise SystemExit(1)

    print("Environment check completed successfully.")


if __name__ == "__main__":
    main()
