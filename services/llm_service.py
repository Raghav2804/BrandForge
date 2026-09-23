import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Find .env in BrandForge root folder
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)

        self.models = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-flash-lite-latest"
]

    def generate(self, prompt):

        for model in self.models:

            for attempt in range(2):

                try:

                    print(f"Trying model: {model}")

                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    return response.text

                except Exception as e:

                    print(f"{model} failed: {e}")

                    if attempt == 0:
                        time.sleep(2)
                    else:
                        time.sleep(1)

        raise RuntimeError("All Gemini models failed.")