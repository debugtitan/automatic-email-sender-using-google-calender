import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mailer.config import BASE_DIR

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "secrets.json")
TOKEN_PICKLE_FILE = os.path.join(BASE_DIR, "token.pickle")

class GoogleCalendarClient:
    """ Google Calendar Client """

    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_credentials(self):
        if os.path.exists(TOKEN_PICKLE_FILE):
            with open(TOKEN_PICKLE_FILE, 'rb') as token:
                credentials = pickle.load(token)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
            with open(TOKEN_PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)

        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        return credentials

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()


