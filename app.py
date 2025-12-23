from event import Event
import streamlit as st
import googlecalendar as gc
import datetime as dt

# Saves list of tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []
tasks = st.session_state.tasks

# Saves list of conflicts
if "conflicts" not in st.session_state:
    st.session_state.conflicts = []
conflicts = st.session_state.conflicts

# Connects to Google Calendar
service = gc.authenticate()

st.header("Welcome to AutoCalendar!")

start_date = st.date_input("Starting Date")
end_date = st.date_input("Ending Date")
start_hour = st.time_input("Starting hour")
end_hour = st.time_input("Ending hour")
break_time = st.number_input("Minutes between each task (break time)", step=1)

start_dt = dt.datetime.combine(start_date, start_hour)
end_dt = dt.datetime.combine(end_date, end_hour)

with st.form("add_event"):
    st.write("Add Event")
    name = st.text_input("Name of task")
    priority = st.selectbox(
        "Input priority:",
        (1, 2, 3, 4, 5)
    )
    duration = st.time_input("Duration of task")

    submitted = st.form_submit_button("Submit")
    if submitted:
        tasks.append(Event(name, priority, duration, fixed=False))

with st.form("add_conflict"):
    st.write("Add Conflict")
    name = st.text_input("Name of task")

    conflict_date = st.date_input("Start date")
    everyday = st.checkbox("Is every day?")
    init_time = st.time_input("Starting time")
    duration = st.time_input("Duration of conflict")

    event_start_dt = dt.datetime.combine(conflict_date, init_time)
    event_end_dt = event_start_dt + dt.timedelta(hours=duration.hour, minutes=duration.minute)

    submitted = st.form_submit_button("Submit")
    if submitted:
        if (event_start_dt >= start_dt) and (event_end_dt <= end_dt):
            conflicts.append(Event(name, date=conflict_date, start=init_time, end=event_end_dt.time(), fixed=True))
        elif event_start_dt < start_dt:
            st.write("Start time is before specified time range")
        else:
            st.write("End time is after specified time range")

# Allows to remove tasks by clicking on their button
st.subheader("Current Tasks (click to remove):")
for i, event in enumerate(tasks):
    if st.button(f"Task #{i+1} : {event.print_event()}", key=f"task_{i}"):
        tasks.pop(i)
        st.rerun()

# Allows to remove conflicts by clicking on their button
st.subheader("Current Conflicts (click to remove):")
for i, event in enumerate(conflicts):
    if st.button(f"Conflict #{i+1} : {event.print_event()}", key=f"conflict_{i}"):
        conflicts.pop(i)
        st.rerun()


if st.button("Add to Google Calendar"):
    for event in tasks:
        gc.create_event(service, event)