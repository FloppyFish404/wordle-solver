import lib
import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt

max_size_answerpool = int(input('max size of answer_pool to test? '))
max_size_guesspool = int(input('max size of guess_pool to test? '))

average_times = {}
for size_answerpool in range(1, max_size_answerpool):
    total_time = 0
    words = lib.get_local_words_list()
    random.shuffle(words)
    guesspool = []
    answerpool = []
    for i in range(size_answerpool):
        word = words.pop()
        answerpool.append(word)
    for i in range(max_size_guesspool - size_answerpool):
        if i < len(answerpool):
            guesspool.append(answerpool[i])
        else:
            word = words.pop()
            guesspool.append(word)
    start = timer()
    best_guess = lib.find_best_guess(guesspool, answerpool)
    end = timer()
    total_time = end - start
    average_times[size_answerpool] = total_time
    print(size_answerpool, total_time)
    # turns = lib.turns_until_solved(best_guess, guesspool, answerpool)

input_sizes = list(average_times.keys())
execution_times = list(average_times.values())
plt.plot(input_sizes, execution_times, marker='o')
plt.xlabel('Input Size')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time vs. Input Size')
# plt.yscale('log')  # Logarithmic scale to better visualize the growth
plt.show()
