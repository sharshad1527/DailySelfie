"""GUI PART"""
import os, time, datetime
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

from DS import core

# ---- module-level state
root = None
preview_lbl = None
status_lbl = None
capture_btn = None
cap = None
capturing = False
cfg = None  # config dict from main


def run(passed_cfg) -> int:
    """Entry from main.py. Build window, open camera, start preview, mainloop."""
    global root, preview_lbl, status_lbl, capture_btn, cfg, cap
    cfg = passed_cfg

    # window
    root = tk.Tk()
    root.title("Daily Selfie")
    root.protocol("WM_DELETE_WINDOW", on_close)

    preview_lbl = tk.Label(root)
    preview_lbl.pack(padx=8, pady=8)

    row = tk.Frame(root)
    row.pack(fill="x", padx=8, pady=4)

    capture_btn = tk.Button(row, text="Capture", state="disabled", command=on_capture)
    capture_btn.pack(side="left")

    status_lbl = tk.Label(row, text="Initializing camera...", anchor="w")
    status_lbl.pack(side="left", padx=8)

    # open camera
    cap = open_camera(
        cfg["CAM_INDEX"],
        cfg["IMG_WIDTH"],
        cfg["IMG_HEIGHT"],
        cfg["WARMUP_FRAMES"],
    )
    if not cap or not cap.isOpened():
        core.log_line("Error: Camera Open Failed", cfg["LOG_PATH"])
        try:
            messagebox.showerror("Camera", "Unable to open camera")
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass
        return 1

    # start preview
    capture_btn.config(state="normal")
    status_lbl.config(text="Preview ready. One photo per day.")
    root.after(30, update_frame)

    root.mainloop()
    return 0


def open_camera(index: int, width: int, height: int, warmup_frames: int):
    """Return an opened cv2.VideoCapture or None."""
    try:
        c = cv2.VideoCapture(int(index), cv2.CAP_V4L2)
        if not c or not c.isOpened():
            c = cv2.VideoCapture(int(index))
        if not c or not c.isOpened():
            return None

        # best-effort resolution
        c.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
        c.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))

        # warm up
        ok = 0
        for _ in range(max(3, int(warmup_frames))):
            ret, _ = c.read()
            if ret:
                ok += 1
            else:
                time.sleep(0.05)
        return c if ok > 0 else None
    except Exception:
        return None


def update_frame():
    """Timer-driven preview refresh."""
    if cap:
        ret, frame = cap.read()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img.thumbnail((800, 600))
            imgtk = ImageTk.PhotoImage(image=img)
            # keep a reference so Tk/GC doesn't drop it
            preview_lbl.imgtk = imgtk
            preview_lbl.config(image=imgtk)
        else:
            status_lbl.config(text="No camera frame")
    root.after(30, update_frame)


def on_capture():
    """Capture once, save, log, disable."""
    global capturing
    if capturing:
        return
    capturing = True
    start = time.time()

    # double-guard: if today already captured, skip
    if core.find_today_image(cfg["SAVE_PATH"]):
        core.log_line("Skipped: Already Captured Today", cfg["LOG_PATH"])
        status_lbl.config(text="Already captured today (Skipped)")
        capture_btn.config(state="disabled")
        capturing = False
        return

    if not cap:
        try:
            messagebox.showerror("Camera", "Camera not available")
        except Exception:
            pass
        core.log_line("Error: No Camera", cfg["LOG_PATH"])
        capturing = False
        return

    ret, frame = cap.read()
    if not ret:
        try:
            messagebox.showerror("Camera", "Failed to capture frame")
        except Exception:
            pass
        core.log_line("Error: Capture Failed", cfg["LOG_PATH"])
        capturing = False
        return

    folder, prefix = core.today_folder_and_prefix(cfg["SAVE_PATH"])
    core.ensure_dir(folder)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fname = f"{ts}.jpg"
    path = os.path.join(folder, fname)

    # optional: fresh frame to avoid saving a mid-conversion preview frame
    ret2, fr2 = cap.read()
    save_frame = fr2 if ret2 else frame

    try:
        cv2.imwrite(path, save_frame)
        ms = int((time.time() - start) * 1000)
        core.log_line(f"Saved {path} | ms={ms}", cfg["LOG_PATH"])
        status_lbl.config(text=f"Saved: {os.path.basename(path)}")
        capture_btn.config(state="disabled")
    except Exception as e:
        try:
            messagebox.showerror("Save error", f"Failed to save: {e}")
        except Exception:
            pass
        core.log_line(f"Error Save Failed reason={e}", cfg["LOG_PATH"])
    finally:
        capturing = False


def on_close():
    """Release the camera and close."""
    try:
        if cap:
            try:
                cap.release()
            except Exception:
                pass
    finally:
        try:
            root.destroy()
        except Exception:
            pass
