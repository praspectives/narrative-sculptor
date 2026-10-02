import sys
import click
from forge.engine import process
from forge.macos_bridge import get_clipboard, set_clipboard, notify_success, notify_error


@click.command()
@click.option("--model", default="llama3.2:1b", show_default=True, help="Ollama model (local default).")
@click.option(
    "--dev-api",
    type=click.Choice(["anthropic", "groq", "openai"]),
    default=None,
    envvar="DEV_API",
    help="Cloud provider for dev/testing. Overrides local Ollama.",
)
@click.option("--dev-model", default=None, envvar="DEV_MODEL", help="Model to use with --dev-api.")
@click.option("--mock", "use_mock", is_flag=True, help="Return hardcoded response. Tests clipboard + notifications without any LLM call.")
@click.option("--stdin", "use_stdin", is_flag=True, help="Read raw text from stdin instead of clipboard.")
def main(model: str, dev_api: str | None, dev_model: str | None, use_mock: bool, use_stdin: bool) -> None:
    """The Storyteller's Forge — transform raw dictated thoughts into polished narratives.

    Default: local Ollama. Dev mode: --dev-api anthropic|groq|openai (requires API key in .env).
    """
    try:
        raw_text = sys.stdin.read().strip() if use_stdin else get_clipboard().strip()
        if not raw_text and not use_mock:
            notify_error("Clipboard is empty. Copy your text first.")
            sys.exit(1)

        result = process(raw_text, model=model, mock=use_mock, dev_api=dev_api, dev_model=dev_model)
        set_clipboard(result)
        notify_success()
        click.echo(result)

    except Exception as e:
        msg = str(e)[:120]
        notify_error(msg)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
