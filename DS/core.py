import datetime
import os
import sys

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def today_folder_and_prefix(SAVE_PATH):
    today = datetime.date.today()
    folder = os.path.join(SAVE_PATH, str(today.year))
    prefix = today.strftime("%Y-%m-%d")
    return folder, prefix

def find_today_image(SAVE_PATH):
    folder, prefix = today_folder_and_prefix(SAVE_PATH)
    if not os.path.isdir(folder):
        return None
    for fname in os.listdir(folder):
        if fname.startswith(prefix) and (fname.lower().endswith(".jpg") or fname.lower().endswith(".jpeg") or fname.lower().endswith(".png")):
            # Found at least one file for today
            return os.path.join(folder, fname)
    return None

def log_line(msg, LOG_PATH):
    ensure_dir(os.path.dirname(LOG_PATH))
    now = datetime.datetime.now().strftime("%F %T")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{now} | {msg}\n")
    except Exception as e:
        # best-effort logging; don't crash app
        print("Logging failed:", e, file=sys.stderr)
