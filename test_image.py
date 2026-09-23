import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt = """
Create a clean marketing image for an eco-friendly reusable
water bottle aimed at college students.

Style:
Modern, minimal, natural, fresh.

Show the bottle on a college campus with greenery,
soft natural lighting and a clean composition.

No text or logos.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

for part in response.candidates[0].content.parts:

    if part.text:
        print(part.text)

    elif part.inline_data:

        image = part.as_image()
        image.save("test_image.png")

        print("Image generated successfully!")
        print("Saved as: test_image.png")