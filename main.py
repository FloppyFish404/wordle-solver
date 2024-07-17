import lib
import random


def main():
    guess_pool = lib.get_local_words_list()
    answer_pool = lib.get_local_words_list()
    ANSWER = random.choice(answer_pool)
    print(f'ANSWER IS {ANSWER}')

    turn = 0
    solved = False
    feedback = lib.Feedback()
    guesses = []
    while not solved and turn <= 6:
        guess = lib.find_best_guess(guess_pool, answer_pool, feedback, guesses)
        guesses.append(guess)
        if guess == ANSWER:
            solved = True
        else:
            new_feedback = lib.get_guess_feedback(guess, ANSWER)
            feedback.merge(new_feedback)
            answer_pool = lib.get_possible_answers(feedback, answer_pool)
        turn += 1
    lib.show_result(guesses, turn, ANSWER)


if __name__ == '__main__':
    main()
