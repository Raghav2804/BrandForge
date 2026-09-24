from datetime import datetime, timedelta


class CampaignCalendar:

    def create_calendar(self, channels):

        calendar = []

        start_date = datetime.now()

        for i, channel in enumerate(channels):

            post_date = start_date + timedelta(
                days=i
            )

            calendar.append({
                "date": post_date.strftime(
                    "%Y-%m-%d"
                ),
                "channel": channel,
                "content": f"Campaign content for {channel}",
                "status": "Scheduled"
            })

        return calendar