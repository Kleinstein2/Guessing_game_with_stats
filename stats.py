import streamlit as st
import pandas as pd

st.title("Stats")

games = st.session_state.get("games", []) # Gespeicherte Spiele aus play.py holen

# Noch keine Spiele -> Hinweis statt Absturz
if not games:
    st.info("No games played yet. Go to Play and start a game!")
    st.stop()

df = pd.DataFrame(games) # Spiele als Tabelle
df.index = df.index + 1                  # Spiele ab 1 zählen statt ab 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Games Played", len(df))
col2.metric("Avg Questions", round(df["questions"].mean(), 1))
col3.metric("Total Time Played", f"{df['seconds'].sum()} s")
col4.metric("Winrate", f"{df['won'].mean() * 100:.0f} %") # won ist true/false, der mean gibt die Gewinnquote in % aus

st.subheader("Questions per Game")
st.bar_chart(df["questions"]) # Fragen pro Spiel als Balkendiagramm

st.subheader("All Games")
st.dataframe(df.sort_values(["lives_lost","seconds"])) # Leben über Zeit

# Beste und schlechteste Frage
history = pd.DataFrame(st.session_state.get("question_history", []))
if not history.empty:
    history["ruled out"] = history["before"] - history["after"]     # Ausgeschlossene Figuren pro Frage
    best = history.loc[history["ruled out"].idxmax()] # Beste Frage = die, die die meisten Figuren ausschließt
    worst = history.loc[history["ruled out"].idxmin()] # Schlechteste frage = die, die die wenigsten Figuren ausschließt
    st.success(f"Best question: {best['question']} ({best['ruled out']} ruled out)")
    st.warning(f"Worst question: {worst['question']} ({worst['ruled out']} ruled out)")
if st.button("Start Over"):
    for key in ["random_name", "lives", "Game_over", "guess_mode", "started", "questions", "time", "message", 
                "chat", "remaining", "question_log"]: # Löscht Spieldaten aus dem session state, damit man wieder von vorne anfangen kann
        st.session_state.pop(key, None)
    st.switch_page("play.py") # Zurück zur play.py Seite also neues Spiel

