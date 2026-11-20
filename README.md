# Who am I? Fairy tale guessing game with both bonus options

2. App: https://who-am-i-to.streamlit.app/  
Code: https://github.com/Kleinstein2/Guessing_game_with_stats

3. Rules are simple: just try to guess which character the game picked with yes or no questions. Every 3 questions you are forced to guess, but if you are sure you know it you can click the guess button. After that you can look at your stats and the best and worst question.

4. The app.py is only for the navigation between the pages. The play.py has the whole game with the start screen, the board with all the characters, the chat with the witch and the buttons. The stats.py shows all the stats after a round. In the Images folder are the pictures of all characters and the heart.

5. The LLM was used as the second player. The character is picked randomly by Python and the LLM does not know which one it is. For every question the LLM gets the names of all characters and lists all characters for which the answer would be yes, based on common knowledge about fairy tales. If the hidden character is in that list the witch answers yes, otherwise no.

6. Extra 2: as explained before, the list from the LLM is used to calculate how many characters each question rules out. Python checks which characters are still possible after every answer. This is used for a second page, Stats, where you can see how long you took, how many lives you had left, how many questions you asked and what your best and worst question were.

7. We implemented a start.bat just so you can pull the git, press start and play instead of using a terminal. The API key will be input on the site itself, so no worry about it being leaked.

8. Except the hearts, all pictures were created using Gemini, as we thought that was easier because of copyright, and we hope it is an acceptable use of AI. The heart was created by WildGoblinDev.

9. Who did what: Malte Bernstein, Niklas Theodor Vartman and Jan Thöle. We all contributed about equally to the project.
