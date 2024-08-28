with open("words.txt","r") as f:
    words = f.readlines()

words = [w.strip() for w in words]

print(len(words))
print(words[1:3])
exit(0)

def guess_word(game_State):
    return "steal"

if __name__ == "__main__":
    while Ture:
        state = input("Game state?")
        guess = guess_word(state)
        print("You should try '"+guess+"'.")
