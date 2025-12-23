import streamlit as st
import googlecalendar as gc
import datetime as dt

service = gc.authenticate()
# Call the Calendar API
now = dt.datetime.now(tz=dt.timezone.utc)
end = now + dt.timedelta(hours=1)

st.write("Welcome to AutoCalendar!")

st.write(st.text_input("Add to do item"))

with st.form("todolist"):
    st.write("To Do List")
    item = st.text_input("Form slider")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", item)



# front end
if st.button("Click to add event"):
    gc.create_event(service, "Test", now, end)
    st.write("Event created!")
if st.button("Click to see past 10 events"):
    gc.print_events(service)
