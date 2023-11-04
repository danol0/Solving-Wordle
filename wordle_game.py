import numpy as np
import re

def loadGuessableWords() :
    words = np.loadtxt("wordle_legal_words.txt",dtype=str)
    return words

def loadAnswers() :
    answers = np.loadtxt("wordle_answers.txt",dtype=str)
    return answers


def feedback(guess, answer) :
    """Returns the coloured text block and regex for filtering for a given guess and answer"""
    feedback = ""
    greenRegex = ""
    yellowRegex = "(?=.*[a-z])"
    greyRegex = " "

    for i in range(5) :
        #for correct behavior we need to go through all the greens first
        if guess[i] == answer[i] :
            feedback += "\033[0;30;42m" + guess[i]
            greenRegex += guess[i]

        #then go through the yellows
        elif guess[i] in answer :
            #count the number of i in answer = n
            n = answer.count(guess[i])
            #only highlight the first n occourences
            if guess.count(guess[i],0,i+1) <= n :
                feedback += "\033[0;30;43m" + guess[i]
            else :
                feedback += "\033[0;30;41m" + guess[i]
            greenRegex += "."
            yellowRegex += "(?=.*" + guess[i] + ")"

        #then add all the letters that are wrong to the greys
        else :
            feedback += "\033[0;30;41m" + guess[i]
            greenRegex += "."
            greyRegex += "(?=.*" + guess[i] + ")"

    feedback += "\033[0;0m"

    return(feedback,greenRegex,yellowRegex,greyRegex)



def filterWordlist(greenRegex, yellowRegex, greyRegex, wordlist) :
    """Filters the wordlist for words that match the given regex"""
    
    greyPattern = re.compile(greyRegex)
    greyFilter = np.vectorize(lambda x: not bool(re.search(greyPattern,x)))

    greenPattern = re.compile(greenRegex)
    greenFilter = np.vectorize(lambda x:bool(re.search(greenPattern,x)))
    
    yellowPattern = re.compile(yellowRegex)
    yellowFilter = np.vectorize(lambda x:bool(re.search(yellowPattern,x)))

    filter = np.logical_and(greyFilter(wordlist),np.logical_and(greenFilter(wordlist),yellowFilter(wordlist)))

    return wordlist[filter]


def game() :
    #load a word
    wordlist = loadGuessableWords()
    answer = np.random.choice(loadAnswers())
    print(answer)

    for attempt in range(5) :
        guess = ""

        while np.isin(guess,wordlist) == False :
            guess = input(f"Attempt {attempt}\nEnter a valid guess: ")
        
        fb, grR, yR, gR = feedback(guess, answer)

        print(fb)

        if guess == answer :
            print("Congrats!")
            return True
        
        wordlist = filterWordlist(grR,yR,gR,wordlist)