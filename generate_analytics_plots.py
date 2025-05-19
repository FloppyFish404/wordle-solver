import matplotlib.pyplot as plt
import json
from collections import Counter
import numpy as np

with open('analytics.txt', 'r') as f:
    data = json.load(f)

all_times = []
no_guesses = Counter()

for entry in data.values():
    all_times.append(entry['time'])
    no_guesses[entry['num_guesses']] += 1

# ---- Plot 1: Histogram of solve times ----
plt.figure()
plt.hist(all_times, bins=np.arange(0, max(all_times), 0.01), edgecolor='black')
plt.xlabel('Solve Time (seconds)')
plt.ylabel('Frequency')
plt.title('Distribution of Solve Times')
plt.xlim(left=0)  
plt.savefig('solve_times_histogram.png')


# ---- Plot 2: Bar graph of number of guesses ----
plt.figure()
x = sorted(no_guesses.keys())
y = [no_guesses[k] for k in x]
plt.bar(x, y)
plt.xlabel('Number of Guesses to Solve')
plt.ylabel('Frequency')
plt.title('Distribution of Guesses per Solve')
plt.xticks(x)
plt.savefig('no_guesses_bar_chart.png')


# Show both plots
plt.show()

average_solve_time = sum(all_times) / len(all_times)
print(average_solve_time)

no_entries = sum(no_guesses.values())
total_turns = sum([k*v for k, v in no_guesses.items()])
average_no_turns = total_turns / no_entries
print(no_guesses)
print(average_no_turns)
