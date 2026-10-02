from click.testing import CliRunner
from forge.cli import main


def test_mock_flag_runs_without_llm(mocker):
    mocker.patch("forge.cli.get_clipboard", return_value="some raw text")
    mocker.patch("forge.cli.set_clipboard")
    mocker.patch("forge.cli.notify_success")
    runner = CliRunner()
    result = runner.invoke(main, ["--mock"])
    assert result.exit_code == 0
    assert "[THE STORY]" in result.output
    assert "[THE X-RAY]" in result.output


def test_stdin_flag(mocker):
    mocker.patch("forge.cli.set_clipboard")
    mocker.patch("forge.cli.notify_success")
    mocker.patch("forge.engine.process", return_value="[THE STORY]\ntest\n\n---\n[THE X-RAY]\n- a\n- b\n- c")
    runner = CliRunner()
    result = runner.invoke(main, ["--stdin", "--mock"], input="raw dictated text")
    assert result.exit_code == 0


def test_empty_clipboard_exits_with_error(mocker):
    mocker.patch("forge.cli.get_clipboard", return_value="")
    mocker.patch("forge.cli.notify_error")
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 1


def test_dev_api_flag_passed_to_process(mocker):
    mocker.patch("forge.cli.get_clipboard", return_value="some text")
    mocker.patch("forge.cli.set_clipboard")
    mocker.patch("forge.cli.notify_success")
    mock_process = mocker.patch(
        "forge.cli.process",
        return_value="[THE STORY]\nx\n\n---\n[THE X-RAY]\n- a\n- b\n- c",
    )
    runner = CliRunner()
    runner.invoke(main, ["--dev-api", "groq"])
    call_kwargs = mock_process.call_args[1]
    assert call_kwargs.get("dev_api") == "groq"


def test_llm_exception_triggers_notification(mocker):
    mocker.patch("forge.cli.get_clipboard", return_value="text")
    mocker.patch("forge.cli.process", side_effect=RuntimeError("Ollama is down"))
    mock_notify = mocker.patch("forge.cli.notify_error")
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    mock_notify.assert_called_once()
