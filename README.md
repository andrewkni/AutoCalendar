# AutoCalendar

AutoCalendar is a desktop-based Python application that converts a prioritized to-do list into scheduled Google Calendar events.  
It runs locally using a Streamlit interface and connects to Google Calendar through the Google Calendar API (OAuth 2.0 Desktop App flow).

---

## Features

- Desktop / local application
- Streamlit-based user interface
- Priority-based task scheduling
- Automatic break insertion between tasks
- Dynamic break-time reduction if tasks do not fit
- Conflict-aware scheduling (including daily recurring conflicts)
- Direct Google Calendar integration via API

---

## Tech Stack

- Python 3.10+
- Streamlit
- Google Calendar API
- Google OAuth 2.0 (Desktop Application)
- google-api-python-client
- google-auth

---

## User Inputs

### Scheduling Parameters
- Starting date
- Ending date
- Starting time
- Ending time
- Minutes between tasks (break time)

### Task Parameters
- Task name
- Task priority (higher number = higher priority)
- Task duration (hh:mm)

### Conflict Parameters
- Conflict name
- Conflict date
- Conflict start time
- Conflict duration (hh:mm)
- Optional daily recurrence

## Google Calendar API

AutoCalendar uses the **Google Calendar API** with **OAuth 2.0 for Desktop Applications**.

## Installation

Clone the repository:
```bash
git clone https://github.com/andrewkni/AutoCalendar.git
cd AutoCalendar
```
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Google API Setup

1. Go to Google Cloud Console  
   https://console.cloud.google.com/

2. Create a new project (or select an existing one)

3. Enable the Google Calendar API  
   - Navigate to APIs & Services → Library  
   - Search for "Google Calendar API"  
   - Click Enable  

4. Create OAuth credentials  
   - Go to APIs & Services → Credentials  
   - Click Create Credentials → OAuth client ID  
   - Application type: Desktop App  
   - Name: AutoCalendar (or any name)

5. Download the OAuth credentials file

6. Rename the downloaded file to:
   credentials.json

7. Place credentials.json in the project root directory

## Running the App
```bash
streamlit run app.py
```
The app runs locally and opens in your browser.

## Contributors

Andrew Ni & Aidan Haya
12/24/2025
