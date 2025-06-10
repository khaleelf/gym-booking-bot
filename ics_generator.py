from ics import Calendar, Event
from datetime import datetime, timedelta
import os

file_path='crossfit_calendar_events.ics'

def update_calendar(date):

    # Create a new calendar
    cal = Calendar()

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            cal = Calendar(f.read())

    # Create a new event
    event = Event()

    # Set event details
    event.name = "CrossFit Vastberaden"
    date_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
    event.begin = date_time  # Event start date and time
    event.end = date_time + timedelta(hours=1)  # Event end date and time
    event.location = "Veemkade 1288, 1019 CZ Amsterdam"

    # Add event to calendar
    cal.events.add(event)

    # Write the calendar to an .ics file
    with open(file_path, 'w') as f:
        f.writelines(cal.serialize_iter())
