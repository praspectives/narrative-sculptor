from forge.engine import format_output, process, MOCK_RESPONSE
from forge.llm_client import ForgeResponse, XRayBulletPoints


def test_format_output_structure():
    response = ForgeResponse(
        story="Every founder is wrong about their first idea.",
        xray=XRayBulletPoints(bullets=[
            "Hook: Contrarian claim opened the piece.",
            "Pacing: Short declarative sentence delivers the gut-punch.",
            "Voice: 'founder' replaces vague 'people' for precision.",
        ]),
    )
    result = format_output(response)
    assert result.startswith("[THE STORY]")
    assert "---" in result
    assert "[THE X-RAY]" in result
    assert result.count("- ") == 3


def test_process_mock_returns_formatted_string():
    result = process("anything", mock=True)
    assert "[THE STORY]" in result
    assert "[THE X-RAY]" in result
    assert result.count("- ") >= 3


def test_process_mock_skips_llm(mocker):
    mock_generate = mocker.patch("forge.engine.generate")
    process("anything", mock=True)
    mock_generate.assert_not_called()


def test_process_calls_generate_with_dev_api(mocker):
    mock_generate = mocker.patch(
        "forge.engine.generate",
        return_value=MOCK_RESPONSE,
    )
    process("test text", dev_api="groq", dev_model="llama-3.1-8b-instant")
    mock_generate.assert_called_once()
    _, kwargs = mock_generate.call_args
    assert kwargs.get("dev_api") == "groq" or mock_generate.call_args[0][3] == "groq"


def test_process_defaults_to_ollama(mocker):
    mock_generate = mocker.patch("forge.engine.generate", return_value=MOCK_RESPONSE)
    process("test text")
    mock_generate.assert_called_once()
    call_kwargs = mock_generate.call_args
    assert "groq" not in str(call_kwargs)
    assert "anthropic" not in str(call_kwargs)
