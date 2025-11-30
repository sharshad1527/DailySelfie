#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/DailySelfie"
SRC_DIR="$(pwd)"  # run this from your repo root
VENV_DIR="$APP_DIR/.venv"
AUTOSTART_DIR="$HOME/.config/autostart"
RUNNER="$APP_DIR/run_daily_selfie.sh"
DESKTOP="$AUTOSTART_DIR/daily-selfie.desktop"

echo "→ Creating app directory: $APP_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$AUTOSTART_DIR"

echo "→ Copying project files to $APP_DIR"
# Adjust list if your repo has more files
cp -r "$SRC_DIR/DS" "$APP_DIR/"
cp "$SRC_DIR/main.py" "$APP_DIR/"
cp "$SRC_DIR/requirements.txt" "$APP_DIR/"
cp "$SRC_DIR/uninstall.sh" "$APP_DIR/"

echo "→ Creating Python venv: $VENV_DIR"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"

echo "→ Creating run script: $RUNNER"
cat > "$RUNNER" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$HOME/DailySelfie"
VENV_DIR="$APP_DIR/.venv"
cd "$APP_DIR"
exec "$VENV_DIR/bin/python" "$APP_DIR/main.py"
EOF
chmod +x "$RUNNER"

echo "→ Creating autostart .desktop entry: $DESKTOP"
cat > "$DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Name=Daily Selfie
Comment=Capture one webcam photo per day
Exec=$RUNNER
Terminal=false
X-GNOME-Autostart-enabled=true
OnlyShowIn=GNOME;
EOF

echo "→ Creating data folders"
mkdir -p "$HOME/Desktop/DailySelfie"              # logs default here in your cfg
mkdir -p "$HOME/Desktop/DailySelfie/Pictures"        # photos default here in your cfg (adjust if you change)

echo "✅ Install complete."
echo "Login to test autostart, or run manually: $RUNNER"
