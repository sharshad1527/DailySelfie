import os
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: %(message)s',
level=logging.INFO)
cfg={
    "SAVE_PATH":os.path.expanduser("~/DailySelfie/Pictures"),
    "LOG_PATH":os.path.expanduser("~/DailySelfie/cam.log"),
    "CAM_INDEX":0,
    "WARMUP_FRAMES": 8,
    "IMG_WIDTH":1280,
    "IMG_HEIGHT":720,
    "DUP_WINDOW_SECONDS":60
    }


if __name__ == "__main__":
    try:
        import cv2
        import tkinter as tk
        from tkinter import messagebox
        from PIL import Image, ImageTk
        from DS import core, gui

        # Ensure folders exist
        core.ensure_dir(cfg['SAVE_PATH'])
        core.ensure_dir(os.path.dirname(cfg['LOG_PATH']))

        if core.find_today_image(cfg['SAVE_PATH']): # Photo Taken Already Exits
            logger.warning("Image Taken already")
            core.log_line("skipped (already captured today)", cfg["LOG_PATH"])
            exit(0)

        logger.info("No Image Found Today")
        logger.info("Starting GUI")
        rc = gui.run(cfg)
        sys.exit(rc)
    except ImportError:
        logger.critical(f"“Missing dependency: opencv-python / pillow / tk”, Try Running 'pip install -r requirements.txt'")
        exit(1)
    except Exception as e:
        logger.critical(f"{e}")
        exit(1)