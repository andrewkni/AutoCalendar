import streamlit as st
import googlecalendar as gc

if st.button("Click to see past 10 events"):
    gc.main()