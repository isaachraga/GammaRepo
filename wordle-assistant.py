# Software Engineering Fall 2024
# Team Gamma
# Wordle Assistant
# Run 'python wordle-assistant.py'

with open("words.txt","r") as f:
    words = f.readlines()

words = [w.strip() for w in words]

# print(len(words))
# print(words[1:3])
# exit(0)

def guess_word(game_State):
    
    charCount = 0 # Ensures the correct amount of characters have been inputted
    prevLetter = '' # Stores letter to use in combination with symbol

    for ch in game_State:
        if ch.isspace(): # Handle whitespace
            continue
        elif ch.isalpha(): # Handle letters
            prevLetter = ch
        elif ch in {'=', '-', '.'} and prevLetter != '': # Handle supported symbols
            wordNum = int((charCount/10)+1)
            letterNum = int((((charCount-1) % 10)/2)+1)

            print("Word " + str(wordNum) + ", Letter " + str(letterNum) + ":  " + prevLetter + " " + ch) # FOR DEBUGGING PURPOSES

            # TO DO: update knowledge on letters based on the inputted info

            prevLetter = '' # Reset previous letter
        else: # Incorrect character inputted
            print("Unexpected Character in Input, Please Try Again")
            return ""
        charCount += 1
    
    # Incorrect amount of characters inputted
    if ((charCount % 10) != 0) or (charCount == 0):
        print("Incorrect Number of Characters, Please Try Again")
        return ""
    
    # Valid input recieved

    # TO DO: use info obtained to get a guess

    return "guess"



# INPUT GAMESTATE:
# groups of 5 letters each suffixed by an identifying symbol (EX: 'g.u-e=s.s.')
# Green: "=", Yellow: '-', Gray: '.'
# Whitespace is disregaurded
# Gamestate should be inputted in full
# Information from previous inputs should not be retained
if __name__ == "__main__":
    while True:
        state = input("\nGame state: ")
        guess = guess_word(state)
        if guess != "":
            print("You should try '" + guess + "'.")
