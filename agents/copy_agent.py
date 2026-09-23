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

BRAND:
Name: {brand["brand_name"]}
Voice: {brand["brand_voice"]}
Do Say: {brand["do_say"]}
Don't Say: {brand["dont_say"]}

STRATEGY:
{json.dumps(strategy, indent=2)}

Create content for:
1. Instagram
2. LinkedIn
3. Email

Rules:

Instagram:
- Engaging caption
- CTA
- Relevant hashtags

LinkedIn:
- Professional but approachable
- CTA
- Avoid excessive hashtags

Email:
- Subject
- Preview text
- Body
- CTA

IMPORTANT:
- Never use words from the Don't Say list.
- Keep all channels consistent.
- Do not create unsupported claims.

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

        for channel, result in qa_report["checks"].items():

            if isinstance(result, list):
                continue

            if result["status"] == "FAIL":

                for issue in result["issues"]:

                    issues.append(
                        f"{channel}: {issue}"
                    )

        issue_text = "\n".join(issues)

        prompt = f"""
You are the Copywriting Revision Agent of BrandForge.

The Brand Guardrail found problems in the campaign.

Your job is to FIX ALL reported problems.

CAMPAIGN:
Product: {campaign.product}
Audience: {campaign.audience}
Goal: {campaign.goal}
Key Message: {campaign.key_message}

BRAND:
Name: {brand["brand_name"]}
Voice: {brand["brand_voice"]}
Do Say: {brand["do_say"]}
Don't Say: {brand["dont_say"]}

CURRENT CONTENT:
{json.dumps(copy, indent=2)}

QA ISSUES:
{issue_text}

MANDATORY RULES:

1. Fix every QA issue.
2. NEVER use any word from the Don't Say list.
3. Check ALL fields before returning.
4. Check captions.
5. Check posts.
6. Check email subject, preview and body.
7. Check CTAs.
8. Check hashtags.
9. Keep all channels consistent.
10. Do not introduce unsupported claims.
11. Keep the original campaign message.
12. Return ONLY valid JSON.

Before returning the answer, internally verify that
none of the forbidden words appear in the final content.

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