from pathlib import Path
from sculptor.llm_client import (
    generate,
    RetroResponse,
    VocabularyCorrection,
    NarrativeLens,
)

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text(encoding="utf-8").strip()

MOCK_RESPONSE = RetroResponse(
    vocabulary_bank=[
        VocabularyCorrection(
            vague_word="things",
            alternatives=["constraints", "trade-offs", "leverage points"],
        ),
        VocabularyCorrection(
            vague_word="stuff",
            alternatives=["infrastructure", "tooling", "accumulated debt"],
        ),
        VocabularyCorrection(
            vague_word="very important",
            alternatives=["load-bearing", "non-negotiable", "decisive"],
        ),
    ],
    narrative_lenses=[
        NarrativeLens(
            archetype="Contrarian Essayist (hook repair)",
            issue="[MOCK] The opening sentence states a fact. It does not create tension or demand the reader argue back.",
            sculpted="[MOCK] Most teams don't have a communication problem. They have a clarity problem they've agreed to call communication.",
        ),
        NarrativeLens(
            archetype="Technothriller Writer (exposition pacing)",
            issue="[MOCK] The middle paragraph explains the process in a single long sentence. No breath. No beat. No weight.",
            sculpted="[MOCK] The pipeline failed. Not once — repeatedly. Each failure was logged. None were fixed. That is not a bug. That is a decision.",
        ),
    ],
    structural_interrogation=[
        "[MOCK] Where is the 'But'? You have stated what happened (And) but the conflict (But) that makes this worth reading is missing entirely.",
        "[MOCK] What is the reader supposed to feel at the end? You have a conclusion but no emotional landing — what changed for the protagonist of this story?",
        "[MOCK] What does this look like physically? Name one object, room, or moment that grounds this abstract argument in the real world.",
    ],
)


def format_output(response: RetroResponse) -> str:
    lines = ["### 🔍 Narrative Retro", ""]

    lines.append("**1. Vocabulary Bank**")
    for entry in response.vocabulary_bank:
        alts = ", ".join(entry.alternatives)
        lines.append(f"- Instead of *{entry.vague_word}* → Use: {alts}")
    lines.append("")

    lines.append("**2. Narrative Lenses**")
    for lens in response.narrative_lenses:
        lines.append(f"- *{lens.archetype}*")
        lines.append(f"  - Issue: {lens.issue}")
        lines.append(f"  - Sculpted: {lens.sculpted}")
    lines.append("")

    lines.append("**3. Structural Interrogation**")
    for q in response.structural_interrogation:
        lines.append(f"- {q}")

    return "\n".join(lines)


def process(
    raw_text: str,
    model: str = "llama3.2:1b",
    mock: bool = False,
    dev_api: str | None = None,
    dev_model: str | None = None,
) -> str:
    if mock:
        return format_output(MOCK_RESPONSE)
    response = generate(
        raw_text,
        model=model,
        system_prompt=SYSTEM_PROMPT,
        dev_api=dev_api,
        dev_model=dev_model,
    )
    return format_output(response)
