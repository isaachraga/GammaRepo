# Software Engineering Fall 2024
# Team Gamma
# Wordle Assistant
# Run 'python wordle-assistant.py'

# with open("words.txt","r") as f:
#     words = f.readlines()

# words = [w.strip() for w in words]

# print(len(words))
# print(words[1:3])
# exit(0)

def guess_word(game_State):

    # How common each letter is by weight
    # All weights sum to a total of 10,000
    frequencyTable = {
        'e': 981,
        'a': 844,
        'r': 777,
        'o': 626,
        't': 621,
        'i': 602,
        'l': 600,
        's': 575,
        'n': 510,
        'u': 425,
        'c': 415,
        'y': 387,
        'h': 351,
        'd': 345,
        'p': 321,
        'g': 278,
        'm': 277,
        'b': 248,
        'f': 192,
        'k': 188,
        'w': 180,
        'v': 138,
        'x': 34,
        'z': 33,
        'q': 27,
        'j': 25
    }

    greenLetters = {}

    yellowLetters = {}

    grayLetters = []

    charCount = 0 # Ensures the correct amount of characters have been inputted
    prevLetter = '' # Stores letter to use in combination with symbol
    yellowCount = 0

    for ch in game_State:
        if ch.isspace(): # Handle whitespace
            continue
        elif ch.isalpha(): # Handle letters
            prevLetter = ch
        elif ch in {'=', '-', '.'} and prevLetter != '': # Handle supported symbols
            wordNum = int((charCount/10)+1)
            letterNum = int((((charCount-1) % 10)/2)+1)

            print("Word " + str(wordNum) + ", Letter " + str(letterNum) + ":  " + prevLetter + " " + ch) # FOR DEBUGGING PURPOSES

            #Adds letters to corresponding dictionaries for use in word guessing
            if ch == '=' :
                greenLetters[prevLetter] = letterNum #green stores letter and position
            elif ch == '-' :
                yellowLetters[yellowCount] = [prevLetter, letterNum] #yellow stores letter and not position, uses wordnum to allow for duplicate keys with different values
                yellowCount = yellowCount+1
            elif ch == '.' :
                if prevLetter not in grayLetters:
                    grayLetters.append(prevLetter) #gray just stores letters

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
    wordCount = int((charCount/10))
    print(str(wordCount) + " Words Inputted") # FOR DEBUGGING PURPOSES

    #Dictionary Debug
    print("Green")
    print(greenLetters)
    print("Yellow")
    print(yellowLetters)
    print("Gray")
    print(grayLetters)



    # TO DO: use info obtained to get a guess
    #if number of words submitted is less than 3, use suggestions to collect data
        #figure out best way to collect most data
    #else
        #search through words that meet criteria, add to new list
        #find the best word based on highest value from frequeny table 
    #submit word

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
        guess = guess_word(state.lower())
        if guess != "":
            print("You should try '" + guess + "'.")
