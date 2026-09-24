import os


class ImageGenerationAgent:

    def __init__(self):
        self.output_folder = "outputs/images"
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_images(self, campaign, brand):

        print("\nGenerating campaign images...")

        return [
            self.create_visual(campaign, brand, "minimal"),
            self.create_visual(campaign, brand, "campus")
        ]

    def create_visual(self, campaign, brand, style):

        brand_name = brand.get("brand_name", "Brand")
        product = campaign.product.strip()
        product_lower = product.lower()

        colors = brand.get("colors", {})

        primary = colors.get("primary", "#1B5E20")
        secondary = colors.get("secondary", "#81C784")
        background = colors.get("background", "#F5F5F5")

        if "lamp" in product_lower or "light" in product_lower:

            product_shape = f"""
            <rect x="475" y="360" width="130" height="300"
                  rx="35" fill="{primary}"/>
            <path d="M540 360 L380 220 L700 220 Z"
                  fill="{primary}"/>
            <path d="M420 225 L660 225 L540 80 Z"
                  fill="{secondary}" opacity="0.8"/>
            <rect x="350" y="650" width="380" height="35"
                  rx="15" fill="{primary}"/>
            <circle cx="540" cy="675" r="18" fill="white"/>
            """

        elif (
            "shoe" in product_lower
            or "sneaker" in product_lower
            or "footwear" in product_lower
        ):

            product_shape = f"""
            <path d="
                M300 600
                C400 590 470 500 520 400
                L650 470
                C700 500 760 560 850 610
                L850 680
                L300 680 Z"
                fill="{primary}"/>

            <path d="
                M320 640
                L850 640
                L850 700
                L300 700
                Q280 670 320 640 Z"
                fill="{secondary}"/>

            <line x1="520" y1="470" x2="650" y2="530"
                  stroke="white" stroke-width="12"/>

            <line x1="500" y1="510" x2="630" y2="570"
                  stroke="white" stroke-width="12"/>
            """

        elif (
            "laptop" in product_lower
            or "computer" in product_lower
        ):

            product_shape = f"""
            <rect x="300" y="300" width="480" height="300"
                  rx="20" fill="{primary}"/>

            <rect x="330" y="330" width="420" height="240"
                  rx="10" fill="white"/>

            <path d="
                M230 650
                L850 650
                L790 710
                L290 710 Z"
                fill="{secondary}"/>

            <circle cx="540" cy="680" r="12"
                    fill="{primary}"/>
            """

        elif (
            "phone" in product_lower
            or "mobile" in product_lower
        ):

            product_shape = f"""
            <rect x="390" y="180" width="300" height="620"
                  rx="45" fill="{primary}"/>

            <rect x="420" y="230" width="240" height="500"
                  rx="20" fill="white"/>

            <circle cx="540" cy="765" r="15"
                    fill="{secondary}"/>
            """

        else:

            product_shape = f"""
            <rect x="360" y="300" width="360" height="400"
                  rx="60" fill="{primary}"/>

            <circle cx="540" cy="470" r="100"
                    fill="{secondary}"/>

            <rect x="440" y="620" width="200" height="35"
                  rx="15" fill="white"/>
            """

        product_text = (
            product
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        brand_text = (
            brand_name
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        if style == "minimal":

            filename = os.path.join(
                self.output_folder,
                "variant_1_minimal.svg"
            )

            svg = f"""
<svg width="1080" height="1080"
     viewBox="0 0 1080 1080"
     xmlns="http://www.w3.org/2000/svg">

    <rect width="1080" height="1080" fill="{background}"/>

    <circle cx="870" cy="180" r="130"
            fill="{secondary}"/>

    {product_shape}

    <text x="540" y="850"
          text-anchor="middle"
          font-family="Arial"
          font-size="40"
          font-weight="bold"
          fill="{primary}">
        {product_text}
    </text>

    <text x="540" y="910"
          text-anchor="middle"
          font-family="Arial"
          font-size="28"
          fill="{primary}">
        {brand_text}
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
     viewBox="0 0 1080 1080"
     xmlns="http://www.w3.org/2000/svg">

    <rect width="1080" height="1080"
          fill="{background}"/>

    <rect y="760" width="1080" height="320"
          fill="{secondary}"/>

    <circle cx="150" cy="180" r="90"
            fill="{secondary}"/>

    <circle cx="920" cy="230" r="120"
            fill="{secondary}"/>

    {product_shape}

    <text x="540" y="870"
          text-anchor="middle"
          font-family="Arial"
          font-size="40"
          font-weight="bold"
          fill="{primary}">
        {product_text}
    </text>

    <text x="540" y="930"
          text-anchor="middle"
          font-family="Arial"
          font-size="28"
          fill="{primary}">
        {brand_text}
    </text>

</svg>
"""

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(svg)

        print(f"Created: {filename}")

        return {
            "style": style,
            "file": filename,
            "status": "fallback_generated",
            "message": "Product-aware local visual generated."
        }