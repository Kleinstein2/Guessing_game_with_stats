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

# # LLM: Fragequalität = wie viele Figuren eine Frage ausgeschlossen hat
# st.header("How good were your questions?")
# st.caption("A good question rules out many characters, a bad one none. 'left_at_guess' in the table above: 1 = you figured it out, many = you guessed.")
# history = pd.DataFrame(st.session_state.get("question_history", []))
# if not history.empty:
#     history["ruled out"] = history["before"] - history["after"]
#     st.metric("Avg characters ruled out per question", round(history["ruled out"].mean(), 1))
#     st.subheader("Characters left after each question (last game)")
#     last = history[history["game"] == history["game"].max()]
#     st.line_chart(last["after"].reset_index(drop=True))
#     st.dataframe(history, hide_index=True)


if st.button("Start Over"):
    for key in ["random_name", "lives", "Game_over", "guess_mode", "started", "questions", "time", "message"]:
#     # LLM: statt der Zeile darüber
#     for key in ["random_name", "lives", "Game_over", "guess_mode", "started", "questions", "time", "message",
#                 "chat", "remaining", "question_log"]:

        st.session_state.pop(key, None)
    st.switch_page("play.py")

#best_question=
#worst_question=