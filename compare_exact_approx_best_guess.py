import lib
import random

for seed in range(100):
    print(f'random seed {seed}')
    random.seed(seed)
    words = lib.get_all_words_list()
    answerpool = []
    max_size = 15
    for i in range(max_size):
        answerpool.append(random.choice(words))
    print(answerpool)
    answerpool = ['broke', 'drove', 'erode', 'froze', 'grove']

    smart_guesses = lib.filter_guess_pool(words, answerpool, 100)
    best_guess = lib.find_exact_best_guess(words, answerpool, None,
                                           set(), smart_guesses)
    turns = lib.turns_until_solved(best_guess, words, answerpool)
    print(' exact:', best_guess, turns)

    best_guess = lib.find_approximate_best_guess(words, answerpool)
    turns = lib.turns_until_solved(best_guess, words, answerpool)
    print('approx:', best_guess, turns, '\n')
