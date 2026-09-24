import streamlit as st
import json
import base64
from pathlib import Path
import streamlit.components.v1 as components

from models.campaign import Campaign
from orchestrator.workflow import BrandForgeWorkflow


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BrandForge",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
BRAND_FILE = BASE_DIR / "config" / "brand_kit.json"


# ============================================================
# SIMPLE CSS
# ============================================================

st.markdown("""
<style>
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.brand-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: #173b2a;
    margin-bottom: 0;
}

.brand-sub {
    color: #718078;
    margin-top: -5px;
}

.hero {
    background: linear-gradient(135deg,#173b2a,#285b40);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin: 20px 0;
}

.hero-small {
    color:#b8dfc4;
    font-size:.75rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:1px;
}

.hero-title {
    font-size:2rem;
    font-weight:800;
    margin:8px 0;
}

.hero-sub {
    color:#dcebe0;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

def load_brand():

    with open(
        BRAND_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def resolve_image_path(value):

    if not value:
        return None

    path = Path(str(value))

    if path.exists():
        return path

    if not path.is_absolute():

        candidate = BASE_DIR / path

        if candidate.exists():
            return candidate

    return None


def show_svg(path):

    try:

        data = base64.b64encode(
            path.read_bytes()
        ).decode("utf-8")

        html = f"""
        <div style="
            background:white;
            border-radius:14px;
            overflow:hidden;
            border:1px solid #e4eae5;
        ">
            <img
                src="data:image/svg+xml;base64,{data}"
                style="width:100%;display:block;"
            >
        </div>
        """

        components.html(
            html,
            height=500,
            scrolling=False
        )

        return True

    except Exception:

        return False


def show_issues(result):

    issues = result.get("issues", [])

    if not issues:

        st.caption("No issues detected.")
        return

    for issue in issues:
        st.warning(issue)


# ============================================================
# LOAD BRAND
# ============================================================

brand = load_brand()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<div class='brand-title'>BrandForge</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='brand-sub'>Create. Validate. Launch.</div>",
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# CAMPAIGN BRIEF
# ============================================================

st.subheader("Campaign Brief")

st.caption(
    "Give BrandForge one brief and let the agents build the campaign."
)

col1, col2 = st.columns(2)


with col1:

    product = st.text_input(
        "Product / Service",
        value="SmartGlow Smart LED Desk Lamp",
        placeholder="e.g. Productivity App"
    )

    audience = st.text_input(
        "Target Audience",
        value="College students and young professionals",
        placeholder="e.g. Young Professionals"
    )

    goal = st.text_input(
        "Campaign Goal",
        value="Increase product awareness and online sales",
        placeholder="e.g. Product Launch"
    )


with col2:

    key_message = st.text_area(
        "Key Message",
        value="Light smarter. Focus better.",
        height=120,
        placeholder="What should the audience remember?"
    )

    channels = st.multiselect(
        "Marketing Channels",
        ["instagram", "linkedin", "email"],
        default=["instagram", "linkedin", "email"]
    )


run_col, test_col = st.columns([3, 1])


with run_col:

    generate_campaign = st.button(
        "🚀 Generate Campaign",
        type="primary",
        use_container_width=True
    )


with test_col:

    test_guardrails = st.button(
        "🛡 Test Guardrails",
        use_container_width=True
    )


# ============================================================
# GUARDRAIL TEST
# ============================================================

if test_guardrails:

    if not channels:

        st.warning(
            "Select at least one channel first."
        )

    else:

        workflow = BrandForgeWorkflow(brand)

        forbidden = brand["dont_say"][0]

        test_campaign = Campaign(
            product=product,
            audience=audience,
            goal=goal,
            key_message=key_message,
            channels=channels
        )

        test_copy = {
            "instagram": {
                "caption": (
                    f"This product is {forbidden} "
                    "and perfect for everyone."
                ),
                "cta": "Learn more",
                "hashtags": []
            },

            "linkedin": {
                "post": (
                    f"Our product is {forbidden} "
                    "and designed for modern users."
                ),
                "cta": "Discover more",
                "hashtags": []
            },

            "email": {
                "subject": f"A {forbidden} solution",
                "preview": "Discover something new.",
                "body": (
                    f"Our product offers a {forbidden} "
                    "experience for everyday users."
                ),
                "cta": "Learn more"
            }
        }

        st.subheader("Guardrail Test")

        st.info(
            f"Testing forbidden term: {forbidden}"
        )

        initial = workflow.qa_engine.check_campaign(
            test_copy,
            test_campaign,
            []
        )

        st.write(
            "Initial validation: "
            f"**{initial.get('overall_status', 'UNKNOWN')}**"
        )

        if initial.get("overall_status") == "FAIL":

            for name, check in initial.get(
                "checks",
                {}
            ).items():

                if (
                    isinstance(check, dict)
                    and check.get("status") == "FAIL"
                ):

                    st.write(
                        f"**{name.title()}**"
                    )

                    show_issues(check)

            revised = workflow.copy_agent.revise_copy(
                test_campaign,
                brand,
                {},
                test_copy,
                initial
            )

            final = workflow.qa_engine.check_campaign(
                revised,
                test_campaign,
                []
            )

            st.write(
                "Final validation: "
                f"**{final.get('overall_status', 'UNKNOWN')}**"
            )

            if final.get("overall_status") == "PASS":

                st.success(
                    "Guardrail detected the violation "
                    "and the Copywriting Agent fixed it."
                )

            else:

                st.warning(
                    "Campaign still requires human review."
                )


# ============================================================
# GENERATE CAMPAIGN
# ============================================================

if generate_campaign:

    errors = []

    if not product.strip():
        errors.append(
            "Product / Service is required."
        )

    if not audience.strip():
        errors.append(
            "Target Audience is required."
        )

    if not goal.strip():
        errors.append(
            "Campaign Goal is required."
        )

    if not key_message.strip():
        errors.append(
            "Key Message is required."
        )

    if not channels:
        errors.append(
            "Select at least one channel."
        )

    if errors:

        for error in errors:
            st.error(error)

    else:

        campaign = Campaign(
            product,
            audience,
            goal,
            key_message,
            channels
        )

        workflow = BrandForgeWorkflow(brand)

        with st.status(
            "Building your campaign...",
            expanded=True
        ) as status:

            st.write(
                "🧠 Creating marketing strategy..."
            )

            result = workflow.run(campaign)

            status.update(
                label="Campaign generation complete",
                state="complete",
                expanded=False
            )

        st.session_state[
            "campaign_result"
        ] = result


# ============================================================
# RESULTS
# ============================================================

if "campaign_result" in st.session_state:

    result = st.session_state[
        "campaign_result"
    ]

    campaign = result["campaign"]
    strategy = result["strategy"]
    copy = result["copy"]
    images = result.get("images", [])
    qa_report = result["qa_report"]

    theme = strategy.get(
        "campaign_theme",
        "Campaign Strategy"
    )

    qa_status = qa_report.get(
        "overall_status",
        "UNKNOWN"
    )

    # --------------------------------
    # Hero
    # --------------------------------

    st.markdown(
        "<div class='hero'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='hero-small'>Campaign Results</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='hero-title'>{campaign.product}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='hero-sub'>{theme}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------
    # Metrics
    # --------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Strategy", "✓")

    with m2:
        st.metric(
            "Channels",
            len(campaign.channels)
        )

    with m3:
        st.metric(
            "Visual Variants",
            len(images)
        )

    with m4:
        st.metric(
            "Brand QA",
            qa_status
        )

    # --------------------------------
    # Strategy
    # --------------------------------

    st.subheader("🎯 Marketing Strategy")

    st.caption(
        "Generated by the Strategy Agent."
    )

    st.markdown("**Campaign Theme**")

    st.info(theme)

    messages = strategy.get(
        "key_messages",
        []
    )

    if messages:

        st.markdown("**Key Messages**")

        for i, message in enumerate(
            messages,
            1
        ):

            st.write(
                f"**{i:02d}**  {message}"
            )

    channel_strategy = strategy.get(
        "channel_strategy",
        {}
    )

    if channel_strategy:

        st.markdown(
            "**Channel Strategy**"
        )

        cols = st.columns(
            min(3, len(channel_strategy))
        )

        for i, (channel, data) in enumerate(
            channel_strategy.items()
        ):

            with cols[i % len(cols)]:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {channel.title()}"
                    )

                    st.caption("Content")

                    for item in data.get(
                        "content_types",
                        []
                    ):

                        st.write(
                            f"• {item}"
                        )

                    st.caption("Purpose")

                    st.write(
                        data.get(
                            "purpose",
                            ""
                        )
                    )

                    st.caption("Cadence")

                    st.write(
                        data.get(
                            "cadence",
                            ""
                        )
                    )

    # --------------------------------
    # Copy
    # --------------------------------

    st.subheader(
        "✍️ Campaign Content"
    )

    st.caption(
        "Channel-ready content generated by "
        "the Copywriting Agent."
    )

    available = [
        c for c in campaign.channels
        if c in copy
    ]

    if available:

        tabs = st.tabs(
            [
                c.title()
                for c in available
            ]
        )

        for tab, channel in zip(
            tabs,
            available
        ):

            with tab:

                data = copy[channel]

                if channel == "instagram":

                    st.markdown(
                        "**Caption**"
                    )

                    st.write(
                        data.get(
                            "caption",
                            ""
                        )
                    )

                    st.markdown(
                        "**Call to Action**"
                    )

                    st.info(
                        data.get(
                            "cta",
                            ""
                        )
                    )

                    st.markdown(
                        "**Hashtags**"
                    )

                    st.write(
                        " ".join(
                            data.get(
                                "hashtags",
                                []
                            )
                        )
                    )

                    st.caption(
                        f"Characters: "
                        f"{len(data.get('caption', ''))}"
                    )

                elif channel == "linkedin":

                    st.markdown(
                        "**Post**"
                    )

                    st.write(
                        data.get(
                            "post",
                            ""
                        )
                    )

                    st.markdown(
                        "**Call to Action**"
                    )

                    st.info(
                        data.get(
                            "cta",
                            ""
                        )
                    )

                    st.markdown(
                        "**Hashtags**"
                    )

                    st.write(
                        " ".join(
                            data.get(
                                "hashtags",
                                []
                            )
                        )
                    )

                    st.caption(
                        f"Characters: "
                        f"{len(data.get('post', ''))}"
                    )

                else:

                    st.markdown(
                        "**Subject**"
                    )

                    st.write(
                        data.get(
                            "subject",
                            ""
                        )
                    )

                    st.markdown(
                        "**Preview**"
                    )

                    st.write(
                        data.get(
                            "preview",
                            ""
                        )
                    )

                    st.markdown(
                        "**Body**"
                    )

                    st.write(
                        data.get(
                            "body",
                            ""
                        )
                    )

                    st.markdown(
                        "**Call to Action**"
                    )

                    st.info(
                        data.get(
                            "cta",
                            ""
                        )
                    )

    # --------------------------------
    # Visuals
    # --------------------------------

    st.subheader(
        "🎨 Visual Variants"
    )

    st.caption(
        "Two visual directions generated "
        "for the campaign."
    )

    if images:

        cols = st.columns(
            min(2, len(images))
        )

        for i, image in enumerate(images):

            with cols[i % len(cols)]:

                style = image.get(
                    "style",
                    "Visual"
                )

                raw_path = image.get(
                    "file"
                )

                path = resolve_image_path(
                    raw_path
                )

                st.markdown(
                    f"### {style.title()}"
                )

                if path:

                    if path.suffix.lower() == ".svg":

                        if show_svg(path):

                            st.success(
                                "Visual generated"
                            )

                        else:

                            st.error(
                                "Could not render SVG."
                            )

                    else:

                        st.image(
                            str(path),
                            use_container_width=True
                        )

                        st.success(
                            "Visual generated"
                        )

                else:

                    st.error(
                        f"Visual file not found: "
                        f"{raw_path}"
                    )

    else:

        st.warning(
            "No visual variants were returned "
            "by the Image Generation Agent."
        )

    # --------------------------------
    # QA
    # --------------------------------

    st.subheader(
        "🛡 Campaign War Room"
    )

    st.caption(
        "Final quality-control checks before "
        "campaign delivery."
    )

    if qa_status == "PASS":

        st.success(
            "✓ CAMPAIGN PASSED — "
            "All configured checks passed."
        )

    else:

        st.error(
            "⚠ REVIEW REQUIRED — "
            "One or more checks need attention."
        )

    checks = qa_report.get(
        "checks",
        {}
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        st.markdown(
            "### 🔤 Text Guard"
        )

        for channel in campaign.channels:

            if channel in checks:

                status = checks[
                    channel
                ].get(
                    "status",
                    "UNKNOWN"
                )

                if status == "PASS":

                    st.success(
                        f"{channel.title()}: PASS"
                    )

                else:

                    st.error(
                        f"{channel.title()}: FAIL"
                    )

                    show_issues(
                        checks[channel]
                    )

    with q2:

        st.markdown(
            "### 🔍 Consistency"
        )

        consistency = checks.get(
            "consistency",
            {}
        )

        if consistency.get(
            "status"
        ) == "PASS":

            st.success(
                "Cross-Channel Claims: PASS"
            )

        else:

            st.error(
                "Cross-Channel Claims: FAIL"
            )

            show_issues(
                consistency
            )

    with q3:

        st.markdown(
            "### 🎨 Image Guard"
        )

        image_checks = checks.get(
            "images",
            []
        )

        if image_checks:

            for check in image_checks:

                if check.get(
                    "status"
                ) == "PASS":

                    st.success(
                        f"{check.get('style', 'Visual').title()}: PASS"
                    )

                else:

                    st.error(
                        f"{check.get('style', 'Visual').title()}: FAIL"
                    )

                    show_issues(check)

        else:

            st.warning(
                "No image checks available."
            )

    st.info(
        f"Revision attempts: "
        f"{qa_report.get('revision_attempts', 0)}"
        f"  •  Final status: "
        f"{qa_report.get('final_status', qa_status)}"
    )

    # --------------------------------
    # Calendar
    # --------------------------------

    st.subheader(
        "📅 Campaign Calendar"
    )

    calendar = result.get(
        "calendar"
    )

    if calendar:

        cols = st.columns(
            min(3, len(calendar))
        )

        for i, item in enumerate(
            calendar
        ):

            with cols[i % len(cols)]:

                with st.container(
                    border=True
                ):

                    st.caption(
                        item.get(
                            "date",
                            ""
                        )
                    )

                    st.write(
                        item.get(
                            "channel",
                            ""
                        ).title()
                    )

                    st.caption(
                        item.get(
                            "status",
                            "Scheduled"
                        )
                    )

    else:

        st.info(
            "Campaign calendar is included "
            "in the exported package."
        )

    # --------------------------------
    # Delivery
    # --------------------------------

    st.subheader(
        "📦 Final Delivery"
    )

    zip_path = (
        BASE_DIR
        / "outputs"
        / "BrandForge_Campaign.zip"
    )

    if zip_path.exists():

        with open(
            zip_path,
            "rb"
        ) as f:

            st.download_button(
                "⬇ Download Campaign Package",
                data=f,
                file_name="BrandForge_Campaign.zip",
                mime="application/zip",
                use_container_width=True
            )

    else:

        st.warning(
            "Campaign ZIP file was not found."
        )

    # --------------------------------
    # Developer Details
    # --------------------------------

    with st.expander(
        "Developer Details"
    ):

        st.write(
            "Strategy JSON"
        )

        st.json(strategy)

        st.write(
            "Campaign Copy JSON"
        )

        st.json(copy)

        st.write(
            "QA Report JSON"
        )

        st.json(qa_report)