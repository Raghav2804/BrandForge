import os


class ImageGenerationAgent:

    def __init__(self):
        self.output_folder = "outputs/images"

        os.makedirs(self.output_folder, exist_ok=True)

    def generate_images(self, campaign, brand):

        print("\nGenerating campaign images...")

        results = []

        # Variant 1
        image1 = self.create_visual(
            campaign,
            brand,
            "minimal"
        )

        results.append(image1)

        # Variant 2
        image2 = self.create_visual(
            campaign,
            brand,
            "campus"
        )

        results.append(image2)

        return results

    def create_visual(self, campaign, brand, style):

        brand_name = brand["brand_name"]

        primary = brand["colors"]["primary"]
        secondary = brand["colors"]["secondary"]
        background = brand["colors"]["background"]

        if style == "minimal":

            filename = os.path.join(
                self.output_folder,
                "variant_1_minimal.svg"
            )

            svg = f"""
<svg width="1080" height="1080"
     xmlns="http://www.w3.org/2000/svg">

    <rect width="1080" height="1080"
          fill="{background}"/>

    <circle cx="850" cy="180"
            r="120"
            fill="{secondary}"/>

    <rect x="390" y="220"
          width="300"
          height="600"
          rx="80"
          fill="{primary}"/>

    <rect x="430" y="300"
          width="220"
          height="400"
          rx="50"
          fill="white"/>

    <rect x="450" y="150"
          width="180"
          height="100"
          rx="30"
          fill="{primary}"/>

    <text x="540"
          y="900"
          text-anchor="middle"
          font-family="Arial"
          font-size="52"
          font-weight="bold"
          fill="{primary}">
        {brand_name}
    </text>

    <text x="540"
          y="960"
          text-anchor="middle"
          font-family="Arial"
          font-size="30"
          fill="{primary}">
        Sustainable hydration
    </text>

</svg>
"""

        else:

            filename = os.path.join(
                self.output_folder,
                "variant_2_campus.svg"
            )

            svg = f"""
<svg width="1080" height="1080"
     xmlns="http://www.w3.org/2000/svg">

    <rect width="1080"
          height="1080"
          fill="{background}"/>

    <rect y="720"
          width="1080"
          height="360"
          fill="{secondary}"/>

    <circle cx="160"
            cy="180"
            r="90"
            fill="{secondary}"/>

    <circle cx="900"
            cy="220"
            r="130"
            fill="{secondary}"/>

    <rect x="390"
          y="260"
          width="300"
          height="560"
          rx="75"
          fill="{primary}"/>

    <rect x="430"
          y="340"
          width="220"
          height="380"
          rx="45"
          fill="white"/>

    <rect x="450"
          y="190"
          width="180"
          height="100"
          rx="30"
          fill="{primary}"/>

    <text x="540"
          y="900"
          text-anchor="middle"
          font-family="Arial"
          font-size="52"
          font-weight="bold"
          fill="{primary}">
        {brand_name}
    </text>

    <text x="540"
          y="960"
          text-anchor="middle"
          font-family="Arial"
          font-size="30"
          fill="{primary}">
        Campus • Sustainable • Reusable
    </text>

</svg>
"""

        with open(filename, "w", encoding="utf-8") as file:
            file.write(svg)

        print(f"Created: {filename}")

        return {
            "style": style,
            "file": filename,
            "status": "fallback_generated",
            "message": "Image API unavailable, local branded fallback used."
        }