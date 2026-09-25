import json
import logging
from google import genai
from google.genai import types
from app.config import settings
log = logging.getLogger(__name__)

class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    def generate(self, prompt: str, image: bytes | None = None, mime: str | None = None):
        if not self.client:
            return None
        parts = [prompt]
        if image and mime:
            parts.append(types.Part.from_bytes(data=image, mime_type=mime))
        try:
            result = self.client.models.generate_content(
                model=settings.gemini_model,
                contents=parts,
                config=types.GenerateContentConfig(temperature=0.4, response_mime_type="application/json"),
            )
            return json.loads(result.text or "{}")
        except Exception as exc:
            log.exception("Gemini request failed: %s", exc)
            return None

gemini = Gemini()
