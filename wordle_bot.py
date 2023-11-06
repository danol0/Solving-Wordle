import wordle_functions as wf
import numpy as np

def wordleGame(selfPlay=True, answer=None, verbose=True) :
    """Plays a game of wordle. If selfPlay is True, uses entropy to make guesses and returns 
    the number of attempts it takes to win. If selfPlay is False, asks for user input.
    Verbose is used to control the print statements and should be left as True for normal play."""

    #load the answer list and pick an answer if none is given
    answerList = wf.loadAnswers()
    answer = answer if answer else np.random.choice(list(answerList))

    for attempt in range(1,7) :

        if selfPlay == True :
            #precomputed best first guess to save time
            if attempt == 1 :
                guess = wf.loadFirstGuess()
            else :
                guess = wf.returnGuess(answerList)

        else :
            guess = input("Enter guess number " + str(attempt) + ": ")

        #generate the pattern & feedback
        pattern = wf.generateColourPattern(guess,answer)
        print(wf.patternFeedback(pattern, guess)) if verbose else None

        if guess == answer :
            print("You won in", attempt, "guesses!") if verbose else None
            return attempt
        
        #filter the answerList
        answerList = wf.filterAnswers(guess,pattern,answerList)
    
    print("Unlucky, the answer was", answer) if verbose else None