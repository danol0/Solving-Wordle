import wordle.tools as wf
import numpy as np


def wordle_bot(selfPlay=True, answer=None, verbose=True):
    """Plays a game of wordle. If selfPlay is True, uses entropy to make
    guesses and returns the number of attempts it takes to win. If selfPlay is
    False, asks for user input. Verbose is used to control the print statements
    and should be left as True for normal play."""

    # load the answer list and pick an answer if none is given
    answer_list = wf.load_answers()
    answer = answer if answer else np.random.choice(list(answer_list))

    for attempt in range(1, 7):

        if selfPlay:
            # precomputed best first guess to save time
            if attempt == 1:
                guess = wf.load_first_guess()
            else:
                guess = wf.return_guess(answer_list)

        else:
            guess = input("Enter guess number " + str(attempt) + ": ")

        # generate the pattern & feedback
        pattern = wf.generate_pattern(guess, answer)
        print(wf.pattern_feedback(pattern, guess)) if verbose else None

        if guess == answer:
            print("Win in", attempt, "guesses!") if verbose else None
            return attempt

        # filter the answer list
        answer_list = wf.filter_answers(guess, pattern, answer_list)

    print("Unlucky, the answer was", answer) if verbose else None
