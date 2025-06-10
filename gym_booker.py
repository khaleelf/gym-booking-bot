#!/usr/bin/python3

import requests
import json
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LOGIN_URL = "https://gotgrib.nl/auth/apiMemberLogin"
ACTIVITIES_URL = "https://gotgrib.nl/memberApi/activitiesWeek?date="
RESERVATION_URL = "https://gotgrib.nl//memberApi/makeReservation"

def get_user_token(email, password):
    """Get authentication token for user"""
    login_data = json.dumps({
        "email": email,
        "password": password
    })
    login_header = {
        'Host': 'gotgrib.nl',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(url=LOGIN_URL, headers=login_header, data=login_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        content = response.json()
        return content["data"]["member"][0]["usersToken"]
    except requests.RequestException as e:
        print(f"Unable to get user token: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Unexpected response format: {e}")
        return None

def get_booking_date():
    """Get date for booking (7 days from now)"""
    return (datetime.datetime.now().date() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

def get_activity_id(headers, booking_date):
    """Get activity ID for preferred time slots"""
    url_activities = ACTIVITIES_URL + booking_date
    
    try:
        response = requests.get(url=url_activities, headers=headers)
        response.raise_for_status()
        activities_data = response.json()
        
        start_times = ['18:30', '18:00', '10:00', '10:30']
        
        for activity in activities_data["data"]["activities"][0]["activities"][::-1]:
            for time in start_times:
                if activity["start_time"] == time:
                    return activity["id"], time
                    
        print("No suitable time slots found")
        return None, None
        
    except requests.RequestException as e:
        print(f"Unable to get activity: {e}")
        return None, None
    except (KeyError, IndexError) as e:
        print(f"Unexpected response format: {e}")
        return None, None

def book_activity(headers, activity_id, date):
    """Make reservation for activity"""
    data = json.dumps({
        "activities_details_id": activity_id,
        "date": date,
        "repeatReservation": False,
        "repeatWeeks": 0,
        "sendICS": False,
        "language": "nl"
    })
    
    try:
        response = requests.post(url=RESERVATION_URL, data=data, headers=headers)
        response.raise_for_status()
        print(f"Successfully booked activity for {date}")
        return True
    except requests.RequestException as e:
        print(f"Unable to book activity: {e}")
        return False

def book_class(date=None):
    """Main booking function"""
    if date is None:
        date = get_booking_date()
    
    # Get credentials from environment
    email1 = os.getenv('GYM_EMAIL_1')
    password1 = os.getenv('GYM_PASSWORD_1')
    email2 = os.getenv('GYM_EMAIL_2')  
    password2 = os.getenv('GYM_PASSWORD_2')
    
    # Get tokens for both users
    token1 = get_user_token(email1, password1)
    token2 = get_user_token(email2, password2)
        
    headers1 = {
        'Content-Type': 'application/json',
        'Grib-Token': token1,
    }

    headers2 = {
        'Content-Type': 'application/json',
        'Grib-Token': token2,
    }
    
    # Get activity details
    activity_id, time = get_activity_id(headers1, date)
    if not activity_id:
        print("No activity found to book")
        return None
    
    # Book for first user
    book_activity(headers1, activity_id, date)
    book_activity(headers2, activity_id, date)
    
    return f"{date} {time}"
