import streamlit as st  # Navigation zwischen play und stats einfach 
st.set_page_config(layout="wide")
play = st.Page("play.py", title="Play")
stats = st.Page("stats.py", title="Stats")

st.navigation([play, stats], position="hidden").run()