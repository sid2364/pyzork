#!/usr/bin/env python3
"""Install required packages and NLTK datasets for pyzork.

Running this script will ensure that the `nltk` package is installed and that the
required NLTK data files are present in the local ``nltk_data`` directory.
After executing it you should be able to start the game with ``python zork.py``.
"""

import importlib
import os
import subprocess
import sys


def ensure_package(pkg_name: str) -> None:
    """Ensure that a package is installed via pip."""
    try:
        importlib.import_module(pkg_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])


def ensure_nltk_data() -> None:
    """Download NLTK resources used by the game if they are missing."""
    import nltk  # noqa: E402 - imported after ensure_package

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(repo_root, "nltk_data")
    os.makedirs(data_dir, exist_ok=True)
    nltk.data.path.append(data_dir)

    for resource in ["punkt", "punkt_tab", "stopwords"]:
        try:
            nltk.data.find(f"tokenizers/{resource}" if resource == "punkt" else f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, download_dir=data_dir)


def main() -> None:
    ensure_package("nltk")
    ensure_nltk_data()
    print("All dependencies installed. You can now run zork.py")


if __name__ == "__main__":
    main()
