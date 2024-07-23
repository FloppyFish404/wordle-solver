import requests
import logging
from collections import Counter

logging.basicConfig(level=logging.WARNING, format='%(message)s')

URL = ("https://gist.githubusercontent.com/cfreshman/"
       "d97dbe7004522f7bc52ed2a6e22e2c04/raw/"
       "633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt")
REMOTE_WORDS = "remote_words.txt"
LOCAL_WORDS = 'words.txt'  # contains all guesses and answers
LOCAL_GUESSES = 'guesses.txt'  # guesses that aren't possible answers
LOCAL_ANSWERS = 'answers.txt'  # possible answers


def fetch_remote_word_list():
    try:
        response = requests.get(URL, timeout=1)
        return response
    except requests.ConnectionError:
        return None


def write_remote_word_list(response):
    if response:
        with open(REMOTE_WORDS, 'w') as file:
            file.write(response.text)


def check_remote_local_words_match():
    with open(REMOTE_WORDS) as f:
        remote = f.readlines()
    with open(LOCAL_WORDS) as f:
        local = f.readlines()
    return local == remote


def get_word_list(filename):
    with open(filename) as f:
        words = f.readlines()
    for i, x in enumerate(words):
        words[i] = x.strip()
    return words

def get_answer_list():  # noqa
    return get_word_list(LOCAL_ANSWERS)

def get_guess_list():  # noqa
    return get_word_list(LOCAL_GUESSES)

def get_all_words_list():  # noqa
    return get_word_list(LOCAL_WORDS)


class Feedback:
    """
    Manages information gained from wordle guesses
    """
    def __init__(self):
        self.greens = [None]*5
        self.yellows = [[] for _ in range(5)]  # list of yellows for each position
        self.grays = set()

    def merge(self, feedback):
        """ Add new feedback to self """
        # GREENS
        for i, green in enumerate(feedback.greens):
            if (self.greens[i] and green) and (self.greens[i] != green):
                raise ValueError('Unmatching green lets during feedback merge')
            self.greens[i] = green if green else self.greens[i]

        # YELLOWS
        for pos, (old_yels, new_yels) in enumerate(zip(self.yellows, feedback.yellows)):
            yel_union = set(old_yels).union(new_yels)
            self.yellows[pos] = list(self._filter_yellows(yel_union))

        # GRAYS
        self.grays.update(feedback.grays)

    def _filter_yellows(self, yel_union):
        """
        Filter out shorter yellows of repeat letters
        e.g. {'eee', 'ee', 'e'} -> {'eee'}
        """
        if len(yel_union) > 1:
            long_yellows = [yel for yel in yel_union if len(yel) > 1]
            for long_yel in long_yellows:
                for length in range(1, len(long_yel)):
                    yel_union.discard(long_yel[0] * length)
        return yel_union

    def is_same(self, feedback):
        if self.greens != feedback.greens:
            return False
        if any(set(y1) != set(y2) for y1, y2 in zip(self.yellows, feedback.yellows)):
            return False
        if self.grays != feedback.grays:
            return False
        return True


def get_guess_feedback(guess, answer) -> Feedback:
    """ Compares guess to answer and returns feedback """
    feedback = Feedback()

    def yellow_or_gray():
        """
        Logic for when guess and answer both contain letter repeats, and
        guess contains more repeats of letter than answer. In a Wordle,
        yellows are assigned in order i.e. first come first served.
        """
        greens_count = sum(1 for j in range(5) if guess[j] == answer[j])
        yellows_remaining = answer_count - greens_count

        for j in range(5):
            if j == i and yellows_remaining > 0:
                feedback.yellows[i].append(g_let * answer_count)
            if guess[j] == g_let and guess[j] != answer[j]:
                yellows_remaining -= 1

    for i, (g_let, a_let) in enumerate(zip(guess, answer)):
        if g_let == a_let:
            feedback.greens[i] = answer[i]  # GREEN
        elif g_let in answer:
            guess_count, answer_count = guess.count(g_let), answer.count(g_let)
            if guess_count <= answer_count:  # YELLOW
                feedback.yellows[i].append(g_let * guess_count)
            else:
                yellow_or_gray()
                feedback.grays.add(g_let * (answer_count+1))
        else:
            feedback.grays.add(g_let)  # GRAY

    return feedback


def possible_answer(feedback, word) -> bool:
    """
    Returns True or False depending on if a word is a possible answer
    based on previously gathered feedback
    """
    # check greens
    for i, green in enumerate(feedback.greens):
        if green and green != word[i]:
            return False

    # compute letter counts in word
    let_count = {}
    for let in word:
        let_count[let] = let_count[let] + 1 if let in let_count else 1

    # check yellows
    for pos, yellows in enumerate(feedback.yellows):
        for yel in yellows:
            if (yel[0] == word[pos] or
                    yel[0] not in let_count or
                    yel[0] in let_count and len(yel) > let_count[yel[0]]):
                return False

    # check grays
    for gray in feedback.grays:
        if gray[0] in let_count and len(gray) <= let_count[gray[0]]:
            return False

    return True


