"""
Download the RDD2022 (Road Damage Dataset 2022) via the Kaggle API.

Dataset: https://www.kaggle.com/datasets/aliabdelmenam/rdd-2022

Prerequisites — one-time setup:
  1. Log in to https://www.kaggle.com
  2. Go to your profile picture → Settings → API
  3. Click "Generate New Token" → download kaggle.json
  4. Run the setup helper once:
       python download_dataset.py --setup

Usage:
    python download_dataset.py
"""

import json
import os
import subprocess
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
KAGGLE_DATASET = "aliabdelmenam/rdd-2022"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
KAGGLE_DIR = os.path.join(os.path.expanduser("~"), ".kaggle")
KAGGLE_JSON = os.path.join(KAGGLE_DIR, "kaggle.json")
ACCESS_TOKEN_FILE = os.path.join(KAGGLE_DIR, "access_token")


# ---------------------------------------------------------------------------
# Step 1 — ensure the kaggle package is installed
# ---------------------------------------------------------------------------
def _ensure_kaggle_installed() -> None:
    try:
        import kaggle  # noqa: F401
    except ImportError:
        print("[setup] 'kaggle' package not found — installing it now...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "kaggle"],
            stdout=subprocess.DEVNULL,
        )
        print("[setup] kaggle installed successfully.\n")


# ---------------------------------------------------------------------------
# Step 2 — ensure credentials exist
# ---------------------------------------------------------------------------
def _ensure_credentials() -> None:
    """
    Accepts all credential formats supported by kaggle 2.x:

      A) ~/.kaggle/access_token          plain-text KGAT_ token  (kaggle 2.x)
      B) KAGGLE_API_TOKEN env variable   same token via environment
      C) ~/.kaggle/kaggle.json           {"token": "KGAT_..."}  → auto-converts to (A)
      D) ~/.kaggle/kaggle.json           {"username": "...", "key": "..."}  (legacy)

    If none of the above exist, the user is guided interactively.
    """
    # (A) access_token file already present
    if os.path.exists(ACCESS_TOKEN_FILE):
        return

    # (B) env var
    if os.environ.get("KAGGLE_API_TOKEN"):
        return

    # (C/D) kaggle.json present — inspect its contents
    if os.path.exists(KAGGLE_JSON):
        try:
            with open(KAGGLE_JSON, "r") as fh:
                creds = json.load(fh)
        except (json.JSONDecodeError, OSError):
            creds = {}

        # (C) New token format — write to access_token so kaggle SDK finds it
        if creds.get("token", "").startswith("KGAT_"):
            os.makedirs(KAGGLE_DIR, exist_ok=True)
            with open(ACCESS_TOKEN_FILE, "w") as fh:
                fh.write(creds["token"])
            print(f"[setup] Saved KGAT_ token to {ACCESS_TOKEN_FILE}")
            return

        # (D) Legacy format — kaggle package reads these env vars directly
        if creds.get("username") and creds.get("key"):
            os.environ["KAGGLE_USERNAME"] = creds["username"]
            os.environ["KAGGLE_KEY"] = creds["key"]
            return

    # --- No credentials found → interactive guided setup ---
    print()
    print("=" * 60)
    print(" Kaggle credentials not found — one-time setup needed")
    print("=" * 60)
    print("""
Steps to get your Kaggle token:
  1. Open https://www.kaggle.com in your browser
  2. Click your profile picture (top-right) → Settings
  3. Scroll to the API section
  4. Click \"Generate New Token\"
     → A file called kaggle.json is downloaded to your Downloads folder
  5. Enter the path to that file below (or paste the token directly)
""")

    choice = input(
        "Do you have the kaggle.json file? [y] Yes / [n] I'll paste the token manually: "
    ).strip().lower()

    os.makedirs(KAGGLE_DIR, exist_ok=True)

    if choice == "n":
        # Manual token paste
        token = input("\nPaste your token (starts with KGAT_ or is a plain key): ").strip()
        if not token:
            sys.exit("ERROR: No token entered. Please re-run the script.")

        if token.startswith("KGAT_"):
            with open(ACCESS_TOKEN_FILE, "w") as fh:
                fh.write(token)
            print(f"[setup] Token saved to {ACCESS_TOKEN_FILE}")
        else:
            username = input("Enter your Kaggle username: ").strip()
            if not username:
                sys.exit("ERROR: Username required for legacy key authentication.")
            creds = {"username": username, "key": token}
            with open(KAGGLE_JSON, "w") as fh:
                json.dump(creds, fh)
            os.environ["KAGGLE_USERNAME"] = username
            os.environ["KAGGLE_KEY"] = token
            print(f"[setup] Credentials saved to {KAGGLE_JSON}")
    else:
        # User has the kaggle.json file
        default = os.path.join(os.path.expanduser("~"), "Downloads", "kaggle.json")
        raw = input(f"\nPath to kaggle.json [default: {default}]: ").strip()
        src = raw if raw else default

        if not os.path.exists(src):
            sys.exit(f"ERROR: File not found: {src}\nPlease re-run the script with the correct path.")

        import shutil
        shutil.copy(src, KAGGLE_JSON)
        print(f"[setup] Copied to {KAGGLE_JSON}")

        # Recursively resolve the copied file
        _ensure_credentials()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    _ensure_kaggle_installed()
    _ensure_credentials()

    import kaggle

    os.makedirs(DATA_DIR, exist_ok=True)

    # Check if already downloaded
    rdd_dir = os.path.join(DATA_DIR, "rdd-2022")
    if os.path.exists(rdd_dir) and any(os.scandir(rdd_dir)):
        print(f"Dataset folder already exists: {rdd_dir}")
        ans = input("Re-download? [y/N]: ").strip().lower()
        if ans != "y":
            print("Dataset is ready at:", rdd_dir)
            return

    api = kaggle.KaggleApi()
    api.authenticate()

    print(f"\nDownloading '{KAGGLE_DATASET}' from Kaggle...")
    print(f"  Destination: {DATA_DIR}")
    print("  (tqdm progress bar below)\n")

    # quiet=False → tqdm progress bar per file, unzip=True → auto-extract
    api.dataset_download_files(
        KAGGLE_DATASET,
        path=DATA_DIR,
        unzip=True,
        quiet=False,
        force=True,
    )

    print(f"\nDataset is ready at: {DATA_DIR}")


if __name__ == "__main__":
    main()
