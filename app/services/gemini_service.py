from google import genai
from app.core.config import GEMINI_API_KEY

client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_recommendation(prompt: str) -> str:
    if not client:
        return "Gemini API key is not configured yet."

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return interaction.output_text

    except Exception as error:
        return f"AI recommendation error: {error}"