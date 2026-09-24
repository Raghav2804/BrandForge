from agents.strategy_agent import StrategyAgent
from agents.copy_agent import CopywritingAgent
from agents.image_agent import ImageGenerationAgent
from guardrails.qa_engine import QAEngine


class BrandForgeWorkflow:

    def __init__(self, brand):

        self.brand = brand

        self.strategy_agent = StrategyAgent()
        self.copy_agent = CopywritingAgent()
        self.image_agent = ImageGenerationAgent()
        self.qa_engine = QAEngine(brand)

        self.max_retries = 2

    def run(self, campaign):

        print("\nStarting BrandForge workflow...")

        # --------------------------------
        # STEP 1: Strategy
        # --------------------------------

        print("\n[1/5] Creating marketing strategy...")

        strategy = self.strategy_agent.create_strategy(
            campaign,
            self.brand
        )

        print("Strategy created.")

        # --------------------------------
        # STEP 2: Initial Copy
        # --------------------------------

        print("\n[2/5] Creating campaign copy...")

        copy = self.copy_agent.create_copy(
            campaign,
            self.brand,
            strategy
        )

        print("Copy created.")

        # --------------------------------
        # STEP 3: Images
        # --------------------------------

        print("\n[3/5] Creating campaign visuals...")

        images = self.image_agent.generate_images(
            campaign,
            self.brand
        )

        print("Visuals created.")

        # --------------------------------
        # STEP 4: Initial QA
        # --------------------------------

        print("\n[4/5] Running brand QA...")

        qa_report = self.qa_engine.check_campaign(
            copy,
            campaign,
            images
        )

        print(
            "Initial QA:",
            qa_report["overall_status"]
        )

        # --------------------------------
        # STEP 5: Revision Loop
        # --------------------------------

        retry_count = 0

        while (
            qa_report["overall_status"] == "FAIL"
            and retry_count < self.max_retries
        ):

            retry_count += 1

            print(
                f"\nRevision attempt "
                f"{retry_count}/{self.max_retries}..."
            )

            copy = self.copy_agent.revise_copy(
                campaign,
                self.brand,
                strategy,
                copy,
                qa_report
            )

            print("Copy revised.")

            # Run QA again
            qa_report = self.qa_engine.check_campaign(
                copy,
                campaign,
                images
            )

            print(
                f"QA after revision {retry_count}:",
                qa_report["overall_status"]
            )

        # --------------------------------
        # Final Status
        # --------------------------------

        if qa_report["overall_status"] == "PASS":

            final_status = "PASS"

            print("\nCampaign passed all QA checks.")

        else:

            final_status = "REVIEW_REQUIRED"

            print(
                "\nCampaign requires human review."
            )

        # --------------------------------
        # QA Metadata
        # --------------------------------

        qa_report["revision_attempts"] = retry_count
        qa_report["final_status"] = final_status

        # --------------------------------
        # Final Result
        # --------------------------------

        return {
            "campaign": campaign,
            "strategy": strategy,
            "copy": copy,
            "images": images,
            "qa_report": qa_report
        }