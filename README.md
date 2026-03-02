# StreetWatch
A mobile application that lets citizens report road damage (potholes, cracks, broken signs) by taking geotagged photos. The app uses an on-device CNN to classify damage type and severity, and uploads reports to an open geospatial database visible on a public web map.

---

## Dataset Setup (RDD2022)

The model is trained on the **RDD2022 – Road Damage Dataset** released through CRDDC 2022.

> The dataset is large (~several GB) and is **not stored in this repository** (`backend/image_classification/data/` is git-ignored). Every team member must download it locally.

---

### TL;DR — just run this

```bash
cd backend/image_classification
python download_dataset.py
```

The script handles everything automatically:
- Installs the `kaggle` package if it is missing
- Guides you through credential setup on first run
- Shows a live progress bar during download
- Unzips the dataset automatically

---

### One-time Kaggle credential setup

You only need to do this **once per machine**. The script will prompt you interactively if it detects no credentials, but you can also set them up manually using the steps below.

#### Step 1 — Get your token from Kaggle

1. Log in to [kaggle.com](https://www.kaggle.com)
2. Click your profile picture (top-right) → **Settings**
3. Scroll down to the **API** section
4. Click **"Generate New Token"** → a file called `kaggle.json` is downloaded

#### Step 2 — Place the file in the right location

The script accepts the file in any of these ways — use whichever is easiest:

**Option A — Let the script do it (recommended)**  
Just run `python download_dataset.py`. When it detects no credentials, it asks for the path to your `kaggle.json` and copies it automatically.

**Option B — Copy the file manually**

| OS | Path |
|----|------|
| Windows | `C:\Users\<YourUsername>\.kaggle\kaggle.json` |
| macOS / Linux | `~/.kaggle/kaggle.json` |

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force "$HOME\.kaggle"
Move-Item "$HOME\Downloads\kaggle.json" "$HOME\.kaggle\kaggle.json"
```

```bash
# macOS / Linux
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

**Option C — Paste the token directly**  
If you can't locate the file, run the script and choose the "paste manually" option. You can find your token value inside the downloaded `kaggle.json` (it looks like `KGAT_...`).

---

### Environment-specific notes

| Setup | What to do |
|-------|------------|
| **Anaconda (any OS)** | `kaggle` is pre-installed. Just place your credentials and run the script. |
| **Plain Python (pip)** | The script auto-installs `kaggle` on first run — no manual install needed. |
| **VS Code / no venv** | Run `pip install kaggle` in your terminal once, then run the script. |
| **Google Colab** | `!pip install kaggle` then upload `kaggle.json` via the Colab file browser to `/root/.kaggle/`. |

---

### Dataset sources

| Source | URL |
|--------|-----|
| **Kaggle** (used by the script) | https://www.kaggle.com/datasets/aliabdelmenam/rdd-2022/data |
| Figshare (backup) | https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547/1 |

### Expected folder structure after download

```
backend/image_classification/data/
└── rdd-2022/
    ├── China_MotorBike/
    ├── China_Drone/
    ├── Czech/
    ├── India/
    ├── Japan/
    ├── Norway/
    ├── United_States/
    └── ...
```
