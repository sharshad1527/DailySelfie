#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/DailySelfie"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP="$AUTOSTART_DIR/daily-selfie.desktop"
RUNNER="$APP_DIR/run_daily_selfie.sh"
VENV_DIR="$APP_DIR/.venv"

echo "→ Disabling autostart"
rm -f "$DESKTOP"

echo "→ Removing virtualenv"
rm -rf "$VENV_DIR"

echo "→ Removing app code (keeping user data like photos/logs)"
rm -f "$RUNNER"
# Remove only code; keep the directory if user stored images here
rm -rf "$APP_DIR/DS"
rm -f "$APP_DIR/main.py"
rm -f "$APP_DIR/requirements.txt"
rm -f "$APP_DIR/uninstall.sh"

echo "✅ Uninstalled. Your photos and cam.log (under ~/Desktop/DailySelfie) were NOT deleted."
echo "If you want to remove ALL data, delete ~/Desktop/DailySelfie and any photo directories you configured."
