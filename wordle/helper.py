import wordle.tools as wf

# TODO: tidy up loop exits


def wordle_helper():
    """Helper program for playing wordle. Suggests the best guess given the
      current state of the game."""

    pattern = 0
    attempt = 0
    answer_list = wf.load_answers()

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

            answer_list = wf.filter_answers(guess, pattern, answer_list)
            best_guess = wf.return_guess(answer_list)
            print("Computed guess: ", best_guess)
            attempt += 1
