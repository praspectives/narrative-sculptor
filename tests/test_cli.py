from click.testing import CliRunner
from sculptor.cli import main


def test_mock_flag_runs_without_llm(mocker):
    mocker.patch("sculptor.cli.get_clipboard", return_value="some raw text")
    mocker.patch("sculptor.cli.set_clipboard")
    mocker.patch("sculptor.cli.notify_success")
    runner = CliRunner()
    result = runner.invoke(main, ["--mock"])
    assert result.exit_code == 0
    assert "Narrative Retro" in result.output
    assert "Vocabulary Bank" in result.output


def test_stdin_flag(mocker):
    mocker.patch("sculptor.cli.set_clipboard")
    mocker.patch("sculptor.cli.notify_success")
    mocker.patch("sculptor.cli.process", return_value="### 🔍 Narrative Retro\n\n**1. Vocabulary Bank**\n- test")
    runner = CliRunner()
    result = runner.invoke(main, ["--stdin", "--mock"], input="raw dictated text")
    assert result.exit_code == 0


def test_empty_clipboard_exits_with_error(mocker):
    mocker.patch("sculptor.cli.get_clipboard", return_value="")
    mocker.patch("sculptor.cli.notify_error")
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 1


def test_dev_api_flag_passed_to_process(mocker):
    mocker.patch("sculptor.cli.get_clipboard", return_value="some text")
    mocker.patch("sculptor.cli.set_clipboard")
    mocker.patch("sculptor.cli.notify_success")
    mock_process = mocker.patch(
        "sculptor.cli.process",
        return_value="### 🔍 Narrative Retro\n\n**1. Vocabulary Bank**\n- test",
    )
    runner = CliRunner()
    runner.invoke(main, ["--dev-api", "groq"])
    call_kwargs = mock_process.call_args[1]
    assert call_kwargs.get("dev_api") == "groq"


def test_llm_exception_triggers_notification(mocker):
    mocker.patch("sculptor.cli.get_clipboard", return_value="text")
    mocker.patch("sculptor.cli.process", side_effect=RuntimeError("Ollama is down"))
    mock_notify = mocker.patch("sculptor.cli.notify_error")
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    mock_notify.assert_called_once()
