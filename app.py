from event import Event
import streamlit as st
import googlecalendar as gc
import datetime as dt
from time_range import TimeRange

# Algorithm to compute a schedule for given tasks, conflicts, start time, end time for each day
# Returns a list of all event items to be imported into Google Calendar
def schedule(tasks, conflicts, start_date, end_date, start_time, end_time):
    events = []  # final array of all Events
    # Sort conflicts by time (earliest conflict is first)
    conflicts.sort(key=lambda event: event.start)

    # Sort tasks by priority (highest priority is first)
    tasks.sort(key=lambda event: event.priority)

    time_range_list = []  # array of time_range objects

    num_days = (end_date - start_date).days

    start_dt = dt.datetime.combine(start_date, start_time)

    break_points = len(conflicts) + num_days + 1
    current_day = start_date

    conflict_count = 0

    for i in range(break_points):
        if (len(conflicts) > conflict_count) and (
                conflicts[conflict_count].get_start_dt() <= dt.datetime.combine(current_day, end_time)):
            time_range_list.append(TimeRange(start_dt, conflicts[conflict_count].get_start_dt()))
            start_dt = conflicts[conflict_count].get_end_dt()
            conflict_count += 1
        else:
            time_range_list.append(TimeRange(start_dt, dt.datetime.combine(current_day, end_time)))
            current_day += dt.timedelta(days=1)
            start_dt = dt.datetime.combine(current_day, start_time)

    for time_range in time_range_list:
        time_range.print_time_range()

    return events


def main():
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

    st.subheader("Input starting parameters")

    start_date = st.date_input("Starting Date")
    end_date = st.date_input("Ending Date")

    # Error checking for date
    if end_date < start_date:
        st.error("End date cannot be earlier than start date")

    start_time = st.time_input("Starting time")
    end_time = st.time_input("Ending time")

    # Error checking for time
    if end_time < start_time:
        st.error("End time cannot be earlier than start time")

    break_time = st.number_input("Minutes between each task (break time)", step=1, min_value=0)
    if break_time >= 60:
        st.write("Hidden Sid achievement unlocked")

    start_dt = dt.datetime.combine(start_date, start_time)
    end_dt = dt.datetime.combine(end_date, end_time)

    st.divider()
    st.subheader("Input to-do list and any scheduled conflicts")

    col1, col2 = st.columns(2, gap='large')

    with col1:
        with st.form("add_event"):
            st.write("Add Task")
            name = st.text_input("Name of task")
            priority = st.selectbox(
                "Task priority:",
                (1, 2, 3, 4, 5)
            )
            # default duration is 0
            duration = st.time_input("Duration of task (hh:mm)", value=dt.time(0, 0))

            submitted = st.form_submit_button("Submit")
            if submitted:
                tasks.append(Event(name, priority=priority, duration=duration, fixed=False))

    with col2:
        with st.form("add_conflict"):
            st.write("Add Conflict")
            name = st.text_input("Name of conflict")

            conflict_date = st.date_input("Start date")
            everyday = st.checkbox("Recurs every day?")
            init_time = st.time_input("Starting time")
            # default duration is 0
            duration = st.time_input("Duration of conflict (hh:mm)", value=dt.time(0, 0))

            event_start_dt = dt.datetime.combine(conflict_date, init_time)
            event_end_dt = event_start_dt + dt.timedelta(hours=duration.hour, minutes=duration.minute)

            submitted = st.form_submit_button("Submit")
            if submitted:
                if (event_start_dt >= start_dt) and (event_end_dt <= end_dt):
                    if not everyday:
                        conflicts.append(
                            Event(name, everyday, start=event_start_dt, end=event_end_dt, fixed=True))
                    else:
                        num_days = (end_dt - start_dt).days
                        for i in range(num_days + 1):
                            if ((i != 0) or (event_start_dt.time() >= start_time)) and (
                                    (i != num_days) or (event_end_dt.time() <= end_time)):
                                conflicts.append(
                                    Event(name, everyday, start=event_start_dt + dt.timedelta(days=i), end=event_end_dt
                                         + dt.timedelta(days=i, hours=duration.hour, minutes=duration.minute), fixed=True))
                elif event_start_dt < start_dt:
                    st.write("Start time is before specified time range")
                else:
                    st.write("End time is after specified time range")

    col1, col2 = st.columns(2, gap='large')

    with col1:
        # Allows to remove tasks by clicking on their button
        st.subheader("Current Tasks (click to remove):")
        for i, event in enumerate(tasks):
            if st.button(f"Task #{i + 1}: {event.print_event()}", key=f"task_{i}"):
                tasks.pop(i)
                st.rerun()

    with col2:
        # Allows to remove conflicts by clicking on their button
        st.subheader("Current Conflicts (click to remove):")
        for i, event in enumerate(conflicts):
            if st.button(f"Conflict #{i + 1}: {event.print_event()}", key=f"conflict_{i}"):
                conflicts.pop(i)
                st.rerun()

    st.divider()

    st.subheader("Generate your calendar!")
    st.write("\n")

    # Import to Google Calendar
    if st.button("Add to Google Calendar", type='primary'):
        events = schedule(tasks, conflicts, start_date, end_date, start_time, end_time)
        st.toast("Event added to Google Calendar!", icon='📅')

        #for event in events:
           #gc.create_event(service, event)

if __name__ == "__main__":
    main()