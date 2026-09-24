import json

from services.llm_service import LLMService


class CopywritingAgent:

    def __init__(self):
        self.llm = LLMService()

    def create_copy(self, campaign, brand, strategy):

        prompt = f"""
You are the Copywriting Agent of BrandForge.

Create channel-specific marketing content.

CAMPAIGN:
Product: {campaign.product}
Audience: {campaign.audience}
Goal: {campaign.goal}
Key Message: {campaign.key_message}
Channels: {campaign.channels}

BRAND:
Name: {brand.get("brand_name", "")}
Voice: {brand.get("brand_voice", {})}
Do Say: {brand.get("do_say", [])}
Don't Say: {brand.get("dont_say", [])}

STRATEGY:
{json.dumps(strategy, indent=2)}

IMPORTANT RULES:

- Use the exact configured brand name.
- Use the actual product name.
- Never use a hardcoded brand name such as EcoFlow unless it is configured.
- Never assume the product type.
- Generate content specifically for the actual product.
- Generate relevant hashtags based on the product, brand, audience and campaign.
- Never create unrelated hashtags.
- Never use words from the Don't Say list.
- Do not force Do Say words if they are irrelevant.
- Do not invent unsupported claims.
- Keep the campaign message consistent across all channels.
- Create content ONLY for the selected channels.
- Follow the configured channel limits.

Instagram:
- Engaging caption
- CTA
- Relevant hashtags
- Maximum 10 hashtags

LinkedIn:
- Professional but approachable
- CTA
- Relevant hashtags
- Avoid excessive hashtags

Email:
- Subject
- Preview text
- Body
- CTA

Return ONLY valid JSON:

{{
    "instagram": {{
        "caption": "",
        "cta": "",
        "hashtags": []
    }},
    "linkedin": {{
        "post": "",
        "cta": "",
        "hashtags": []
    }},
    "email": {{
        "subject": "",
        "preview": "",
        "body": "",
        "cta": ""
    }}
}}
"""

        response = self.llm.generate(prompt)

        return json.loads(response)

    def revise_copy(
        self,
        campaign,
        brand,
        strategy,
        copy,
        qa_report
    ):

        issues = []

        for channel, result in qa_report.get(
            "checks",
            {}
        ).items():

            if isinstance(result, list):
                continue

            if result.get("status") == "FAIL":

                for issue in result.get(
                    "issues",
                    []
                ):
                    issues.append(
                        f"{channel}: {issue}"
                    )

        issue_text = "\n".join(issues)

        prompt = f"""
You are the Copywriting Revision Agent of BrandForge.

Fix ALL reported QA problems.

CAMPAIGN:
Product: {campaign.product}
Audience: {campaign.audience}
Goal: {campaign.goal}
Key Message: {campaign.key_message}
Channels: {campaign.channels}

BRAND:
Name: {brand.get("brand_name", "")}
Voice: {brand.get("brand_voice", {})}
Do Say: {brand.get("do_say", [])}
Don't Say: {brand.get("dont_say", [])}

CURRENT CONTENT:
{json.dumps(copy, indent=2)}

QA ISSUES:
{issue_text}

MANDATORY RULES:

1. Fix every QA issue.
2. Use the exact configured brand name.
3. Use the actual product name.
4. Never use EcoFlow or another unrelated brand name.
5. Never assume the product type.
6. Keep hashtags relevant to the actual product and campaign.
7. Never use any word from the Don't Say list.
8. Check ALL content fields.
9. Check captions.
10. Check posts.
11. Check email subject, preview and body.
12. Check CTAs.
13. Check hashtags.
14. Keep all channels consistent.
15. Do not introduce unsupported claims.
16. Keep the original campaign message.
17. Do not add unrelated product features.
18. Respect channel character and hashtag limits.
19. Create content only for the selected channels.
20. Return ONLY valid JSON.

Before returning, internally verify that:
- The correct brand name is used.
- The correct product is referenced.
- No forbidden words appear.
- No unrelated brand names appear.
- No unsupported claims were introduced.
- All channels remain consistent.
- Channel limits are respected.

Return:

{{
    "instagram": {{
        "caption": "",
        "cta": "",
        "hashtags": []
    }},
    "linkedin": {{
        "post": "",
        "cta": "",
        "hashtags": []
    }},
    "email": {{
        "subject": "",
        "preview": "",
        "body": "",
        "cta": ""
    }}
}}
"""

        response = self.llm.generate(prompt)

        return json.loads(response)