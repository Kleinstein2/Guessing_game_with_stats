import streamlit as st
import random

names = ["Niklas", "Leonard", "Jann", "Phillip", "Erik", "Malte"] #Personen Liste                              # Random auswahl
Max_Live = 3

#Game state
st.session_state.setdefault("random_name", random.choice(names))  # alle Konstanten
st.session_state.setdefault("lives", Max_Live)
st.session_state.setdefault("guesser", True)
st.session_state.setdefault("Game_over", False)
st.session_state.setdefault("stats_page", False)
st.session_state.setdefault("guess_mode", False) 
st.session_state.setdefault("message", "Welcome to the Guessing Game! You have 3 lives. Try to guess the name.")

#Funktionen
def guess():
    st.session_state["guess_mode"] = not st.session_state["guess_mode"]

def check_guess(user_guess):
    st.session_state["guess_mode"] = False
    if user_guess == st.session_state["random_name"]:
        st.session_state["message"] = "Correct! You guessed the name."
        st.session_state["Game_over"] = True
    else:
        st.session_state["lives"] -= 1
        if st.session_state["lives"] <= 0:
            st.session_state["message"] = f"You Failed once again. The name was {st.session_state['random_name']}."
            st.session_state["Game_over"] = True
        else:
            st.session_state["message"] = f"{user_guess} is wrong! ({st.session_state['lives']} lives left)"

#Oberfläche
user_name = st.text_input("Enter your name:", key="name_input")

if st.session_state["guesser"]:
    st.write(st.session_state["message"])
    user_guess = st.text_input("Enter your guess:", key="guess_input")

if st.session_state["lives"] <= 0:
    st.write(f"You Failed once again.You will never know the name.")
    st.session_state.update({"stats_page": True})

Lives_left = st.session_state["lives"]
if Lives_left > 0:
    st.image(["https://media.tenor.com/8X0g1k5J6nIAAAAC/pepe-frog.gif"] * Lives_left, width=32)

if st.session_state["guess_mode"]:
    st.write("Who am I?")
    cols = st.columns(3)
    for i, name in enumerate(names):
        cols[i % 3].button(name,key=f"guess_{name}",on_click=check_guess,args=(name,),disabled=st.session_state["Game_over"],use_container_width=True,)
#Könpfe
if Lives_left > 0:
    st.button("Guess Name", key="submit_button", on_click=check_guess, args=(user_guess,))

st.button("Give Up", key="give_up_button", on_click=lambda: st.write(f"The correct name was: {st.session_state['random_name']}"))
st.button("Guess", key="guess_button", on_click=guess,disabled=st.session_state["Game_over"])