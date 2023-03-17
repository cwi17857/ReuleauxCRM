import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the service account credentials and calendar ID
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'primary'

# Authenticate and authorize the service account
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Calendar API client
service = build('calendar', 'v3', credentials=creds)

# Create a start and end time for the event
start_time = datetime.datetime(2023, 3, 13, 9, 0, 0, tzinfo=pytz.UTC)
end_time = datetime.datetime(2023, 3, 13, 10, 0, 0, tzinfo=pytz.UTC)

# Create the event
event = {
    'summary': 'Meeting with John',
    'location': 'Room 101',
    'description': 'Discuss project progress',
    'start': {
        'dateTime': start_time.isoformat(),
        'timeZone': 'UTC',
    },
    'end': {
        'dateTime': end_time.isoformat(),
        'timeZone': 'UTC',
    },
}

# Send the request to the API to create the event
created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

print(f"Event created: {created_event.get('htmlLink')}")
