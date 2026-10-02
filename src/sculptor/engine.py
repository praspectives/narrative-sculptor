from sculptor.llm_client import (
    generate,
    RetroResponse,
    VocabularyCorrection,
    NarrativeLens,
)

SYSTEM_PROMPT = """You are an elite narrative post-mortem analyzer. Analyze the user's ENTIRE raw draft and provide a comprehensive pedagogical Retro.

1. THE VOCABULARY BANK: Scan the ENTIRE draft for vague placeholder words, abstract fluff, and weak verbs. Provide precise, context-accurate noun/verb alternatives for ALL major instances you find. Do not limit yourself to a fixed number — cover every significant weakness in the draft.

2. THE NARRATIVE LENSES: Scan the ENTIRE draft for stylistic dead zones: weak hooks, poor pacing, lack of sensory detail, flat exposition, buried tension. Identify the most critical weak sections. For each, dynamically select a Master Storyteller Archetype (e.g., a technothriller author for flat exposition, a contrarian essayist for a weak hook, a nature writer for missing sensory detail) that best solves the specific flaw. Show exactly how that archetype would rewrite that section. Do not limit yourself to specific named authors — use the narrative style best suited to fix the exact failure. Cover all major stylistic dead zones you find.

3. THE STRUCTURAL INTERROGATION: Analyze the overall architecture of the ENTIRE draft. Identify ALL major structural misses: missing ABT friction (And / But / Therefore), buried thesis, lack of micro-to-macro visual anchors, unearned conclusions, missing stakes. Ask a piercing Socratic question for each structural gap you find. Force the author to rethink every weak architectural choice.

Respond with valid JSON matching the required schema. No markdown, no explanation outside the JSON."""

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
