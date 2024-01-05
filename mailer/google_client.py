from googleapiclient.discovery import build
from mailer.config import AppConfig


service = build("calendar","v3",developerKey=AppConfig.google_api_key)
class GoogleCalenderClient:
    """ Google Calender Client """

    def __init__(self):
        