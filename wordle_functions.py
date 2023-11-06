import numpy as np

#Using sets for efficiency
def loadGuessableWords():
    with open("wordle_legal_words.txt", "r") as file:
        words = set(word.strip() for word in file)
    return words

def loadAnswers():
    with open("wordle_answers.txt", "r") as file:
        answers = set(answer.strip() for answer in file)
    return answers

def loadFirstGuess() :
    with open("first_turn_entropies.txt", "r") as file:
        guess = file.readline()
        return guess.split(':')[0].strip()



def filterAnswers(guess, pattern, wordlist) :
    """Filters the answer list for just words that match the given guess & pattern"""
    return [a for a in wordlist if generateColourPattern(guess,a) == pattern]


def patternFeedback(pattern, guess) :
    """Returns the coloured text block output for a given guess and pattern"""
    feedback = ""
    for i in range(5) :
        
        if pattern[i] == 2 :
            feedback += "\033[0;30;42m" + guess[i]

        elif pattern[i] == 1 :
            feedback += "\033[0;30;43m" + guess[i]

        else :
            feedback += "\033[0;30;41m" + guess[i]

    feedback += "\033[0;0m"
    return(feedback)


def generateColourPattern(guess,answer) :
    """Returns a colour pattern list for a given guess and answer"""

    #default to all grey
    pattern = [0,0,0,0,0]
    correctGuesses = []

    #check for green
    for i in range(5) :
        if guess[i] == answer[i] :
            pattern[i] = 2
            correctGuesses.append(guess[i])

    #check for yellow
    for i in range(5) :
        if guess[i] in answer and guess[i] != answer[i] :
            #yellows letter are highlighted in order, up to the count in the answer minus the number guessed correctly
            n = answer.count(guess[i])
            c = correctGuesses.count(guess[i])
            if guess.count(guess[i],0,i+1) <= n-c :
                pattern[i] = 1

    return pattern


def calculateEntropy(distributionDict) :
    """Calculates the entropy of a given distribution of patterns"""

    observations = distributionDict.values()
    total = sum(observations)
    probabilities = [x/total for x in observations]
    entropy = -sum([p*np.log2(p) for p in probabilities])
    return entropy


def returnGuess(possibleAnswers) :
    """Generates a dictionary of entropies for all legal guesses given set of possible answers, 
    then uses this to return the best guess"""
    
    remainingEntropy = np.log2(len(possibleAnswers))
    wordEntropies = {}

    for guess in loadGuessableWords() :
        patternDist = {}

        #find the distribution of patterns for this guess against all possible answers
        for answer in possibleAnswers :
            pattern = ''.join(str(x) for x in generateColourPattern(guess,answer))
            patternDist[pattern] = patternDist.get(pattern,0) + 1

        #calculate the total entropy for this distribution
        e = calculateEntropy(patternDist)

        #add this to the dictionary of entropies for all guesses
        wordEntropies[guess] = wordEntropies.get(guess,0) + e

    #check the entropy of the valid answers
    validKeys = loadAnswers().intersection(set(possibleAnswers))
    validEntropies = {key: wordEntropies[key] for key in validKeys}

    #if there is only one valid answer, return it
    if len(validEntropies) == 1 :
        return list(validEntropies.keys())[0]
    
    #if there is a valid answer with higher entropy than the remaining entropy, return it
    elif max(validEntropies.values()) > remainingEntropy :
        return max(validEntropies, key=validEntropies.get)
    
    #otherwise return the max entropy guess
    else :
        return max(wordEntropies, key=wordEntropies.get)