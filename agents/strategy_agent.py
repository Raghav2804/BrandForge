import json

from services.llm_service import LLMService


class StrategyAgent:

    def __init__(self):
        self.llm = LLMService()

    def create_strategy(self, campaign, brand):

        prompt = f"""
You are the Strategy Agent of BrandForge,
an AI-powered marketing agency.

Create a complete marketing strategy for this campaign.

CAMPAIGN:
Product: {campaign.product}
Target Audience: {campaign.audience}
Goal: {campaign.goal}
Key Message: {campaign.key_message}
Channels: {campaign.channels}

BRAND:
Brand Name: {brand.get("brand_name", "")}
Brand Voice: {brand.get("brand_voice", {})}
Visual Style: {brand.get("visual_style", [])}
Do Say: {brand.get("do_say", [])}
Don't Say: {brand.get("dont_say", [])}

IMPORTANT:
- Make the strategy specific to the actual product.
- Do not assume the product type.
- Adapt the strategy to the selected channels only.
- Keep messaging consistent across channels.
- Do not invent unsupported product claims.
- Respect the brand voice and visual style.
- Use channel-specific content formats.
- Return ONLY valid JSON.
- Do not add markdown or explanations.

Use exactly this structure:

{{
    "campaign_theme": "...",
    "key_messages": [
        "...",
        "..."
    ],
    "channel_strategy": {{
        "instagram": {{
            "content_types": [],
            "purpose": "",
            "cadence": ""
        }},
        "linkedin": {{
            "content_types": [],
            "purpose": "",
            "cadence": ""
        }},
        "email": {{
            "content_types": [],
            "purpose": "",
            "cadence": ""
        }}
    }}
}}
"""

        response = self.llm.generate(prompt)

        return json.loads(response)