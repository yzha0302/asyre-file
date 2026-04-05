#!/usr/bin/env bash
set -e

echo ""
echo "  Asyre File — Installer"
echo "  ======================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "  ERROR: Python 3 is required but not found."
  echo "  Install it first: https://www.python.org/downloads/"
  exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "  Python: $PY_VER"

# Clone or update
INSTALL_DIR="${1:-asyre-file}"
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "  Updating existing installation..."
  cd "$INSTALL_DIR" && git pull
else
  echo "  Cloning repository..."
  git clone https://github.com/yzha0302/asyre-file.git "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

# Create data dir
mkdir -p data

# Optional: install export deps
echo ""
read -p "  Install PDF/Word export support? (requires ~200MB) [y/N]: " INSTALL_EXPORT
if [[ "$INSTALL_EXPORT" =~ ^[Yy]$ ]]; then
  pip install -r requirements.txt
fi

echo ""
echo "  Done! To start:"
echo ""
echo "    cd $INSTALL_DIR"
echo "    python3 server.py"
echo ""
echo "  Then visit http://localhost:8765"
echo "  The setup wizard will guide you through first-time configuration."
echo ""
