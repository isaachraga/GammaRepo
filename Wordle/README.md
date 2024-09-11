# Wordle
Software Engineering Gamma Project Repository

This program is designed to help users win the game Wordle suggesting words based off the gamestate inputted by the user. The program requires you to enter the 4 default words first in every game, then it determines the correct word of the day on one of its next 2 guesses. The input should only be in the following format:

a-d.i.e-u. w.r-o-n.g. l.y.m.p-h. s.t.a-c.k.

Each group of characters is a five letter word with an identifying symbol following each letter in the word that indicates the status of its respective letter in the current game state. Each group is separated by one space. This is what each symbol indicates:

= The letter is green. This letter is correct and its position is correct.

- The letter is yellow. This letter is in the word, but it is in the wrong position.

. The letter is gray. It is not in the word. 

Rank Word Function
The rank word function scores words based on the frequency of letters in the English language. It uses a frequency table to rank words by adding the score for each letter in the word, and then it selects the highest-ranked word. This word is assumed to be the best guess in terms of uncovering more useful information. 

Guess Word Function
The guess word function processes the input game state, analyzes the feedback for each letter, and makes recommendations based on green, yellow, and gray letters. 
