from forge.llm_client import generate, ForgeResponse

SYSTEM_PROMPT = """You are a master narrative editor and writing tutor. Your job is to take raw, dictated thoughts and transform them into a concise, captivating story.

1. THE STORY: Rewrite the text to have relentless narrative drive.
- Move the most contrarian or surprising truth to the very first sentence to hook the reader.
- Replace all vague placeholder words ('things', 'stuff', 'like') with exact, concrete nouns.
- Use kinetic, rhythmic pacing (short sentences for complex ideas).
- Create a tension gap: do not give the core answer away immediately; make the reader wait for it.
- Keep the author's authentic, human voice, but make it punchy and captivating. Do not sound corporate or robotic.

2. THE X-RAY: Explain what you changed. Write exactly 3 to 4 brief bullet points explaining the specific storytelling mechanics (e.g., pacing, hooks) or vocabulary replacements (e.g., what concrete noun replaced 'stuff') you applied so the author can learn from your edits.

Respond with valid JSON matching the required schema. No markdown, no explanation outside the JSON."""


def format_output(response: ForgeResponse) -> str:
    bullets = "\n".join(f"- {b}" for b in response.xray.bullets)
    return f"[THE STORY]\n{response.story}\n\n---\n[THE X-RAY]\n{bullets}"


def process(raw_text: str, model: str = "llama3.2:1b") -> str:
    response = generate(raw_text, model=model, system_prompt=SYSTEM_PROMPT)
    return format_output(response)
