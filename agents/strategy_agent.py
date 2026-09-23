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
Brand Name: {brand["brand_name"]}
Brand Voice: {brand["brand_voice"]}
Visual Style: {brand["visual_style"]}
Do Say: {brand["do_say"]}
Don't Say: {brand["dont_say"]}

Return ONLY valid JSON.

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