import streamlit as st
import pandas as pd

st.title("Stats")

games = st.session_state.get("games", []) #gespeicherte spiele aus play.py holen

# noch keine Spiele -> Hinweis statt Absturz
if not games:
    st.info("No games played yet. Go to Play and start a game!")
    st.stop()

df = pd.DataFrame(games) #spiele als tabelle 
df.index = df.index + 1                  # Spiele ab 1 zählen statt ab 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Games Played", len(df))
col2.metric("Avg Questions", round(df["questions"].mean(), 1))
col3.metric("Total Time Played", f"{df['seconds'].sum()} s")
col4.metric("Winrate", f"{df['won'].mean() * 100:.0f} %") #won ist true/false, der mean gibt die gewinnquote in % aus

st.subheader("Questions per Game")
st.bar_chart(df["questions"]) #fragen pro spiel als balkendiagramm

st.subheader("All Games")
st.dataframe(df)

# beste und schlechteste Frage
history = pd.DataFrame(st.session_state.get("question_history", []))
if not history.empty:
    history["ruled out"] = history["before"] - history["after"]     # ausgeschlossene Figuren pro Frage
    best = history.loc[history["ruled out"].idxmax()] #beste frage = die, die die meisten figuren ausschließt
    worst = history.loc[history["ruled out"].idxmin()] #schlechteste frage = die, die die wenigsten figuren ausschließt
    st.success(f"Best question: {best['question']} ({best['ruled out']} ruled out)")
    st.warning(f"Worst question: {worst['question']} ({worst['ruled out']} ruled out)")

if st.button("Start Over"):
    for key in ["random_name", "lives", "Game_over", "guess_mode", "started", "questions", "time", "message", 
                "chat", "remaining", "question_log"]: #löscht spieldaten aus dem session state, damit man wieder von vorne anfangen kann
        st.session_state.pop(key, None)
    st.switch_page("play.py") #zurück zur play.py Seite also neues spiel

