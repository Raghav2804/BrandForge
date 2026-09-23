import re


class ConsistencyGuard:

    def check(self, copy):

        issues = []

        instagram = copy["instagram"]
        linkedin = copy["linkedin"]
        email = copy["email"]

        # --------------------------------
        # Combine all campaign text
        # --------------------------------

        texts = {
            "Instagram": (
                instagram["caption"]
                + " "
                + instagram["cta"]
            ),
            "LinkedIn": (
                linkedin["post"]
                + " "
                + linkedin["cta"]
            ),
            "Email": (
                email["subject"]
                + " "
                + email["preview"]
                + " "
                + email["body"]
                + " "
                + email["cta"]
            )
        }

        all_text = " ".join(
            texts.values()
        ).lower()

        # --------------------------------
        # Brand name check
        # --------------------------------

        if "ecoflow" not in all_text:

            issues.append(
                "Brand name EcoFlow is missing "
                "from campaign content."
            )

        # --------------------------------
        # Main message check
        # --------------------------------

        if "sustainable" not in all_text:

            issues.append(
                "Main sustainability message "
                "is missing."
            )

        # --------------------------------
        # Extract numeric claims
        # --------------------------------

        claims = {}

        for channel, text in texts.items():

            percentages = re.findall(
                r'\b\d+(?:\.\d+)?\s*%',
                text
            )

            prices = re.findall(
                r'(?:₹|\$|€)\s*\d+(?:\.\d+)?',
                text
            )

            durations = re.findall(
                r'\b\d+\s*(?:day|days|week|weeks|month|months)\b',
                text.lower()
            )

            claims[channel] = {
                "percentages": percentages,
                "prices": prices,
                "durations": durations
            }

        # --------------------------------
        # Check percentage consistency
        # --------------------------------

        percentage_values = []

        for channel in claims:

            for value in claims[channel]["percentages"]:

                number = re.search(
                    r'\d+(?:\.\d+)?',
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
        # Check price consistency
        # --------------------------------

        price_values = []

        for channel in claims:

            for value in claims[channel]["prices"]:

                number = re.search(
                    r'\d+(?:\.\d+)?',
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
        # Check duration consistency
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