import wordle_functions as wf

def wordleHelper() :
    """Helper program for playing wordle. Suggests the best guess given the current state of the game."""

    pattern = 0
    attempt = 0
    answerList = wf.loadAnswers()

    while attempt < 6 :

        #precomputed best first guess to save time
        if attempt == 0 :
            guess = wf.loadFirstGuess()
            print("Computed guess: ", guess)
            attempt += 1

        else :
            guess = input("Enter what you guessed: ")
            pattern = list(map(int, input("Enter the pattern as a number with no spaces: ")))

            if pattern == [2,2,2,2,2] :
                return
            
            answerList = wf.filterAnswers(guess,pattern,answerList)
            bestGuess = wf.returnGuess(answerList)
            print("Computed guess: ", bestGuess)
            attempt += 1

wordleHelper()