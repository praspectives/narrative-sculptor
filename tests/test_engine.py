from sculptor.engine import format_output, process, MOCK_RESPONSE
from sculptor.llm_client import RetroResponse, VocabularyCorrection, NarrativeLens


def _make_response() -> RetroResponse:
    return RetroResponse(
        vocabulary_bank=[
            VocabularyCorrection(vague_word="things", alternatives=["constraints", "trade-offs", "levers"]),
        ],
        narrative_lenses=[
            NarrativeLens(
                archetype="Contrarian Essayist",
                issue="Weak hook — states a fact without tension.",
                sculpted="Every founder is wrong about their first idea. That's the point.",
            ),
        ],
        structural_interrogation=[
            "Where is the 'But'? What conflict makes this worth reading?",
        ],
    )


def test_format_output_structure():
    result = format_output(_make_response())
    assert "### 🔍 Narrative Retro" in result
    assert "**1. Vocabulary Bank**" in result
    assert "**2. Narrative Lenses**" in result
    assert "**3. Structural Interrogation**" in result
    assert "Instead of *things*" in result
    assert "Contrarian Essayist" in result


def test_process_mock_returns_formatted_string():
    result = process("anything", mock=True)
    assert "### 🔍 Narrative Retro" in result
    assert "Vocabulary Bank" in result
    assert "Narrative Lenses" in result
    assert "Structural Interrogation" in result


def test_process_mock_skips_llm(mocker):
    mock_generate = mocker.patch("sculptor.engine.generate")
    process("anything", mock=True)
    mock_generate.assert_not_called()


def test_process_calls_generate_with_dev_api(mocker):
    mock_generate = mocker.patch("sculptor.engine.generate", return_value=MOCK_RESPONSE)
    process("test text", dev_api="groq", dev_model="llama-3.1-8b-instant")
    mock_generate.assert_called_once()
    args, kwargs = mock_generate.call_args
    assert kwargs.get("dev_api") == "groq" or args[3] == "groq"


def test_process_defaults_to_ollama(mocker):
    mock_generate = mocker.patch("sculptor.engine.generate", return_value=MOCK_RESPONSE)
    process("test text")
    mock_generate.assert_called_once()
    call_str = str(mock_generate.call_args)
    assert "groq" not in call_str
    assert "anthropic" not in call_str
