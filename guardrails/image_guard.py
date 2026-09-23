import os
import re


class ImageGuard:

    def __init__(self, brand):
        self.brand = brand

        self.brand_colors = [
            brand["colors"]["primary"],
            brand["colors"]["secondary"],
            brand["colors"]["background"]
        ]

        # Neutral colors are normally safe in designs
        self.allowed_neutrals = [
            "#FFFFFF",
            "#000000"
        ]

        # Maximum RGB distance allowed
        self.tolerance = 60

    def hex_to_rgb(self, color):

        color = color.replace("#", "")

        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16)
        )

    def color_distance(self, color1, color2):

        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)

        return (
            (r1 - r2) ** 2
            + (g1 - g2) ** 2
            + (b1 - b2) ** 2
        ) ** 0.5

    def is_brand_color(self, color):

        color = color.upper()

        # Allow neutral colors
        if color in [
            c.upper() for c in self.allowed_neutrals
        ]:
            return True

        for brand_color in self.brand_colors:

            distance = self.color_distance(
                color,
                brand_color
            )

            if distance <= self.tolerance:
                return True

        return False

    def check_image(self, image):

        issues = []

        file_path = image.get("file")

        # -----------------------------
        # Check file
        # -----------------------------

        if not file_path:

            return {
                "status": "FAIL",
                "issues": ["Image file path is missing."]
            }

        if not os.path.exists(file_path):

            return {
                "status": "FAIL",
                "issues": [
                    f"Image file not found: {file_path}"
                ]
            }

        # -----------------------------
        # Read SVG
        # -----------------------------

        if file_path.lower().endswith(".svg"):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            colors = re.findall(
                r'#[0-9A-Fa-f]{6}',
                content
            )

            unique_colors = set(
                color.upper()
                for color in colors
            )

            # -----------------------------
            # Check colors
            # -----------------------------

            for color in unique_colors:

                if not self.is_brand_color(color):

                    issues.append(
                        f"Off-brand color detected: {color}"
                    )

        else:

            issues.append(
                "Image format is not SVG, so "
                "color validation was skipped."
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