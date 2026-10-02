from forge.llm_client import generate, ForgeResponse, XRayBulletPoints

SYSTEM_PROMPT = """You are a master narrative editor and writing tutor. Your job is to take raw, dictated thoughts and transform them into a concise, captivating story.

1. THE STORY: Rewrite the text to have relentless narrative drive.
- Move the most contrarian or surprising truth to the very first sentence to hook the reader.
- Replace all vague placeholder words ('things', 'stuff', 'like') with exact, concrete nouns.
- Use kinetic, rhythmic pacing (short sentences for complex ideas).
- Create a tension gap: do not give the core answer away immediately; make the reader wait for it.
- Keep the author's authentic, human voice, but make it punchy and captivating. Do not sound corporate or robotic.

2. THE X-RAY: Explain what you changed. Write exactly 3 to 4 brief bullet points explaining the specific storytelling mechanics (e.g., pacing, hooks) or vocabulary replacements (e.g., what concrete noun replaced 'stuff') you applied so the author can learn from your edits.

Respond with valid JSON matching the required schema. No markdown, no explanation outside the JSON."""

MOCK_RESPONSE = ForgeResponse(
    story="[MOCK] Most teams ship the wrong thing perfectly. This is a placeholder polished narrative confirming the clipboard pipeline, notification bridge, and formatter are all wired correctly.",
    xray=XRayBulletPoints(bullets=[
        "Hook: Contrarian opener placed first to test the story formatter.",
        "Pacing: Single declarative sentence verifies the clipboard write path.",
        "Voice: Placeholder preserves casual register to confirm notification delivery.",
    ]),
)


def format_output(response: ForgeResponse) -> str:
    bullets = "\n".join(f"- {b}" for b in response.xray.bullets)
    return f"[THE STORY]\n{response.story}\n\n---\n[THE X-RAY]\n{bullets}"


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
