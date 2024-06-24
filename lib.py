import requests

URL = "https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt"
REMOTE_WORDS = "remote_words.txt"
LOCAL_WORDS = 'words.txt'


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


class Feedback:
    def __init__(self):
        self.greens = [None]*5
        self.yellows = [None]*5
        self.grays = set()
