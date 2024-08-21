import lib
import random
import logging
import sys

def main(): 

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    guess_pool = lib.get_all_words_list()
    answer_pool = lib.get_answer_list()

    if any(arg in {'random', 'r'} for arg in sys.argv):
        ANSWER = random.choice(answer_pool)
        wordle_id = ''
    elif len(sys.argv) > 1:
        if sys.argv[1] in answer_pool:
            ANSWER = sys.argv[1]
            wordle_id = ''
        else:
            raise ValueError('Please provide a valid 5 letter word to solve. '
                             f'{sys.argv[1]} is not a valid word.')
    else:
        ANSWER, wordle_id = lib.fetch_official_answer_and_id()
    logging.info(f'ANSWER IS {ANSWER}')

    turn = 0
    solved = False
    feedback = lib.Feedback()
    guesses = []
    while not solved and turn <= 6:
        if turn == 0:
            guess = 'roate'
        else:
            guess = lib.find_best_guess(guess_pool, answer_pool, feedback, set(guesses))
        logging.info(f'turn {turn+1} guess {guess}')
        guesses.append(guess)
        if guess == ANSWER:
            solved = True
        else:
            new_feedback = lib.get_guess_feedback(guess, ANSWER)
            feedback.merge(new_feedback)
            answer_pool = lib.get_possible_answers(feedback, answer_pool)
        turn += 1
        logging.info(f'{vars(feedback)}')
        logging.info(f'possible answers {answer_pool}')
        logging.info(f'guesses {guesses}\n')
    text = lib.get_attempt_text(guesses, ANSWER, wordle_id)
    print(f'{text}\nAnswer was {ANSWER}, guessed {guesses}\n')

if __name__ == '__main__':
    main()

# 6 turn answers:
#       keyed
#       gazed
