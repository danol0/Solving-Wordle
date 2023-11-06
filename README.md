# Wordle Bot
### Solving Wordle with entropy

This repo contains a algorithm which computes the wordle guess with maximum 1 turn entropy, inspired by the [3blue1brown video](https://www.youtube.com/watch?v=v68zYyaEmEA).

In the `precompute_first_guess notebook` I reproduce the result for best first guess ([post correction](https://www.youtube.com/watch?v=fRed0Xmc2Wg)).

`wordle_bot` contains a program that can be used both to play wordle in the terminal or for self-play of the algorithm against itself for evaluation.

`wordle_helper` can be used to suggest guesses based on a live game of wordle. 

`wordle_answers.txt` contains the 2315 possible wordle answers, which is a subset of the 12964 allowed wordle guesses in `wordle_legal_words.txt`