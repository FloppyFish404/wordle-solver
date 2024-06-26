import requests

URL = "https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt"
REMOTE_WORDS = "remote_words.txt"
LOCAL_WORDS = 'words.txt'


class Feedback:
    def __init__(self):
        self.greens = [None]*5
        self.yellows = [[] for _ in range(5)]  # list of yellows for each position
        self.grays = set()

    def merge_feedback(self, feedback):
        """ merge new feedback into existing feedback """
        pass


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

    for i in range(5):
        if guess[i] == answer[i]:
            feedback.greens[i] = answer[i]

    for i, (g_let, a_let) in enumerate(zip(guess, answer)):
        if g_let == a_let:
            pass  # green, already dealt with above
        elif g_let in answer:
            guess_count = guess.count(g_let)
            answer_count = answer.count(g_let)
            if guess_count > answer_count > 0:
                yellow_or_gray(feedback, i, g_let, guess, answer, guess_count, answer_count)
            elif guess_count <= answer_count:
                length = min(guess_count, answer_count)
                feedback.yellows[i].append(g_let * length)
            else:
                feedback.grays.add(g_let)
        else:
            feedback.grays.add(g_let)

    return feedback


def yellow_or_gray(feedback, i, let, guess, answer, guess_count, answer_count):
    """
    Logic for when both guess and answer contain multiple repeats of the 
    same letter.
    """
    answer_remaining = answer_count - feedback.greens.count(let)
    for j, (g_let, a_let) in enumerate(zip(guess, answer)):
        if j == i:
            if answer_remaining > 0:
                length = min(guess_count, answer_count)
                feedback.yellows[i].append(let * length)
        else:
            feedback.grays.add(let)

        if g_let == let and feedback.greens[i] != g_let:
            answer_remaining -= 1  # noqa


def possible_answer() -> bool:
    check = True
    return check


def get_score() -> float:
    return score


