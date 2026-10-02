import os
from pydantic import BaseModel, Field
import ollama
from dotenv import load_dotenv

load_dotenv()


class XRayBulletPoints(BaseModel):
    bullets: list[str] = Field(..., min_length=3, max_length=4)


class ForgeResponse(BaseModel):
    story: str
    xray: XRayBulletPoints


def _generate_ollama(raw_text: str, model: str, system_prompt: str) -> ForgeResponse:
    client = ollama.Client()
    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text},
        ],
        format=ForgeResponse.model_json_schema(),
    )
    return ForgeResponse.model_validate_json(response.message.content)


def _generate_anthropic(raw_text: str, system_prompt: str, model: str) -> ForgeResponse:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("Anthropic SDK not installed. Run: uv pip install 'storytellers-forge[dev-api]'")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment or .env file")

    schema = ForgeResponse.model_json_schema()
    full_prompt = (
        f"{system_prompt}\n\nYou MUST respond with valid JSON matching this schema exactly:\n"
        f"{schema}\n\nRespond with JSON only. No markdown, no explanation."
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model or "claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=full_prompt,
        messages=[{"role": "user", "content": raw_text}],
    )
    return ForgeResponse.model_validate_json(response.content[0].text)


def _generate_groq(raw_text: str, system_prompt: str, model: str) -> ForgeResponse:
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("OpenAI SDK not installed. Run: uv pip install 'storytellers-forge[dev-api]'")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set in environment or .env file")

    schema = ForgeResponse.model_json_schema()
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    response = client.chat.completions.create(
        model=model or "llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"{system_prompt}\n\nRespond with valid JSON matching this schema: {schema}"},
            {"role": "user", "content": raw_text},
        ],
        response_format={"type": "json_object"},
    )
    return ForgeResponse.model_validate_json(response.choices[0].message.content)


def _generate_openai(raw_text: str, system_prompt: str, model: str) -> ForgeResponse:
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("OpenAI SDK not installed. Run: uv pip install 'storytellers-forge[dev-api]'")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment or .env file")

    schema = ForgeResponse.model_json_schema()
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model or "gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_prompt}\n\nRespond with valid JSON matching this schema: {schema}"},
            {"role": "user", "content": raw_text},
        ],
        response_format={"type": "json_object"},
    )
    return ForgeResponse.model_validate_json(response.choices[0].message.content)


def generate(
    raw_text: str,
    model: str,
    system_prompt: str,
    dev_api: str | None = None,
    dev_model: str | None = None,
) -> ForgeResponse:
    provider = dev_api or os.getenv("DEV_API")
    if provider == "anthropic":
        return _generate_anthropic(raw_text, system_prompt, dev_model or "")
    if provider == "groq":
        return _generate_groq(raw_text, system_prompt, dev_model or "")
    if provider == "openai":
        return _generate_openai(raw_text, system_prompt, dev_model or "")
    return _generate_ollama(raw_text, model, system_prompt)
