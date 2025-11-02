import streamlit as st
import googlecalendar as gc
import datetime as dt

service = gc.authenticate()

# Call the Calendar API
now = dt.datetime.now(tz=dt.timezone.utc)
end = now + dt.timedelta(hours=1)

# front end
if st.button("Click to add an event"):
    gc.create_event(service, "Test", now, end)
    st.write("Event created!")
if st.button("Click to see past 10 events"):
    gc.print_events(service)
