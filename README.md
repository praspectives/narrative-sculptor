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
DEV_API=grok
GROK_API_KEY=xai-...
```

Supported providers: `grok`, `anthropic`, `groq`, `openai`.

## Hotkey setup (one command)

Run the automated setup script — it installs a macOS Quick Action directly into `~/Library/Services/`:

```bash
bash scripts/setup_mac_hotkey.sh
```

Then bind a shortcut (e.g. `Cmd+Shift+E`):
1. System Settings → Keyboard → Keyboard Shortcuts → Services
2. Scroll to **General** → find **Narrative Sculptor**
3. Click **Add Shortcut** and press your chosen key combo

From then on:
1. Copy your raw draft (`Cmd+C`)
2. Press the hotkey
3. Wait for the **"Narrative Sculptor Ready"** notification
4. Paste (`Cmd+V`) at the bottom of your document

## Customising the system prompt

The prompt lives in `src/sculptor/system_prompt.md` — edit it directly with no Python changes required. Restart the tool and the new prompt is live.

## Project structure

```
src/sculptor/
├── cli.py             # Entry point (click)
├── engine.py          # Reads system_prompt.md + output formatter
├── system_prompt.md   # System prompt — edit freely to refine coaching rules
├── llm_client.py      # Ollama/cloud wrapper with Pydantic structured output
└── macos_bridge.py    # clipboard (pbcopy/pbpaste) + macOS notifications
scripts/
├── install_mac.sh     # One-shot installer (Ollama + uv sync)
└── setup_mac_hotkey.sh  # Installs Automator Quick Action + hotkey instructions
```
