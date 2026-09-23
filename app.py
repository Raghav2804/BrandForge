import json
import os
import base64
import streamlit as st

from models.campaign import Campaign
from orchestrator.workflow import BrandForgeWorkflow
from assembly.exporter import CampaignExporter
from assembly.calendar import CampaignCalendar


st.set_page_config(
    page_title="BrandForge",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 BrandForge")
st.subheader("Create. Validate. Launch.")

st.write(
    "AI-powered multi-agent marketing agency that "
    "turns one campaign brief into a complete "
    "multi-channel marketing package."
)

st.divider()


# ==========================================
# LOAD BRAND CONFIG
# ==========================================

with open(
    "config/brand_kit.json",
    "r",
    encoding="utf-8"
) as file:

    brand = json.load(file)


# ==========================================
# CAMPAIGN BRIEF
# ==========================================

st.header("📋 Campaign Brief")

product = st.text_input(
    "Product",
    value="Eco-friendly Water Bottle"
)

audience = st.text_input(
    "Target Audience",
    value="College Students"
)

goal = st.text_input(
    "Campaign Goal",
    value="Increase product awareness"
)

key_message = st.text_area(
    "Key Message",
    value="Sustainable hydration for everyday life"
)

channels = st.multiselect(
    "Marketing Channels",
    ["Instagram", "LinkedIn", "Email"],
    default=[
        "Instagram",
        "LinkedIn",
        "Email"
    ]
)


# ==========================================
# BUTTONS
# ==========================================

generate_button = st.button(
    "🚀 Generate Campaign",
    use_container_width=True
)

test_button = st.button(
    "🧪 Test Brand Guardrails",
    use_container_width=True
)


# ==========================================
# GUARDRAIL TEST
# ==========================================

if test_button:

    st.header("🧪 Guardrail Test")

    st.info(
        "BrandForge will intentionally create invalid "
        "content, detect the violation, revise it, "
        "and run QA again."
    )

    test_word = brand["dont_say"][0]

    st.write(
        f"Testing forbidden word: **{test_word}**"
    )

    # ------------------------------------------
    # Intentionally invalid copy
    # ------------------------------------------

    test_copy = {
        "instagram": {
            "caption": (
                f"This is a {test_word} product."
            ),
            "cta": "Buy now",
            "hashtags": []
        },

        "linkedin": {
            "post": (
                f"Our product is {test_word}."
            ),
            "cta": "Learn more",
            "hashtags": []
        },

        "email": {
            "subject": "Product Offer",
            "preview": "Special product message",
            "body": (
                f"This product is {test_word}."
            ),
            "cta": "Shop now"
        }
    }

    test_campaign = Campaign(
        product="Eco-friendly Water Bottle",
        audience="College Students",
        goal="Increase product awareness",
        key_message="Sustainable hydration",
        channels=[
            "Instagram",
            "LinkedIn",
            "Email"
        ]
    )

    workflow = BrandForgeWorkflow(brand)

    # ------------------------------------------
    # Initial QA
    # ------------------------------------------

    st.subheader("1️⃣ Initial QA")

    initial_qa = workflow.qa_engine.check_campaign(
        test_copy,
        []
    )

    if initial_qa["overall_status"] == "FAIL":

        st.error(
            "❌ Guardrail detected a violation."
        )

        for channel, result in initial_qa["checks"].items():

            if isinstance(result, list):
                continue

            if result["status"] == "FAIL":

                st.write(
                    f"**{channel.title()}**"
                )

                for issue in result["issues"]:

                    st.write(
                        f"⚠️ {issue}"
                    )

    else:

        st.error(
            "❌ Guardrail test failed."
        )

    # ------------------------------------------
    # Automatic Revision
    # ------------------------------------------

    st.subheader(
        "2️⃣ Automatic Revision"
    )

    if initial_qa["overall_status"] == "FAIL":

        with st.spinner(
            "🤖 Revising invalid content..."
        ):

            revised_copy = workflow.copy_agent.revise_copy(
                test_campaign,
                brand,
                {},
                test_copy,
                initial_qa
            )

        st.success(
            "✅ Revision generated."
        )

        # ------------------------------------------
        # Recheck
        # ------------------------------------------

        st.subheader(
            "3️⃣ Recheck"
        )

        final_qa = workflow.qa_engine.check_campaign(
            revised_copy,
            []
        )

        if final_qa["overall_status"] == "PASS":

            st.success(
                "✅ PASS — violation fixed successfully."
            )

        else:

            st.error(
                "❌ FAIL — content still requires review."
            )

        with st.expander(
            "🔍 View Test QA Report"
        ):

            st.json(
                final_qa
            )


# ==========================================
# GENERATE CAMPAIGN
# ==========================================

if generate_button:

    # ----------------------------------------
    # Input validation
    # ----------------------------------------

    if not product.strip():

        st.warning(
            "Please enter a product."
        )

        st.stop()

    if not audience.strip():

        st.warning(
            "Please enter a target audience."
        )

        st.stop()

    if not goal.strip():

        st.warning(
            "Please enter a campaign goal."
        )

        st.stop()

    if not key_message.strip():

        st.warning(
            "Please enter a key message."
        )

        st.stop()

    if not channels:

        st.warning(
            "Please select at least one channel."
        )

        st.stop()

    campaign = Campaign(
        product=product,
        audience=audience,
        goal=goal,
        key_message=key_message,
        channels=channels
    )

    # ==========================================
    # WORKFLOW
    # ==========================================

    with st.status(
        "🚀 BrandForge is building your campaign...",
        expanded=True
    ) as status:

        st.write(
            "🧠 Strategy Agent: creating strategy..."
        )

        workflow = BrandForgeWorkflow(brand)

        result = workflow.run(campaign)

        strategy = result["strategy"]
        copy = result["copy"]
        images = result["images"]
        qa_report = result["qa_report"]

        st.write(
            "✍️ Copywriting Agent: creating content..."
        )

        st.write(
            "🎨 Image Agent: creating visual variants..."
        )

        st.write(
            "🛡️ Brand Guardrail: validating campaign..."
        )

        status.update(
            label="✅ Campaign generation complete!",
            state="complete"
        )

    # ==========================================
    # EXPORT
    # ==========================================

    with st.spinner(
        "📦 Packaging campaign..."
    ):

        exporter = CampaignExporter()

        zip_file = exporter.export(
            campaign,
            strategy,
            copy,
            images,
            qa_report
        )

    st.divider()

    # ==========================================
    # CAMPAIGN RESULTS
    # ==========================================

    st.header("📊 Campaign Results")

    # ==========================================
    # STRATEGY
    # ==========================================

    with st.expander(
        "🧠 Marketing Strategy",
        expanded=True
    ):

        st.write(
            f"**Campaign Theme:** "
            f"{strategy['campaign_theme']}"
        )

        st.write("**Key Messages:**")

        for message in strategy["key_messages"]:

            st.write(
                f"• {message}"
            )

        st.write("**Channel Strategy:**")

        st.json(
            strategy["channel_strategy"]
        )

    # ==========================================
    # GENERATED CONTENT
    # ==========================================

    st.header("✍️ Generated Content")

    tab1, tab2, tab3 = st.tabs(
        [
            "📸 Instagram",
            "💼 LinkedIn",
            "📧 Email"
        ]
    )

    # ----------------------------------------
    # Instagram
    # ----------------------------------------

    with tab1:

        st.subheader("Instagram")

        st.write(
            copy["instagram"]["caption"]
        )

        st.write("**CTA**")

        st.info(
            copy["instagram"]["cta"]
        )

        st.write("**Hashtags**")

        st.write(
            " ".join(
                copy["instagram"]["hashtags"]
            )
        )

    # ----------------------------------------
    # LinkedIn
    # ----------------------------------------

    with tab2:

        st.subheader("LinkedIn")

        st.write(
            copy["linkedin"]["post"]
        )

        st.write("**CTA**")

        st.info(
            copy["linkedin"]["cta"]
        )

        st.write("**Hashtags**")

        st.write(
            " ".join(
                copy["linkedin"]["hashtags"]
            )
        )

    # ----------------------------------------
    # Email
    # ----------------------------------------

    with tab3:

        st.subheader("Email")

        st.write("**Subject**")

        st.write(
            copy["email"]["subject"]
        )

        st.write("**Preview Text**")

        st.write(
            copy["email"]["preview"]
        )

        st.write("**Email Body**")

        st.write(
            copy["email"]["body"]
        )

        st.write("**CTA**")

        st.info(
            copy["email"]["cta"]
        )

    # ==========================================
    # VISUAL VARIANTS
    # ==========================================

    st.header("🎨 Visual Variants")

    image_columns = st.columns(
        len(images)
    )

    for i, image in enumerate(images):

        with image_columns[i]:

            st.subheader(
                image["style"].title()
            )

            file_path = image["file"]

            st.write(
                f"Generation: `{image['status']}`"
            )

            if os.path.exists(file_path):

                if file_path.lower().endswith(".svg"):

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        svg_data = file.read()

                    svg_base64 = base64.b64encode(
                        svg_data.encode("utf-8")
                    ).decode("utf-8")

                    st.markdown(
                        f"""
                        <div style="
                            width:100%;
                            background:white;
                            border-radius:12px;
                            padding:10px;
                            border:1px solid #ddd;
                        ">
                            <img
                                src="data:image/svg+xml;base64,{svg_base64}"
                                style="
                                    width:100%;
                                    height:auto;
                                "
                            >
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.image(
                        file_path,
                        use_container_width=True
                    )

            st.caption(
                image["message"]
            )

    # ==========================================
    # BRAND QA
    # ==========================================

    st.header("🛡️ Brand QA Report")

    final_status = qa_report.get(
        "final_status",
        qa_report["overall_status"]
    )

    revision_attempts = qa_report.get(
        "revision_attempts",
        0
    )

    if final_status == "PASS":

        st.success(
            "✅ Campaign passed brand consistency checks."
        )

    else:

        st.error(
            "⚠️ Campaign requires human review."
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Revision Attempts",
            revision_attempts
        )

    with col2:

        st.metric(
            "Final Status",
            final_status
        )

    checks = qa_report["checks"]

    # ==========================================
    # CHANNEL QA
    # ==========================================

    st.subheader("Channel Checks")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if checks["instagram"]["status"] == "PASS":

            st.success(
                "Instagram\n\n✅ PASS"
            )

        else:

            st.error(
                "Instagram\n\n❌ FAIL"
            )

    with col2:

        if checks["linkedin"]["status"] == "PASS":

            st.success(
                "LinkedIn\n\n✅ PASS"
            )

        else:

            st.error(
                "LinkedIn\n\n❌ FAIL"
            )

    with col3:

        if checks["email"]["status"] == "PASS":

            st.success(
                "Email\n\n✅ PASS"
            )

        else:

            st.error(
                "Email\n\n❌ FAIL"
            )

    with col4:

        if checks["consistency"]["status"] == "PASS":

            st.success(
                "Consistency\n\n✅ PASS"
            )

        else:

            st.error(
                "Consistency\n\n❌ FAIL"
            )

    # ==========================================
    # IMAGE QA
    # ==========================================

    st.subheader("Image Checks")

    image_checks = checks.get(
        "images",
        []
    )

    if image_checks:

        image_cols = st.columns(
            len(image_checks)
        )

        for i, image_check in enumerate(
            image_checks
        ):

            with image_cols[i]:

                style = image_check.get(
                    "style",
                    f"Image {i + 1}"
                )

                if image_check["status"] == "PASS":

                    st.success(
                        f"{style.title()}\n\n✅ PASS"
                    )

                else:

                    st.error(
                        f"{style.title()}\n\n❌ FAIL"
                    )

                for issue in image_check.get(
                    "issues",
                    []
                ):

                    st.caption(
                        f"⚠️ {issue}"
                    )

    else:

        st.info(
            "No image QA results available."
        )

    # ==========================================
    # DETAILED QA
    # ==========================================

    with st.expander(
        "🔍 View Detailed QA Report"
    ):

        st.json(
            qa_report
        )

    # ==========================================
    # CAMPAIGN CALENDAR
    # ==========================================

    st.header("📅 Campaign Calendar")

    calendar_generator = CampaignCalendar()

    calendar = calendar_generator.create_calendar(
        campaign.channels
    )

    for item in calendar:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write("📅 **Date**")

            st.write(
                item["date"]
            )

        with col2:

            st.write("📢 **Channel**")

            st.write(
                item["channel"]
            )

        with col3:

            st.write("📌 **Status**")

            st.write(
                item["status"]
            )

        st.divider()

    # ==========================================
    # FINAL PACKAGE
    # ==========================================

    st.header("📦 Final Campaign Package")

    if final_status == "PASS":

        st.write(
            "Your complete campaign package "
            "is ready for delivery."
        )

    else:

        st.warning(
            "Campaign has unresolved issues. "
            "Review the QA report before delivery."
        )

    if os.path.exists(zip_file):

        with open(
            zip_file,
            "rb"
        ) as file:

            zip_data = file.read()

        st.download_button(
            label="⬇️ Download BrandForge Campaign",
            data=zip_data,
            file_name="BrandForge_Campaign.zip",
            mime="application/zip",
            use_container_width=True
        )

        if final_status == "PASS":

            st.success(
                "Campaign package ready for delivery!"
            )

        else:

            st.warning(
                "Package generated, but QA requires review."
            )

    else:

        st.error(
            "Campaign ZIP could not be created."
        )