from forge.llm_client import (
    generate,
    RetroResponse,
    VocabularyBank,
    VocabEntry,
    StyleLenses,
    StyleLens,
    Interrogation,
)

SYSTEM_PROMPT = """You are a master writing mentor analyzing a raw draft. Do not rewrite it. Diagnose it.

1. VOCABULARY BANK: Find vague or weak words (things, stuff, very, kind of, sort of, etc.) in the text. For each one found, suggest exactly 3 precise, concrete nouns or verbs that could replace it. Find at least 1 entry.

2. STYLE LENSES: Pick 2 weak or generic sentences from the draft. Rewrite each one showing how a master writer would handle it. Label each rewrite with the lens used:
   - Hook (Thiel): Start with a contrarian claim that makes the reader argue back.
   - Macro (Harari): Zoom out to the civilizational or historical stakes behind this sentence.
   - Pacing (Lee Child): Strip it to the bone. One idea per sentence. Make it hit.

3. INTERROGATION: Ask 2 Socratic questions that expose what is missing. Focus on:
   - Missing friction (ABT framework: And, But, Therefore — where is the conflict?)
   - Missing visual anchors (what scene, object, or sensory detail is absent that would make this concrete?)

Respond with valid JSON matching the required schema. No markdown, no explanation outside the JSON."""

MOCK_RESPONSE = RetroResponse(
    vocabulary_bank=VocabularyBank(
        entries=[
            VocabEntry(
                vague_word="things",
                suggestions=["constraints", "trade-offs", "mechanisms"],
            ),
            VocabEntry(
                vague_word="stuff",
                suggestions=["infrastructure", "tooling", "boilerplate"],
            ),
        ]
    ),
    style_lenses=StyleLenses(
        rewrites=[
            StyleLens(
                label="Hook (Thiel)",
                original="[MOCK] We should think about how we communicate better.",
                sculpted="[MOCK] Most teams don't have a communication problem. They have a clarity problem disguised as one.",
            ),
            StyleLens(
                label="Pacing (Lee Child)",
                original="[MOCK] The process was slow and people were getting frustrated with the lack of progress.",
                sculpted="[MOCK] It was slow. People noticed. Nobody said anything. That was the real problem.",
            ),
        ]
    ),
    interrogation=Interrogation(
        questions=[
            "[MOCK] Where is the 'But'? What is the conflict or obstacle that makes this story worth telling?",
            "[MOCK] What does this look like physically? Name one object, room, or moment the reader can picture.",
        ]
    ),
)


def format_output(response: RetroResponse) -> str:
    lines = ["### 🔍 Narrative Retro", ""]

    lines.append("**1. Vocabulary Bank**")
    for entry in response.vocabulary_bank.entries:
        nouns = ", ".join(entry.suggestions)
        lines.append(f"- Instead of *{entry.vague_word}* → Use: {nouns}")
    lines.append("")

    lines.append("**2. Style Lenses**")
    for rewrite in response.style_lenses.rewrites:
        lines.append(f"- *{rewrite.label}:* {rewrite.original} → {rewrite.sculpted}")
    lines.append("")

    lines.append("**3. Interrogation**")
    for q in response.interrogation.questions:
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
