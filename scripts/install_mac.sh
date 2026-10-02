#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="llama3.2:1b"

echo "=== Narrative Sculptor — macOS Installer ==="
echo ""

# 1. Check Ollama
if ! command -v ollama &>/dev/null; then
    echo "ERROR: Ollama is not installed."
    echo "Install it from: https://ollama.com/download"
    echo "Then re-run this script."
    exit 1
fi
echo "[1/3] Ollama found: $(ollama --version 2>&1 | head -1)"

# 2. Pull model
echo "[2/3] Pulling $MODEL (this may take a few minutes on first run)..."
ollama pull "$MODEL"

# 3. Sync uv environment
if ! command -v uv &>/dev/null; then
    echo "ERROR: uv is not installed."
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo "[3/3] Syncing Python environment with uv..."
cd "$REPO_DIR" && uv sync

echo ""
echo "=== Installation complete ==="
echo ""
echo "Quick test:"
echo "  echo 'your raw draft here' | uv run sculpt --stdin"
echo ""
echo "To bind to a macOS hotkey:"
echo "  1. Open Automator → New Document → Quick Action"
echo "  2. Set 'Workflow receives' = 'no input' in 'any application'"
echo "  3. Add action: 'Run Shell Script'"
echo "  4. Set shell to /bin/bash and paste:"
echo "     cd $REPO_DIR && uv run sculpt"
echo "  5. Save as 'Narrative Sculptor'"
echo "  6. System Settings → Keyboard → Keyboard Shortcuts → Services"
echo "     Find 'Narrative Sculptor' → assign hotkey (e.g. Cmd+Shift+N)"
echo ""
echo "Usage: copy any draft to clipboard, trigger the hotkey, paste the Retro at the bottom of your note."
