import streamlit as st
import pandas as pd

st.title("Stats")

games = st.session_state.get("games", [])

# noch keine Spiele -> Hinweis statt Absturz
if not games:
    st.info("No games played yet. Go to Play and start a game!")
    st.stop()

df = pd.DataFrame(games)
df.index = df.index + 1                  # Spiele ab 1 zählen statt ab 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Games Played", len(df))
col2.metric("Avg Questions", round(df["questions"].mean(), 1))
col3.metric("Total Time Played", f"{df['seconds'].sum()} s")
col4.metric("Winrate", f"{df['won'].mean() * 100:.0f} %")

st.subheader("Questions per Game")
st.bar_chart(df["questions"])

st.subheader("All Games")
st.dataframe(df)

if st.button("Start Over"):
    for key in ["random_name", "lives", "Game_over", "guess_mode", "started", "questions", "time", "message"]:
        st.session_state.pop(key, None)
    st.switch_page("play.py")

#best_question=
#worst_question=