import pytest
from sculptor.llm_client import RetroResponse, VocabularyCorrection, NarrativeLens, generate


def _make_response() -> RetroResponse:
    return RetroResponse(
        vocabulary_bank=[
            VocabularyCorrection(vague_word="stuff", alternatives=["tooling", "infrastructure", "debt"]),
        ],
        narrative_lenses=[
            NarrativeLens(
                archetype="Lee Child (pacing)",
                issue="Run-on sentence drains tension.",
                sculpted="It failed. Nobody noticed. That was the problem.",
            ),
        ],
        structural_interrogation=[
            "What is the 'But' in this story?",
            "Where is the visual anchor that grounds this argument?",
        ],
    )


def test_retro_response_json_roundtrip():
    r = _make_response()
    restored = RetroResponse.model_validate_json(r.model_dump_json())
    assert restored.vocabulary_bank[0].vague_word == "stuff"
    assert restored.narrative_lenses[0].archetype == "Lee Child (pacing)"
    assert len(restored.structural_interrogation) == 2


def test_vocabulary_correction_accepts_any_list():
    # Schema intentionally has no min-length — prompt engineering enforces quality
    entry = VocabularyCorrection(vague_word="things", alternatives=["constraints"])
    assert entry.vague_word == "things"


def test_generate_calls_ollama_by_default(mocker):
    mock_ollama = mocker.patch("sculptor.llm_client._generate_ollama", return_value=_make_response())
    result = generate("raw text", model="llama3.2:1b", system_prompt="sys")
    mock_ollama.assert_called_once()
    assert result.vocabulary_bank[0].vague_word == "stuff"


def test_generate_routes_to_anthropic(mocker):
    mock_fn = mocker.patch("sculptor.llm_client._generate_anthropic", return_value=_make_response())
    generate("raw text", model="llama3.2:1b", system_prompt="sys", dev_api="anthropic")
    mock_fn.assert_called_once()


def test_generate_routes_to_groq(mocker):
    mock_fn = mocker.patch("sculptor.llm_client._generate_groq", return_value=_make_response())
    generate("raw text", model="llama3.2:1b", system_prompt="sys", dev_api="groq")
    mock_fn.assert_called_once()


def test_generate_routes_to_openai(mocker):
    mock_fn = mocker.patch("sculptor.llm_client._generate_openai", return_value=_make_response())
    generate("raw text", model="llama3.2:1b", system_prompt="sys", dev_api="openai")
    mock_fn.assert_called_once()
