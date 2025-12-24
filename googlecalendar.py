import datetime
import os.path
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def create_event(service, event):
    event = service.events().insert(calendarId='primary', body=event()).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def print_events(service):
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    now_iso = now.isoformat()

    try:
        st.write("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
            calendarId="primary",
            timeMin = now_iso,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            st.write("No upcoming events found.")

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            st.write(start, event["summary"])

    except HttpError as error:
        st.write(f"An error occurred: {error}")