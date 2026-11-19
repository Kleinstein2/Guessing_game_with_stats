import streamlit as st
play = st.Page("play.py", title="Play")
stats = st.Page("stats.py", title="Stats")

st.navigation([play, stats], position="hidden").run()