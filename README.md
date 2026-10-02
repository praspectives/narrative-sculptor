# Narrative Sculptor

A macOS utility that analyzes raw drafts and delivers a pedagogical Narrative Retro — vocabulary corrections, style lens rewrites from master archetypes, and Socratic structural questions. Runs 100% locally via Ollama, no API keys required.

## How it works

1. Write or dictate your raw draft → copy to clipboard
2. Trigger the hotkey
3. Paste the Narrative Retro at the bottom of your document and iterate

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
# From clipboard (default — copy your draft first)
uv run sculpt

# From stdin
echo "your raw draft here" | uv run sculpt --stdin

# Use a different local model
uv run sculpt --model phi3

# Dev mode: test with a cloud API (no local Ollama needed)
uv run sculpt --dev-api anthropic   # requires ANTHROPIC_API_KEY in .env

# Test plumbing without any LLM call
uv run sculpt --mock
```

## Output format

```
### 🔍 Narrative Retro

**1. Vocabulary Bank**
- Instead of *things* → Use: constraints, trade-offs, leverage points

**2. Narrative Lenses**
- *Contrarian Essayist (hook repair)*
  - Issue: The opening sentence states a fact with no tension.
  - Sculpted: Most teams don't have a communication problem...

**3. Structural Interrogation**
- Where is the 'But'? What conflict makes this worth reading?
```

## Dev mode (cloud API for prompt iteration)

Copy `.env.example` to `.env` and add your key:
```
DEV_API=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

## Hotkey setup (macOS Automator)

See the step-by-step instructions printed by `install_mac.sh` after installation.

## Project structure

```
src/sculptor/
├── cli.py           # Entry point (click)
├── engine.py        # System prompt + output formatter
├── llm_client.py    # Ollama/cloud wrapper with Pydantic structured output
└── macos_bridge.py  # clipboard (pbcopy/pbpaste) + macOS notifications
scripts/
└── install_mac.sh   # One-shot installer
```
