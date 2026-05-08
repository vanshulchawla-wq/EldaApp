# Elda Directory - Android App

A KivyMD-based Android app that mirrors the Elda Customer Directory Streamlit web app.

## Features
- Customer listing with phone number search
- Customer detail view (Emergency, Social, Health, Home)
- Edit customer data
- MongoDB backend (same database as web version)

## How to Build APK

### Option A: GitHub Actions (Recommended)
1. Push this folder to a GitHub repo
2. Add `MONGO_URI` as a repository secret (Settings → Secrets → Actions)
3. The workflow will build the APK automatically on push
4. Download the APK from Actions → Build → Artifacts

### Option B: Local Build (Linux/Docker)
```bash
pip install buildozer cython
buildozer android debug
```
The APK will be in the `bin/` folder.

### Option C: Google Colab
Run in a Colab notebook:
```python
!pip install buildozer cython
!sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
!buildozer android debug
```

## Running Locally (Desktop Preview)
```bash
pip install kivy kivymd pymongo[srv]
python main.py
```

## Configuration
Set `MONGO_URI` environment variable or edit it in `main.py`.
