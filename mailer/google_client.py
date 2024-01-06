import os
import pickle
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mailer.config import BASE_DIR
from mailer.email_client import EmailClient

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "secrets.json")
TOKEN_PICKLE_FILE = os.path.join(BASE_DIR, "token.pickle")


class GoogleCalendarClient:
    """Google Calendar Client"""

    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = build("calendar", "v3", credentials=self.credentials)

    def get_credentials(self):
        if os.path.exists(TOKEN_PICKLE_FILE):
            with open(TOKEN_PICKLE_FILE, "rb") as token:
                credentials = pickle.load(token)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            credentials = flow.run_local_server(port=0)
            with open(TOKEN_PICKLE_FILE, "wb") as token:
                pickle.dump(credentials, token)

        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        return credentials

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()["items"]

    def get_today_events(self):
        today = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=today,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        for event in events:
            subject = event.get("kind", "No subject")
            summary = event.get("summary", "No summary")
            organizer_email = event["organizer"].get("email", "No organizer email")
            event_link = event["htmlLink"]
            attendees = event.get("attendees", [])
            attendee_emails = [
                attendee["email"] for attendee in attendees if "email" in attendee
            ]
            helper = EmailClient(
                subject=subject,
                message=summary,
                to=organizer_email,
                bcc=attendee_emails,  #
                button_text="View Event",
                link=event_link,
            )
            helper._send_mail()

        return events
