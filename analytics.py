import lib
import logging
import json, os
import time

"""
Solves the wordle for every possible answer and stores to analytics.txt in a giant dict. For performances testing i.e. finding average no. guesses per solve. 

Supports safe ctrl+c quitting during runtime, storing work done during execution in analytics.txt
"""

guess_pool = lib.get_all_words_list()
answer_pool = lib.get_answer_list()

with open('analytics.txt', 'r') as f:
    answer_guesses = json.load(f)
solved_answers = set(answer_guesses.keys())

not_solved = set(answer_pool) - solved_answers
i = 0

while not_solved:
    start = time.perf_counter()
    ANSWER = not_solved.pop()
    turn = 0
    solved = False
    feedback = lib.Feedback()
    guesses = []
    answer_pool = lib.get_answer_list()
    while not solved and turn <= 6:
        if turn == 0:
            guess = 'roate'
        else:
            guess = lib.find_best_guess(guess_pool, answer_pool, feedback, set(guesses))
        guesses.append(guess)
        if guess == ANSWER:
            solved = True
        else:
            new_feedback = lib.get_guess_feedback(guess, ANSWER)
            feedback.merge(new_feedback)
            answer_pool = lib.get_possible_answers(feedback, answer_pool)
        turn += 1
    end = time.perf_counter()
    time_taken = end - start
    print(f'Answer was {ANSWER}, guessed {guesses}, {len(not_solved)} to solve')
    
    answer_guesses[ANSWER] = {
        "guesses": guesses, 
        "num_guesses": len(guesses),
        "time": round(time_taken, 3)
        }

    guesses
    if i%10 == 0 or not not_solved:
        print('writing to analytics.txt...')
        with open('analytics_tmp.txt', 'w') as f:
            json.dump(answer_guesses, f)
        os.replace('analytics_tmp.txt', 'analytics.txt')
    i += 1

