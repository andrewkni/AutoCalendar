import streamlit as st
import googlecalendar as gc

# front end
if st.button("Click to see past 10 events"):
    gc.main()