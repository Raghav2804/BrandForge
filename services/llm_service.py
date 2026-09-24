import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(
            api_key=api_key
        )

        self.models = [
            "gemini-flash-lite-latest",
            "gemini-3.6-flash",
            "gemini-3.7-flash",
            "gemini-3.5-flash-lite"
        ]

    def generate(self, prompt):

        last_error = None

        for model in self.models:

            print(f"\nTrying model: {model}")

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    print(f"Success: {model}")
                    return response.text

                print(f"{model} returned empty response.")

            except Exception as e:

                last_error = e
                error_text = str(e)

                print(
                    f"{model} failed: {error_text}"
                )

                if "503" in error_text or "429" in error_text:
                    print(
                        "Temporary Gemini issue. "
                        "Trying next model..."
                    )

                continue

        raise RuntimeError(
            "All Gemini models failed. "
            f"Last error: {last_error}"
        )