from guardrails.text_guard import TextGuard
from guardrails.consistency_guard import ConsistencyGuard
from guardrails.image_guard import ImageGuard


class QAEngine:

    def __init__(self, brand):

        self.text_guard = TextGuard(brand)
        self.consistency_guard = ConsistencyGuard()
        self.image_guard = ImageGuard(brand)

    def check_campaign(self, copy, images=None):

        results = {}

        # -----------------------------
        # Instagram
        # -----------------------------

        instagram_text = (
            copy["instagram"]["caption"]
            + " "
            + copy["instagram"]["cta"]
        )

        results["instagram"] = self.text_guard.check_text(
            instagram_text,
            "instagram"
        )

        # -----------------------------
        # LinkedIn
        # -----------------------------

        linkedin_text = (
            copy["linkedin"]["post"]
            + " "
            + copy["linkedin"]["cta"]
        )

        results["linkedin"] = self.text_guard.check_text(
            linkedin_text,
            "linkedin"
        )

        # -----------------------------
        # Email
        # -----------------------------

        email_text = (
            copy["email"]["subject"]
            + " "
            + copy["email"]["preview"]
            + " "
            + copy["email"]["body"]
            + " "
            + copy["email"]["cta"]
        )

        results["email"] = self.text_guard.check_text(
            email_text,
            "email"
        )

        # -----------------------------
        # Consistency
        # -----------------------------

        results["consistency"] = (
            self.consistency_guard.check(copy)
        )

        # -----------------------------
        # Image Checks
        # -----------------------------

        results["images"] = []

        if images:

            for image in images:

                image_result = self.image_guard.check_image(
                    image
                )

                results["images"].append({
                    "style": image.get("style", "unknown"),
                    **image_result
                })

        # -----------------------------
        # Overall Status
        # -----------------------------

        failed = False

        for result in results.values():

            if isinstance(result, list):

                for image_result in result:

                    if image_result["status"] == "FAIL":
                        failed = True

            else:

                if result["status"] == "FAIL":
                    failed = True

        if failed:
            overall = "FAIL"
        else:
            overall = "PASS"

        return {
            "overall_status": overall,
            "checks": results
        }