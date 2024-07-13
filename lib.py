import requests
from collections import Counter

URL = "https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt"
REMOTE_WORDS = "remote_words.txt"
LOCAL_WORDS = 'words.txt'


class Feedback:
    def __init__(self):
        self.greens = [None]*5
        self.yellows = [[] for _ in range(5)]  # list of yellows for each position
        self.grays = set()

    def merge_feedback(self, feedback):
        """ Add new feedback to self """
        # GREENS
        for i, green in enumerate(feedback.greens):
            if (self.greens[i] and green) and (self.greens[i] != green):
                raise ValueError('Unmatching green letters during feedback merge')  # noqa
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


def get_local_words_list():
    with open(LOCAL_WORDS) as f:
        words = f.readlines()
    for i, x in enumerate(words):
        words[i] = x.strip()
    return words


def check_remote_local_words_match():
    with open(REMOTE_WORDS) as f:
        remote = f.readlines()
    with open(LOCAL_WORDS) as f:
        local = f.readlines()
    return local == remote


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


def find_best_guess(guess_pool, answer_pool, feedback=None):
    """
    returns the guess in guess_pool that will result in the least
    amount of turns to solve the remainder of the wordle puzzle
    """
    # optimisation: initial filter of guess pool
    pass

    # optimisation: best case scenario for early return
    best_case = (2*len(answer_pool))-1 / len(answer_pool)

    if len(answer_pool) <= 2:
        return answer_pool[0]  # any potential answer will be best guess
    guess_turns = {}
    for guess in guess_pool:
        # print(feedback.grays, 'here')
        turns = turns_until_solved(guess, guess_pool, answer_pool, feedback)
        if turns == best_case:
            return guess
        guess_turns[guess] = turns
    print(f'\n\n all guess_turns are {guess_turns}')
    return min(guess_turns, key=guess_turns.get)


def turns_until_solved(guess, guesspool, answerpool, existing_feedback=None, turn=1):
    """
    Returns a float of the number of predicted turns it will take to reach the
    answer, provided the best guess is entered every time.

    The best guess is the one that leads to the lowest mean average number
    of turns to solve the wordle.
    """
    feedbacks = {}
    expected_turns = {}

    # GET FEEDBACK
    for potential_answer in answerpool:
        if guess == potential_answer:
            expected_turns[turn] = 1
        else:
            new_feedback = get_guess_feedback(guess, potential_answer)
            if existing_feedback:
                new_feedback.merge_feedback(existing_feedback)

            # APPEND TO FEEDBACK COUNTER
            for f in feedbacks:
                if f.is_same(new_feedback):
                    feedbacks[f] += 1
                    break
            else:
                feedbacks[new_feedback] = 1

    print('FEEDBACKS SET', guess, turn)
    for f in feedbacks:
        possible_answers = get_possible_answers(f, answerpool)
        print('count', feedbacks[f], possible_answers)
        print(f.greens)
        print(f.yellows)
        print(f.grays)
        print()
        # print('possible ans', len(possible_answers))
        if len(possible_answers) == 0:
            raise IndexError('No possible answers with this set of feedback')
        elif len(possible_answers) == 1:
            turns = turn + 1 # 1 possible answer to guess next turn
        elif len(possible_answers) <= 2:
            turns = turn + 1.5  # 1/2 chance of guessing right
        else:
            best_guess = find_best_guess(guesspool, possible_answers, f)
            print('found best guess as', best_guess)
            turns = turns_until_solved(best_guess, guesspool, answerpool, f)
            if len(possible_answers) == len(answerpool):
                turns += 1

        expected_turns[turns] = expected_turns.get(turns, 0) + feedbacks[f]

    average_turns = sum(k*v for k, v in expected_turns.items()) / sum(expected_turns.values())

    print(expected_turns, average_turns)
    return average_turns


"""
TO DO:
change Feedback.is_same into __eq__
prevent infinite recursion (don't guess same guess)
    should be a stack of guesses, use length of this as turn?
implement entropy/score function
"""
