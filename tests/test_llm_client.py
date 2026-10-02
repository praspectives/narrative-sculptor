import pytest
from forge.llm_client import ForgeResponse, XRayBulletPoints, generate


def _make_response():
    return ForgeResponse(
        story="The best ideas arrive uninvited.",
        xray=XRayBulletPoints(bullets=[
            "Hook: Surprise opener.",
            "Pacing: Short sentence.",
            "Voice: Active verb replaces passive construction.",
        ]),
    )


def test_forge_response_validates_bullet_count():
    with pytest.raises(Exception):
        ForgeResponse(
            story="x",
            xray=XRayBulletPoints(bullets=["only one bullet"]),
        )


def test_forge_response_json_roundtrip():
    r = _make_response()
    restored = ForgeResponse.model_validate_json(r.model_dump_json())
    assert restored.story == r.story
    assert restored.xray.bullets == r.xray.bullets


def test_generate_calls_ollama_by_default(mocker):
    mock_ollama = mocker.patch("forge.llm_client._generate_ollama", return_value=_make_response())
    result = generate("raw text", model="llama3.2:1b", system_prompt="sys")
    mock_ollama.assert_called_once()
    assert result.story == "The best ideas arrive uninvited."


def test_generate_routes_to_anthropic(mocker):
    mock_fn = mocker.patch("forge.llm_client._generate_anthropic", return_value=_make_response())
    generate("raw text", model="llama3.2:1b", system_prompt="sys", dev_api="anthropic")
    mock_fn.assert_called_once()


def test_generate_routes_to_groq(mocker):
    mock_fn = mocker.patch("forge.llm_client._generate_groq", return_value=_make_response())
    generate("raw text", model="llama3.2:1b", system_prompt="sys", dev_api="groq")
    mock_fn.assert_called_once()


def test_generate_routes_to_openai(mocker):
    mock_fn = mocker.patch("forge.llm_client._generate_openai", return_value=_make_response())
    generate("raw text", model="llama3.2:1b", system_prompt="sys", dev_api="openai")
    mock_fn.assert_called_once()
