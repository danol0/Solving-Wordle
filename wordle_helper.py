import wordle_functions as wf

# TODO: tidy up loop exits


def wordle_helper():
    """Helper program for playing wordle. Suggests the best guess given the
      current state of the game."""

    pattern = 0
    attempt = 0
    answerList = wf.load_answers()

    while attempt < 6:

        # precomputed best first guess to save time
        if attempt == 0:
            guess = wf.load_first_guess()
            print("Computed guess: ", guess)
            attempt += 1

        else:
            guess = input("Enter what you guessed: ")
            pattern = list(map(int, input("Enter the pattern as a number with "
                                          "no spaces: ")))

            if pattern == [2, 2, 2, 2, 2]:
                return

            answerList = wf.filter_answers(guess, pattern, answerList)
            bestGuess = wf.return_guess(answerList)
            print("Computed guess: ", bestGuess)
            attempt += 1
