import pytest
from forge.macos_bridge import get_clipboard, set_clipboard, notify, notify_error, notify_success


def test_get_clipboard_calls_pbpaste(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "hello world"
    result = get_clipboard()
    assert result == "hello world"
    mock_run.assert_called_once_with(["pbpaste"], capture_output=True, text=True)


def test_get_clipboard_raises_on_failure(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(RuntimeError, match="pbpaste failed"):
        get_clipboard()


def test_set_clipboard_calls_pbcopy(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    mock_run.return_value.returncode = 0
    set_clipboard("test output")
    mock_run.assert_called_once_with(["pbcopy"], input="test output", capture_output=True, text=True)


def test_set_clipboard_raises_on_failure(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = "error"
    with pytest.raises(RuntimeError, match="pbcopy failed"):
        set_clipboard("anything")


def test_notify_constructs_osascript(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    notify("Title", "Message", subtitle="Sub")
    call_args = mock_run.call_args[0][0]
    assert call_args[0] == "osascript"
    assert "Title" in call_args[2]
    assert "Message" in call_args[2]
    assert "Sub" in call_args[2]


def test_notify_error_does_not_raise_on_osascript_failure(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    mock_run.return_value.returncode = 1
    notify_error("something went wrong")


def test_notify_escapes_quotes(mocker):
    mock_run = mocker.patch("forge.macos_bridge.subprocess.run")
    notify("Title", 'He said "hello"')
    script = mock_run.call_args[0][0][2]
    assert '\\"' in script
