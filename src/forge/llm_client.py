from pydantic import BaseModel, Field
import ollama


class XRayBulletPoints(BaseModel):
    bullets: list[str] = Field(..., min_length=3, max_length=4)


class ForgeResponse(BaseModel):
    story: str
    xray: XRayBulletPoints


def generate(raw_text: str, model: str, system_prompt: str) -> ForgeResponse:
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
