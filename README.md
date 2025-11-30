# 🧠 Daily Selfie Automation

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](#)

> A lightweight, privacy-focused Python application that captures **one photo per day** from your webcam.  
> Designed to help you track your appearance or build long-term visual logs — securely and offline.

---

## 🎯 Features

- 📸 **One-per-day rule** – prevents duplicate photos automatically  
- 🖥️ **Live preview GUI** – view yourself before capturing  
- 🗓️ **Auto-organized storage** – saves to:
  ```
  ~/DailySelfies/<year>/YYYY-MM-DD_HH-MM-SS.jpg
  ```
- 🧾 **Local logging** – every event written to:
  ```
  ~/DailySelfie/cam.log
  ```
- ⚙️ **Customizable configuration** – camera index, resolution, warmup frames, etc.  
- 🔁 **Optional autostart at system login**
- 🧹 **Uninstall script** included
- 🧠 **Future plans:** headless mode

---

## 🧱 Project Structure

```
DailySelfie/
├── DS/
│   ├── core.py       # Core logic: logging, folders, path checks
│   └── gui.py        # GUI logic: camera preview, capture handling
├── main.py           # Entry point — connects config, core, and GUI
├── requirements.txt  # Dependencies
├── install.sh        # Setup + optional autostart script
└── uninstall.sh      # Clean uninstaller script
```

---

## ⚙️ Requirements

- **Python 3.8+**
- **Linux desktop environment** (GNOME, KDE, XFCE, etc.)
- Working webcam (`/dev/video*`)

### Install dependencies:
```bash
pip install -r requirements.txt
```

> **Tip:** If `tkinter` is missing, install it via:
> ```bash
> sudo apt install python3-tk
> ```

---

## 🚀 Quick Start

```bash
git clone https://github.com/sharshad1527/DailySelfie.git
cd DailySelfie

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```

✅ If you’ve already taken a photo today → the app exits with a log entry.  
📷 If not → GUI opens → click **Capture** to save today’s selfie.

---

## 🖥️ Auto-Start Setup (Linux)

Automate startup at login:

```bash
chmod +x install.sh
./install.sh
```

This script:
- Copies all files to `~/DailySelfie`
- Creates a virtual environment
- Adds a `.desktop` launcher under `~/.config/autostart`

To verify:
```bash
ls ~/.config/autostart | grep dailyselfie
```

---

## ❌ Uninstall

To remove the app safely:
```bash
chmod +x ~/DailySelfie/uninstall.sh
bash ~/DailySelfie/uninstall.sh
```

If you want to delete everything (photos, logs, scripts):
```bash
rm -rf ~/DailySelfie/
```

---

## 🧾 Log Example

**Location:** `~/DailySelfie/cam.log`

```
2025-11-27 09:20:01 | saved /home/testuser/DailySelfie/Pictures/2025/2025-11-27_09-20-01.jpg | ms=180
2025-11-27 09:20:15 | skipped (already captured today)
2025-11-27 09:21:44 | error= camera open failed
```

---

## 🧠 Configuration

Modify these settings in **main.py**:

```python
cfg = {
    "SAVE_PATH": os.path.expanduser("~/DailySelfie/Pictures"),
    "LOG_PATH": os.path.expanduser("~/DailySelfie/cam.log"),
    "CAM_INDEX": 0,
    "WARMUP_FRAMES": 8,
    "IMG_WIDTH": 1280,
    "IMG_HEIGHT": 720,
    "DUP_WINDOW_SECONDS": 60
}
```

💡 If your camera isn’t detected, try setting `"CAM_INDEX": 1`.

---

## 🧰 Troubleshooting

| Issue | Cause | Fix |
|-------|--------|-----|
| **Camera not detected** | Wrong device index | Change `CAM_INDEX` to 1 or 2 |
| **No preview window** | Wayland/driver issue | Run under X11 |
| **“Failed to save”** | No write permission | Check your `SAVE_PATH` folder |
| **Tkinter not found** | Missing package | `sudo apt install python3-tk` |

---

## 🧾 License

**MIT License**

```
Copyright (c) 2025 Harshad Sundar
```

Permission is granted to use, copy, modify, and distribute this software under the MIT terms.  
See [LICENSE](LICENSE.md) for full text.

---

## 👤 Author

**Harshad Sundar**

Built as a personal automation project to explore:
- Python scripting
- OpenCV
- Linux system integration
---

## 💬 Final Note

> **Daily Selfie Automation** helps you visually track your journey over time —  
> one photo, once a day, no cloud storage, no privacy risks.

---
