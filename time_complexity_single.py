import lib
import random
from timeit import default_timer as timer

size_answerpool = int(input('size of answer_pool to test? '))
size_guesspool = int(input('size of guess_pool to test? '))

words = lib.get_local_words_list()
random.shuffle(words)
guesspool = []
answerpool = []
for i in range(size_answerpool):
    word = words.pop()
    answerpool.append(word)
for i in range(size_guesspool - size_answerpool):
    if i < len(answerpool):
        guesspool.append(answerpool[i])
    else:
        word = words.pop()
        guesspool.append(word)
start = timer()
best_guess = lib.find_best_guess(guesspool, answerpool)
end = timer()
total_time = end - start
print(size_answerpool, total_time)
# turns = lib.turns_until_solved(best_guess, guesspool, answerpool)
