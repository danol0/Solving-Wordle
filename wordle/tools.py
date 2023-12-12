import numpy as np


def load_guessable_words():
    with open("wordle_legal_words.txt", "r") as file:
        words = set(word.strip() for word in file)
    return words


def load_answers():
    with open("wordle_answers.txt", "r") as file:
        answers = set(answer.strip() for answer in file)
    return answers


def load_first_guess(answer_list):
    """Loads a precomputed first guess if available, otherwise recalculates it"""
    try:
        with open("first_turn_entropies.txt", "r") as file:
            guess = file.readline()
            return guess.split(':')[0].strip()
    except FileNotFoundError:
        return return_guess(load_answers())


def filter_answers(guess, pattern, wordlist):
    """Filters answers for just words that match the given guess & pattern"""

    return [a for a in wordlist if generate_pattern(guess, a) == pattern]


def pattern_feedback(pattern, guess):
    """Returns the coloured text block output for a given guess and pattern"""

    feedback = ""
    for i in range(5):

        if pattern[i] == 2:
            feedback += "\033[0;30;42m" + guess[i]

        elif pattern[i] == 1:
            feedback += "\033[0;30;43m" + guess[i]

        else:
            feedback += "\033[0;30;41m" + guess[i]

    feedback += "\033[0;0m"
    return feedback


def generate_pattern(guess, answer):
    """Returns a colour pattern list for a given guess and answer"""

    # default to all grey
    pattern = [0, 0, 0, 0, 0]
    correct_guesses = []

    # check for green
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 2
            correct_guesses.append(guess[i])

    # check for yellow
    for i in range(5):
        if guess[i] in answer and guess[i] != answer[i]:
            # yellows letter are highlighted in order, up to the count in
            # the answer, minus the number guessed correctly
            n = answer.count(guess[i])
            c = correct_guesses.count(guess[i])
            if guess.count(guess[i], 0, i+1) <= n-c:
                pattern[i] = 1

    return pattern


def calculate_entropy(distribution_dict):
    """Calculates the entropy of a given distribution of patterns"""

    observations = distribution_dict.values()
    total = sum(observations)
    probabilities = [x/total for x in observations]
    entropy = -sum([p*np.log2(p) for p in probabilities])
    return entropy


def generate_entropy_dict(possible_answers):
    """Generates a dictionary of entropies for all legal guesses given a
    set of possible answers"""

    entropy_dict = {}

    for guess in load_guessable_words():
        pattern_dist = {}

        # find the distribution of patterns for this guess
        for answer in possible_answers:
            pattern = ''.join(str(x) for x in generate_pattern(guess, answer))
            pattern_dist[pattern] = pattern_dist.get(pattern, 0) + 1

        # calculate the total entropy for this distribution
        e = calculate_entropy(pattern_dist)

        # add this to the dictionary of entropies for all guesses
        entropy_dict[guess] = entropy_dict.get(guess, 0) + e

    return entropy_dict


def return_guess(possible_answers):
    """Returns the best guess given a set of possible answers"""

    word_entropies = generate_entropy_dict(possible_answers)
    remaining_entropy = np.log2(len(possible_answers))

    # check the entropy of the valid answers
    valid_keys = load_answers().intersection(set(possible_answers))
    valid_entropies = {key: word_entropies[key] for key in valid_keys}

    # if there is only one valid answer, return it
    if len(valid_entropies) == 1:
        return list(valid_entropies.keys())[0]

    # if there is a valid answer with higher entropy than the remaining
    # entropy, return it
    elif max(valid_entropies.values()) > remaining_entropy:
        return max(valid_entropies, key=valid_entropies.get)

    # otherwise return the max entropy guess
    else:
        return max(word_entropies, key=word_entropies.get)
