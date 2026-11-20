import streamlit as st
import random
import time
import os
from openai import OpenAI, OpenAIError       

names = ["Pinocchio","The Frog Prince","Puss in Boots","The Bremen Town Musicians","Mother Holle","The Genie","The Seven Dwarfs","Rumpelstiltskin",
        "Snow White","Cinderella","Red Riding Hood","Sleeping Beauty","The Snow Queen","Hansel","Gretel",
        "The Witch","The Pied Piper","The Big Bad Wolf","King Thrushbeard","The Star Money Girl"]#Personen Liste
CHARACTERS = {name: f"Images/{name}.png" for name in names}                          
Max_Live = 3

Greetings = ["Ooh  the famous knight {name}, I see. Lets see if you can best me",
"A losy jester not even worth remembering by name, but a word is a word i suppose.Just dont expeact to win",
"A brave soul, I see. I will give you a chance to prove yourself. But be warned, the path ahead is treacherous.",
"The king himself? I am honored to have you here. But do not let your title fool you, for the game I propose is not for the faint of heart."]

#Game state
st.session_state.setdefault("random_name", random.choice(names))  # alle Konstanten
st.session_state.setdefault("lives", Max_Live)
st.session_state.setdefault("guesser", True)
st.session_state.setdefault("Game_over", False)
st.session_state.setdefault("stats_page", False)
st.session_state.setdefault("guess_mode", False) 
st.session_state.setdefault("started", False)
st.session_state.setdefault("player_name", "")
st.session_state.setdefault("games",[])
st.session_state.setdefault("questions",0)
st.session_state.setdefault("time",0)
st.session_state.setdefault("chat", [])
st.session_state.setdefault("remaining", list(names))   
st.session_state.setdefault("question_log", [])         
st.session_state.setdefault("question_history", [])     

#Funktionen
def start_game():
    st.session_state["time"] = time.time()
    st.session_state["started"] = True
    st.session_state["message"] = "Dont Forget ask as much as you want, but you can only guess 3 times."

def guess():
    st.session_state["guess_mode"] = not st.session_state["guess_mode"]

def check_guess(user_guess):
    st.session_state["guess_mode"] = False
    if user_guess == st.session_state["random_name"]:
        st.session_state["message"] = "Correct! You guessed the name."
        st.session_state["Game_over"] = True
        save_game(True)
    else:
        st.session_state["lives"] -= 1
        if st.session_state["lives"] <= 0:
            st.session_state["message"] = f"You Failed once again. The name was {st.session_state['random_name']}."
            st.session_state["Game_over"] = True
            save_game(False)
        else:
            st.session_state["message"] = f"{user_guess} is wrong! You have only ({st.session_state['lives']} trys left)"

def give_up():
    st.session_state["Game_over"] = True
    st.session_state["message"] = "So easy to be discurraged ?"   
    save_game(False)                                               

def save_game(won):
    st.session_state["games"].append({
        "player_name": st.session_state["player_name"],
        "random_name": st.session_state["random_name"],
        "won": won,
        "questions": st.session_state["questions"],
        "lives_lost": Max_Live - st.session_state["lives"],
        "seconds": round(time.time() - st.session_state["time"]),
        "left_at_guess": len(st.session_state["remaining"]),   
    })
    for q in st.session_state["question_log"]:                 # Fragen für die Stats-Seite sichern
        st.session_state["question_history"].append({"game": len(st.session_state["games"]), **q})

# LLM: fragt die KI, für welche Figuren die Antwort "Ja" ist (Aufbau wie in 07-aiapp.py)
def ask_witch(question):
    try:
        response = client.chat.completions.create(
            model="google/gemma-4-E4B-it",
            messages=[
                {"role": "system", "content": "We play 'Who am I?' with these fairy tale characters: "
                 + ", ".join(names) + ". The user asks a yes/no question. List ALL characters for which "
                 "the answer is yes, separated by commas. Write nothing else."},
                {"role": "user", "content": question},
            ],
        )
        text = response.choices[0].message.content
        return [name for name in names if name in text]       
    except OpenAIError as e:
        st.error(e)          # nur zum Testen
        return None                                                         

#Oberfläche
 # LLM: API-Key abfragen, stoppen wenn keiner da ist (wie in 07-aiapp.py)
with st.sidebar:
     api_key = st.text_input("UOS AI API-Key", type="password", key="uos_api_key").strip()
if not api_key:
        st.info("Please enter your Uni Osnabrück API key. You can get one at https://ai-keys.uni-osnabrueck.de.")
        st.stop()
client = OpenAI(base_url="https://litellm.uni-osnabrueck.de/v1", api_key=api_key, timeout=30, max_retries=1) #beschränlte wartezeit

if not st.session_state["started"]:
    st.title("Who am I?")
    st.write("Let me know your name, little one. If you will, I have a proposal for you: guess who I am. If you fail, you will lose everything.")
    st.session_state["player_name"] = st.text_input("Enter your name:", key="name_input")
    if st.session_state["player_name"]:                            # FIX: eingerückt
        st.write(random.choice(Greetings).format(name=st.session_state["player_name"]))
    st.button("Start Game", on_click=start_game, disabled=not st.session_state["player_name"])
    st.stop()

if st.session_state["questions"] >= 5:
    st.write("Did you really think you can ask as much as you want? It is time for a Guess dear guest")
    st.session_state["guess_mode"] = True

Lives_left = st.session_state["lives"]
left, right = st.columns([3, 2])          #anpassung seiten aufteilung

with left:
    st.write("Who am I?")
    cols = st.columns(5)
    for i, name in enumerate(names):
        if os.path.exists(CHARACTERS[name]):
            cols[i % 5].image(CHARACTERS[name])
        else:
            cols[i % 5].write("?")
        cols[i % 5].button(name,key=f"guess_{name}",on_click=check_guess,args=(name,),disabled=not st.session_state["guess_mode"] or st.session_state["Game_over"],use_container_width=True,)

with right:
    if Lives_left > 0:
        st.image(["Images/heart.gif"] * Lives_left, width=36)
    st.write(st.session_state["message"])

    with st.container(height=350):        #damit nur chat
        for msg in st.session_state["chat"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    question = st.chat_input("Ask me a yes/no question...", disabled=st.session_state["Game_over"])
    if question:
        st.session_state["chat"].append({"role": "user", "content": question})
        with st.spinner("The witch is thinking..."):
            yes = ask_witch(question)
        if yes is None:
            reply = "My crystal ball is cloudy... (connection problem, try again)"
        else:
            answer = st.session_state["random_name"] in yes                       # nur ja wenn figur dabei
            before = len(st.session_state["remaining"])
            st.session_state["remaining"] = [n for n in st.session_state["remaining"] if (n in yes) == answer]
            st.session_state["questions"] += 1
            st.session_state["question_log"].append({
                "question": question,
                "answer": "Yes" if answer else "No",
                "before": before,
                "after": len(st.session_state["remaining"]),
            })
            reply = "Yes!" if answer else "No!"
        st.session_state["chat"].append({"role": "assistant", "content": reply})
        st.rerun()

    #Knöpfe
    st.button("Guess", key="guess_button", on_click=guess, disabled=st.session_state["Game_over"])
    st.button("Give Up", key="give_up_button", on_click=give_up, disabled=st.session_state["Game_over"])
    if st.session_state["Game_over"]:
        if st.button("See your stats"):
            st.switch_page("stats.py")