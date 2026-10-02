import subprocess


def get_clipboard() -> str:
    result = subprocess.run(["pbpaste"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pbpaste failed: {result.stderr}")
    return result.stdout


def set_clipboard(text: str) -> None:
    result = subprocess.run(["pbcopy"], input=text, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pbcopy failed: {result.stderr}")


def notify(title: str, message: str, subtitle: str = "") -> None:
    safe = lambda s: s.replace('"', '\\"')
    script = f'display notification "{safe(message)}" with title "{safe(title)}"'
    if subtitle:
        script += f' subtitle "{safe(subtitle)}"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def notify_error(message: str) -> None:
    notify("Storyteller's Forge", message, subtitle="Error — check terminal")


def notify_success() -> None:
    notify(
        "Storyteller's Forge",
        "Retro Ready! Press Cmd+V to append it at the bottom of your note.",
        subtitle="Narrative Post-Mortem",
    )
