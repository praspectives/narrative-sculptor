import sys
import click
from forge.engine import process
from forge.macos_bridge import get_clipboard, set_clipboard, notify_success, notify_error


@click.command()
@click.option("--model", default="llama3.2:1b", show_default=True, help="Ollama model to use.")
@click.option("--stdin", "use_stdin", is_flag=True, help="Read raw text from stdin instead of clipboard.")
def main(model: str, use_stdin: bool) -> None:
    """The Storyteller's Forge — transform raw dictated thoughts into polished narratives."""
    try:
        raw_text = sys.stdin.read().strip() if use_stdin else get_clipboard().strip()
        if not raw_text:
            notify_error("Clipboard is empty. Copy your text first.")
            sys.exit(1)

        result = process(raw_text, model=model)
        set_clipboard(result)
        notify_success()
        click.echo(result)

    except Exception as e:
        msg = str(e)[:120]
        notify_error(msg)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
