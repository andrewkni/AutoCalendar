from event import Event
import streamlit as st
import googlecalendar as gc
import datetime as dt

# Saves list of tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []
tasks = st.session_state.tasks

# Connects to Google Calendar
service = gc.authenticate()

st.header("Welcome to AutoCalendar!")

start_date = st.date_input("Starting Date")
end_date = st.date_input("Ending Date")
start_hour = st.time_input("Starting hour")
end_hour = st.time_input("Ending hour")
break_time = st.number_input("Minutes between each task (break time)", step=1)


with st.form("add_event"):
    st.write("Add Event")
    name = st.text_input("Name of task")
    priority = st.selectbox(
        "Input priority:",
        (1, 2, 3, 4, 5)
    )
    duration = st.number_input("Duration of task in minutes", step=1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        tasks.append(Event(name, priority, duration))

with st.form("add_conflict"):
    st.write("Add Conflict")
    name = st.text_input("Name of task")

    init_time = st.time_input("Starting time")
    end_time = st.time_input("Ending time")

    submitted = st.form_submit_button("Submit")
    if submitted:
        tasks.append(Event(name, priority, duration))

st.subheader("Current Tasks:")
for event in tasks:
    st.write(event.print_event())


if st.button("Add to Google Calendar"):
    for event in tasks:
        gc.create_event(service, event)