def get_possible_answers(feedback, answer_pool) -> list:
    l = []  # noqa
    for answer in answer_pool:
        if possible_answer(feedback, answer):
            l.append(answer)
    return l


def count_possible_answers(feedback, answer_pool) -> int:
    count = 0
    for answer in answer_pool:
        if possible_answer(feedback, answer):
            count += 1
    return count


class CommonLetters:
    """
    Calculates information regarding letter distribution in a given answerpool,
    to find guesses likely to be most relevant
    """
    def __init__(self, answer_pool):
        self.answer_pool = answer_pool
        self.common_letters = Counter()
        self.let_position = [Counter() for _ in range(5)]
        for ans in answer_pool:
            for i, let in enumerate(ans):
                self.let_position[i][let] += 1
                self.common_letters[let] += 1

        for pos in self.let_position:
            if len(pos) == 1:  # greens, no new information, not good to guess
                let = next(iter(pos.keys()))
                self.common_letters[let] -= pos[let]

    def calc_smart_guess_scores(self, guess_pool):
        """
        Returns guesses that have lots of relevant letters
        so are likely to greatly reduce size of answerpool.

        No bonus is given if guess is a possible answers.

        Most likely usage is to opimise guess_pool for find_best_guess()
        which is computationally expensive as it utilises recursive function
        turns_until_solved() # O(?) time?
        """
        guess_scores = Counter()
        for guess in guess_pool:
            score = 0
            for i, guess_let in enumerate(guess):

                # relevance of letter in position
                if len(self.let_position[i]) != 1:  # greens, so no new info
                    size = self.let_position[i].total()
                    position_let_count = self.let_position[i][guess_let]
                    score += position_let_count * size // size 

                # relevance of letter not in position
                if guess_let not in set(guess[0:i]):
                    size = self.common_letters.total()
                    total_let_count = self.common_letters[guess_let]
                    position_let_count = self.let_position[i][guess_let]
                    score += total_let_count * size // size

            guess_scores[guess] = score
        return guess_scores

    def get_smart_guesses(self, guess_pool, size):
        guess_scores = self.calc_smart_guess_scores(guess_pool)
        return [guess for guess, _ in guess_scores.most_common(size)]

    def print_smart_guesses(self, guess_scores, size=None):
        logging.debug('')
        logging.debug('COMMON LETTERS:')
        logging.debug(f'{self.common_letters}')
        logging.debug('\n')
        logging.debug('LETTERS IN POSITION:')
        for i, lets in enumerate(self.let_position):
            logging.debug(f'POSITION {i+1}')
            logging.debug(f'{lets}')
            logging.debug('')
        logging.debug('')
        logging.debug('GUESS SCORES:')
        for g_score in guess_scores.most_common(size):
            logging.debug(f'{g_score}')


def find_best_guess(guess_pool, answer_pool, feedback=None,
                    guesses_tried=None):
    """
    Returns the guess in either guess_pool or answer_pool that will result in
    the least amount of turns to solve the remainder of the wordle puzzle.

    """
    if len(answer_pool) <= 2:
        return answer_pool[0]  # any potential answer will be best guess

    # solve exactly with entire wordpool
    elif len(answer_pool) < 17:
        best_guess = find_exact_best_guess(guess_pool, answer_pool, feedback, guesses_tried)

    # solve exactly for ~10 optimised guesses
    elif len(answer_pool) < 100:
        n_guesses = 10
        smart_guesses = filter_guess_pool(guess_pool, answer_pool, n_guesses)
        best_guess = find_exact_best_guess(guess_pool, answer_pool, feedback,
                                           guesses_tried, smart_guesses)

    # solve approximately for 100 optimised guesses
    else:
        n_guesses = 100
        smart_guesses = filter_guess_pool(guess_pool, answer_pool, n_guesses)
        smart_guesses = smart_guesses[0].extend(smart_guesses[1])
        best_guess = find_approximate_best_guess(smart_guesses, answer_pool, feedback)

    return best_guess


def remove_possible_answers(guess_pool, answer_pool, guesses_tried):
    filtered = []
    for guess in guess_pool:
        if guess not in guesses_tried and guess not in answer_pool:
            filtered.append(guess)
    return filtered


