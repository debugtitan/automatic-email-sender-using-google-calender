import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from mailer.config import  BASE_DIR


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "secrets.json")

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=credentials)

class GoogleCalendarClient:
    """ Google Calendar Client """

    @staticmethod
    def get_calendar_list():
        return service.calendarList().list().execute()
