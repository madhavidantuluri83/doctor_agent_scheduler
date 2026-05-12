from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import datetime
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarTool:

    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):

        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)

    # ------------------------------------------
    # LIST EVENTS
    # ------------------------------------------

    def list_upcoming_events(self, max_results=10):

        now = datetime.datetime.utcnow().isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        return events

    # ------------------------------------------
    # CHECK AVAILABILITY
    # ------------------------------------------

    def check_availability(self, start_time, end_time):

    # Fetch events around requested slot

        search_start = start_time - datetime.timedelta(days=1)

        search_end = end_time + datetime.timedelta(days=1)

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=search_start.isoformat() + 'Z',
            timeMax=search_end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        # ------------------------------------------
        # CHECK OVERLAPS
        # ------------------------------------------

        for event in events:

            start_str = event['start'].get('dateTime')

            end_str = event['end'].get('dateTime')

            # Skip all-day events
            if not start_str or not end_str:
                continue

            event_start = datetime.datetime.fromisoformat(
                start_str.replace('Z', '+00:00')
            ).replace(tzinfo=None)

            event_end = datetime.datetime.fromisoformat(
                end_str.replace('Z', '+00:00')
            ).replace(tzinfo=None)

            # OVERLAP DETECTION
            if start_time < event_end and end_time > event_start:

                return False

        return True

    # ------------------------------------------
    # CREATE EVENT
    # ------------------------------------------

    def create_event(
        self,
        summary,
        start_time,
        end_time
    ):

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
        }

        created_event = self.service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        return created_event

# -------------------------------------------------
# TESTING
# -------------------------------------------------

if __name__ == "__main__":

    tool = GoogleCalendarTool()

    print("\nUpcoming Events:\n")

    events = tool.list_upcoming_events()

    if not events:
        print("No upcoming events found.")

    for event in events:

        start = event['start'].get(
            'dateTime',
            event['start'].get('date')
        )

        print(start, event['summary'])