import re


class ConsistencyGuard:

    def check(self, copy, campaign=None, brand=None):

        issues = []

        instagram = copy.get("instagram", {})
        linkedin = copy.get("linkedin", {})
        email = copy.get("email", {})

        # --------------------------------
        # Combine campaign text
        # --------------------------------

        texts = {
            "Instagram": (
                instagram.get("caption", "")
                + " "
                + instagram.get("cta", "")
            ),

            "LinkedIn": (
                linkedin.get("post", "")
                + " "
                + linkedin.get("cta", "")
            ),

            "Email": (
                email.get("subject", "")
                + " "
                + email.get("preview", "")
                + " "
                + email.get("body", "")
                + " "
                + email.get("cta", "")
            )
        }

        all_text = " ".join(
            texts.values()
        ).lower()

        # --------------------------------
        # Dynamic brand check
        # --------------------------------

        if campaign:

            product = str(
                campaign.product
            ).strip()

            if product:
                product_words = [
                    word.lower()
                    for word in product.split()
                    if len(word) > 2
                ]

                product_found = any(
                    word in all_text
                    for word in product_words
                )

                if not product_found:

                    issues.append(
                        f"Product name '{product}' "
                        "is missing from campaign content."
                    )

        # --------------------------------
        # Dynamic brand check
        # --------------------------------

        if brand:

            brand_name = brand.get(
                "brand_name",
                ""
            ).strip()

            if brand_name:

                if brand_name.lower() not in all_text:

                    issues.append(
                        f"Brand name '{brand_name}' "
                        "is missing from campaign content."
                    )

        # --------------------------------
        # Extract numeric claims
        # --------------------------------

        claims = {}

        for channel, text in texts.items():

            percentages = re.findall(
                r"\b\d+(?:\.\d+)?\s*%",
                text
            )

            prices = re.findall(
                r"(?:₹|\$|€)\s*\d+(?:\.\d+)?",
                text
            )

            durations = re.findall(
                r"\b\d+\s*(?:day|days|week|weeks|month|months)\b",
                text.lower()
            )

            claims[channel] = {
                "percentages": percentages,
                "prices": prices,
                "durations": durations
            }

        # --------------------------------
        # Percentage consistency
        # --------------------------------

        percentage_values = []

        for channel in claims:

            for value in claims[channel]["percentages"]:

                number = re.search(
                    r"\d+(?:\.\d+)?",
                    value
                )

                if number:

                    percentage_values.append(
                        float(number.group())
                    )

        if percentage_values:

            if len(set(percentage_values)) > 1:

                issues.append(
                    "Contradictory percentage claims "
                    "found across channels."
                )

        # --------------------------------
        # Price consistency
        # --------------------------------

        price_values = []

        for channel in claims:

            for value in claims[channel]["prices"]:

                number = re.search(
                    r"\d+(?:\.\d+)?",
                    value
                )

                if number:

                    price_values.append(
                        float(number.group())
                    )

        if price_values:

            if len(set(price_values)) > 1:

                issues.append(
                    "Contradictory price claims "
                    "found across channels."
                )

        # --------------------------------
        # Duration consistency
        # --------------------------------

        duration_values = []

        for channel in claims:

            duration_values.extend(
                claims[channel]["durations"]
            )

        if duration_values:

            normalized = [
                value.lower()
                for value in duration_values
            ]

            if len(set(normalized)) > 1:

                issues.append(
                    "Contradictory duration claims "
                    "found across channels."
                )

        # --------------------------------
        # Final result
        # --------------------------------

        if issues:

            return {
                "status": "FAIL",
                "issues": issues,
                "claims": claims
            }

        return {
            "status": "PASS",
            "issues": [],
            "claims": claims
        }