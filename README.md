# The Storyteller's Forge

A macOS utility that transforms raw, dictated thoughts into polished narratives using a local LLM (Ollama). 100% local, free, no API keys.

## How it works

1. Dictate or write raw thoughts → copy to clipboard
2. Trigger the hotkey
3. Paste the result — a polished story with an X-Ray explanation of what changed

## Requirements

- macOS
- [Ollama](https://ollama.com/download)
- [uv](https://astral.sh/uv)

## Install

```bash
bash scripts/install_mac.sh
```

## Usage

```bash
# From clipboard (default — use after copying your raw text)
uv run forge

# From stdin
echo "your raw text here" | uv run forge --stdin

# Use a different model
uv run forge --model phi3
```

## Output format

```
[THE STORY]
The polished narrative goes here.

---
[THE X-RAY]
- Bullet explaining storytelling mechanic 1
- Bullet explaining vocabulary replacement
- Bullet explaining pacing choice
```

## Hotkey setup (macOS Automator)

See the step-by-step instructions printed by `install_mac.sh` after installation.

## Project structure

```
src/forge/
├── cli.py           # Entry point (click)
├── engine.py        # System prompt + output formatter
├── llm_client.py    # Ollama wrapper with Pydantic structured output
└── macos_bridge.py  # clipboard (pbcopy/pbpaste) + macOS notifications
scripts/
└── install_mac.sh   # One-shot installer
```
