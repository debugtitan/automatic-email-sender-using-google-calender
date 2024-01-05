from googleapiclient.discovery import build
from mailer.config import AppConfig


service = build("calendar","v3",developerKey=AppConfig.google_api_key)

class GoogleCalenderClient:
    """ Google Calender Client """

    @staticmethod
    def get_calender_list():
        return service.calendarList().list(pageToken=None).execute()

        