def filter_guess_pool(guess_pool, answer_pool, size):
    """
    Filters list of potential guesses to a given size based off
    common letters in the answerpool to to optimise find_best_guess.

    format of smart guesses [[answers], [non_answers]]
    """
    common = CommonLetters(answer_pool)
    smart_guesses = []
    smart_guesses.append(common.get_smart_guesses(answer_pool, size//2))
    smart_guesses.append(common.get_smart_guesses(guess_pool, size//2))
    return smart_guesses


def find_exact_best_guess(guess_pool, answer_pool, feedback,
                          guesses_tried, smart_guesses=None):
    """
    Returns the exact best guess and its expected turns until solved based on
    the complete probability tree of scenarios.

    Used with high frequency in recursive function time_until_solved() making
    up the majority of the computational time
    """
    max_size = 100
    if len(answer_pool) > max_size:
        raise ValueError("answer pool is too large to solve exactly, \
                         this will take too long")
    if smart_guesses:
        non_answer_guesses = smart_guesses[0]
        answer_guesses = smart_guesses[1]
    else:
        non_answer_guesses = guess_pool
        answer_guesses = answer_pool

    guess_turns = {}

    best_case_turns = (2*len(answer_pool))-1 / len(answer_pool)
    for guess in answer_guesses:
        turns = turns_until_solved(guess, guess_pool, answer_pool,
                                   feedback, guesses_tried)
        if turns == best_case_turns:
            return guess
        guess_turns[guess] = turns

    best_case_turns = 2.0  # best case for non answer_pool guess
    for guess in non_answer_guesses:
        turns = turns_until_solved(guess, guess_pool, answer_pool,
                                   feedback, guesses_tried)
        if turns == best_case_turns:
            return guess
        guess_turns[guess] = turns
    return min(guess_turns, key=guess_turns.get)


def find_approximate_best_guess(guess_pool, answer_pool, old_feedback):
    """
    Returns the best guess, as defined by the smallest average length of the
    resulting answerpool the next turn.
    """
    answers = set(answer_pool)
    guess_scores = {}
    for guess in guess_pool:
        total_score = 0
        feedbacks = Counter()
        for answer in answer_pool:
            f = get_guess_feedback(guess, answer)
            f.merge_feedback(old_feedback)
            feedbacks[f] += 1
        for f in feedbacks:
            total_score += count_possible_answers(f, answer_pool) * feedbacks[f]
        score = total_score / len(answer_pool)
        if guess in answers:  # approx bonus score given to potential answers
            score -= 1
        guess_scores[guess] = score
    guess_scores = sorted(guess_scores.items(), key=lambda item: item[1], reverse=True)
    return guess_scores


def turns_until_solved(guess, guesspool, answerpool, existing_feedback=None,
                       tried_guesses=None, turn=1):
    """
    Solves and returns exactly the average turns taken to reach the answer,
    by iterating through all scenarios as a probability tree.

    Assumes the best guess is entered every turn. The best guess is the guess
    that leads to the lowest mean average number of turns to solve the wordle.

    Returns a float of the number of predicted turns.
    """

    # BASE CASES
    if len(answerpool) == 1:
        if guess == answerpool[0]:
            return turn
        else:
            return turn + 1
    elif len(answerpool) == 2:
        return turn + 0.5 # 50/50 of getting the right turn

    feedbacks = {}
    expected_turns = {}

    if not tried_guesses:
        tried_guesses = set()
    tried_guesses.add(guess)

    # GET FEEDBACK
    for potential_answer in answerpool:
        if guess == potential_answer:
            expected_turns[turn] = 1
        else:
            new_feedback = get_guess_feedback(guess, potential_answer)
            if existing_feedback:
                new_feedback.merge(existing_feedback)

            # APPEND TO FEEDBACK COUNTER
            for f in feedbacks:
                if f.is_same(new_feedback):
                    feedbacks[f] += 1
                    break
            else:
                feedbacks[new_feedback] = 1

    logging.debug(f'FEEDBACKS SET {guess} {turn}')
    for f in feedbacks:
        possible_answers = get_possible_answers(f, answerpool)
        logging.debug(f'count {feedbacks[f]}  {possible_answers}') 
        logging.debug(f'{f.greens}')
        logging.debug(f'{f.yellows}')
        logging.debug(f'{f.grays}')
        # logging.debug('possible ans', len(possible_answers))
        if len(possible_answers) == 0:
            raise IndexError('No possible answers with this set of feedback')
        best_guess = find_best_guess(guesspool, possible_answers, f, tried_guesses)
        logging.debug(f'for above feedback, best guess next turn is {best_guess}')
        turns = turns_until_solved(best_guess, guesspool, possible_answers,
                                   f, tried_guesses, turn+1)
        expected_turns[turns] = expected_turns.get(turns, 0) + feedbacks[f]

    average_turns = (sum(k*v for k, v in expected_turns.items())
                     / sum(expected_turns.values()))

    logging.debug(f'{expected_turns} {average_turns}\n\n')
    return average_turns


def show_result(guesses, turn, ANSWER):
    print(f'the answer was {ANSWER}')
    print(f'best guesses found were {guesses}')
    print(f'took {turn} turns to solve')


"""
TO DO:
implement find_best_guess for multiple answerpool sizes
TEST THE SHIT OUT OF THIS
change Feedback.is_same into __eq__ and __hash__
implement entropy/score function? if needed
implemenet memoisation
implement options for main, evaluate a guess,
change code to work for answers list
"""
