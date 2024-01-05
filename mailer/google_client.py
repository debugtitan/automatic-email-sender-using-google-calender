from googleapiclient.discovery import build
from mailer.config import AppConfig


service = build("calendar","v3",developerKey=A)
class GoogleCalenderClient:
    """ Google Calender Client """

    def __init__(self):
        