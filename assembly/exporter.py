import os
import json
import shutil

from assembly.calendar import CampaignCalendar


class CampaignExporter:

    def export(
        self,
        campaign,
        strategy,
        copy,
        images,
        qa_report
    ):

        folder = "outputs/BrandForge_Campaign"

        os.makedirs(
            folder,
            exist_ok=True
        )

        os.makedirs(
            f"{folder}/content",
            exist_ok=True
        )

        os.makedirs(
            f"{folder}/images",
            exist_ok=True
        )

        # --------------------------------
        # Strategy
        # --------------------------------

        with open(
            f"{folder}/strategy.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                strategy,
                file,
                indent=4
            )

        # --------------------------------
        # Instagram
        # --------------------------------

        with open(
            f"{folder}/content/instagram.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                copy["instagram"]["caption"]
            )

            file.write(
                "\n\nCTA: "
            )

            file.write(
                copy["instagram"]["cta"]
            )

            file.write(
                "\n\n"
            )

            file.write(
                " ".join(
                    copy["instagram"]["hashtags"]
                )
            )

        # --------------------------------
        # LinkedIn
        # --------------------------------

        with open(
            f"{folder}/content/linkedin.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                copy["linkedin"]["post"]
            )

            file.write(
                "\n\nCTA: "
            )

            file.write(
                copy["linkedin"]["cta"]
            )

            file.write(
                "\n\n"
            )

            file.write(
                " ".join(
                    copy["linkedin"]["hashtags"]
                )
            )

        # --------------------------------
        # Email
        # --------------------------------

        with open(
            f"{folder}/content/email.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"Subject: "
                f"{copy['email']['subject']}\n\n"
            )

            file.write(
                f"Preview: "
                f"{copy['email']['preview']}\n\n"
            )

            file.write(
                copy["email"]["body"]
            )

            file.write(
                f"\n\nCTA: "
                f"{copy['email']['cta']}"
            )

        # --------------------------------
        # Images
        # --------------------------------

        for image in images:

            source = image["file"]

            destination = (
                f"{folder}/images/"
                + os.path.basename(source)
            )

            if os.path.exists(source):

                shutil.copy2(
                    source,
                    destination
                )

        # --------------------------------
        # QA Report
        # --------------------------------

        with open(
            f"{folder}/qa_report.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                qa_report,
                file,
                indent=4
            )

        # --------------------------------
        # Campaign Summary
        # --------------------------------

        summary = {
            "product": campaign.product,
            "audience": campaign.audience,
            "goal": campaign.goal,
            "key_message": campaign.key_message,
            "channels": campaign.channels,
            "qa_status": qa_report["overall_status"]
        }

        with open(
            f"{folder}/campaign_summary.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary,
                file,
                indent=4
            )

        # --------------------------------
        # Campaign Calendar
        # --------------------------------

        calendar_generator = CampaignCalendar()

        calendar = calendar_generator.create_calendar(
            campaign.channels
        )

        with open(
            f"{folder}/campaign_calendar.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                calendar,
                file,
                indent=4
            )

        # --------------------------------
        # ZIP Package
        # --------------------------------

        zip_file = shutil.make_archive(
            "outputs/BrandForge_Campaign",
            "zip",
            folder
        )

        return zip_file