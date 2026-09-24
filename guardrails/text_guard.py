class TextGuard:

    def __init__(self, brand):
        self.brand = brand

    def check_text(self, text, channel):

        issues = []

        text_lower = text.lower()

        # -----------------------------
        # Check forbidden words
        # -----------------------------

        for word in self.brand.get("dont_say", []):

            if word.lower() in text_lower:

                issues.append(
                    f"Forbidden word found: {word}"
                )

        # -----------------------------
        # Check character limit
        # -----------------------------

        channel_rules = self.brand.get(
            "channel_rules",
            {}
        )

        rules = channel_rules.get(
            channel.lower(),
            {}
        )

        max_characters = rules.get(
            "max_characters"
        )

        if max_characters and len(text) > max_characters:

            issues.append(
                f"{channel} content exceeds "
                f"{max_characters} characters"
            )

        # -----------------------------
        # Check hashtag limit
        # -----------------------------

        max_hashtags = rules.get(
            "max_hashtags"
        )

        if max_hashtags:

            hashtag_count = text.count("#")

            if hashtag_count > max_hashtags:

                issues.append(
                    f"{channel} content exceeds "
                    f"{max_hashtags} hashtags"
                )

        # -----------------------------
        # Final result
        # -----------------------------

        if issues:

            return {
                "status": "FAIL",
                "issues": issues
            }

        return {
            "status": "PASS",
            "issues": []
        }